#!/usr/bin/python

# Author: Marco Dinacci - www.intransitione.com -

from PySide.QtCore import *
from PySide.QtGui import *

import photoflow, config

# TODO launch in a new thread the import process
# every image processed send a signal from the import thread
# and set the current filename here. 
# Use a timer that every 20 ms or so refresh the image with the current one
# as there's no need to resize ans show every photo, the human eya is not that fast
class MainWindow(QMainWindow):

    _source = None

    def __init__(self):
        super(MainWindow, self).__init__()
        
        # show the status bar
        self.statusBar()

        self.setWindowTitle("Photoflow")

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
       
        # browse button and label
        self.dirLabel = QLabel("Select the directory containing the photos")
        self.dirBtn = QPushButton("Browse")
        self.dirBtn.clicked.connect(self._showImportDialog)
        
        hbox.addWidget(self.dirLabel)
        hbox.addWidget(self.dirBtn)
        vbox.addLayout(hbox)

        # preview image
        self.preview = QPixmap()
        self._previewLabel = QLabel()
        self._previewLabel.setPixmap(self.preview)
        vbox.addWidget(self._previewLabel)

        # import button
        self.importBtn = QPushButton("Import")
        self.importBtn.setEnabled(False)
        self.importBtn.clicked.connect(self._import)

        vbox.addWidget(self.importBtn)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(vbox)
        self.setCentralWidget(self.mainWidget)
        self.resize(400, 300)

    def update(self, filename):
        self._currentImage = filename
        img = QImage(filename)
        self.preview = QPixmap.fromImage(img).scaledToWidth(380)
        self._previewLabel.setPixmap(self.preview)
        self._previewLabel.adjustSize()

    def _import(self):
        if self._source is not None:
            mm = photoflow.MediaManager()
            mm.set_source(self._source)
            mm.set_destination(config.PHOTOS_DESTINATION)
            mm.register_subscriber(self)

            self.statusBar().showMessage("Importing photos...")
            mm.import_photos()

            # TODO show progress
            self.statusBar().showMessage("Finished importing photos", 5000)

            mm.set_destination(config.VIDEOS_DESTINATION)

            self.statusBar().showMessage("Importing videos...")
            mm.import_videos()
            self.statusBar().showMessage("Finished importing videos", 5000)

    def _showImportDialog(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select directory",\
                self.dirLabel.text(), options)
        if directory:
            self._source = directory
            self.dirLabel.setText(directory)
            self.importBtn.setEnabled(True)

if __name__ == "__main__":
    import sys

    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
    sys.exit()
