#!/usr/bin/python

# Author: Marco Dinacci - www.intransitione.com -

from PySide.QtCore import *
from PySide.QtGui import *

import photoflow, config

class MainWindow(QWidget):

    _source = None

    def __init__(self):
        QWidget.__init__(self, None)

        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        self.dirLabel = QLabel("Select the directory containing the photos")
        self.dirBtn = QPushButton("Browse")
        self.dirBtn.clicked.connect(self._showImportDialog)
        
        hbox.addWidget(self.dirLabel)
        hbox.addWidget(self.dirBtn)
        vbox.addLayout(hbox)

        self.importBtn = QPushButton("Import")
        self.importBtn.clicked.connect(self._import)

        vbox.addWidget(self.importBtn)

        self.setLayout(vbox)

    def _import(self):
        if self._source is not None:
            mm = photoflow.MediaManager()
            mm.set_source(self._source)
            mm.set_destination(config.PHOTOS_DESTINATION)
            mm.import_photos()

            # TODO show progress

            mm.set_destination(config.VIDEOS_DESTINATION)
            mm.import_videos()

    def _showImportDialog(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select directory",\
                self.dirLabel.text(), options)
        if directory:
            self._source = directory
            self.dirLabel.setText(directory)

if __name__ == "__main__":
    import sys

    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
    sys.exit()
