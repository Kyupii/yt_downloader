import sys
from PySide6.QtWidgets import  QLabel, QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QDialog, QFileDialog
from PySide6 import QtCore
from pytube import YouTube # I think these are our slowest imports...
import moviepy.editor as mp
import os
import re

class Form(QDialog):
    def __init__(self, parent=None):
        self.download_path = ''
        super(Form, self).__init__(parent)
        self.setWindowTitle("Youtube MP3 Downloader")
        # These add the widgets
        self.edit = QLineEdit("Youtube URL")
        self.dialog = QFileDialog(self)
        self.dialog.setFileMode(QFileDialog.Directory)
        self.dialog.setWindowTitle('Select Download Directory...')
        self.button = QPushButton('Download')
        self.opendia = QPushButton('Select Directory')
        # We them have to define the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.opendia)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)


        

        # Similar to a callback. we must CONNECT the signal to the method
        self.button.clicked.connect(self.download_callback)
        self.opendia.clicked.connect(self.opendia_callback)

    @QtCore.Slot()
    def on_finished(self) -> None:
        for path in self.dialog.selectedFiles():
            self.download_path = path
        print(self.download_path)
    def opendia_callback(self):
        self.dialog.open(self, QtCore.SLOT('on_finished()'))
    def download_callback(self):
        yt = YouTube(self.edit.text())
        yt.streams.filter(only_audio=True).first().download(output_path=self.download_path)
        for file in os.listdir(self.download_path):
            if re.search('mp4',file):
                mp4_path = os.path.join(self.download_path,file)
                mp3_path = os.path.join(self.download_path,file[:-4]+'.mp3')
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                os.remove(mp4_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = Form()
    form.show()

    sys.exit(app.exec())