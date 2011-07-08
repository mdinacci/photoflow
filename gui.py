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
        self._dirLabel = QLabel("Select the directory containing the photos")
        self._dirBtn = QPushButton("Browse")
        self._dirBtn.clicked.connect(self._showImportDialog)
        
        hbox.addWidget(self._dirLabel)
        hbox.addWidget(self._dirBtn)
        vbox.addLayout(hbox)

        self._importBtn = QPushButton("Import")
        self._importBtn.clicked.connect(self._import)

        vbox.addWidget(self._importBtn)

        self.setLayout(vbox)

    def _import(self):
        if self._source is not None:
            mm = photoflow.MediaManager()
            mm.select_source(self._source)
            mm.select_destination(config.PHOTOS_DESTINATION)
            mm.import_photos()

            # TODO show progress

            mm.select_destination(config.VIDEOS_DESTINATION)
            mm.import_videos()

    def _showImportDialog(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select directory",\
                self._dirLabel.text(), options)
        if directory:
            self._source = directory
            self._dirLabel.setText(directory)

if __name__ == "__main__":
    import sys

    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
    sys.exit()
