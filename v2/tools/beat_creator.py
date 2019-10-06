from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QGridLayout
from PyQt5.QtGui import QIcon
import sys
import ntpath
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.withdraw()


timestamps = []

global audio_path

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Beat timestamp editor") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setText("Play")
        self.playButton.clicked.connect(self.play)

        #add timestamp
        self.add = QPushButton()
        self.add.setEnabled(False)
        self.add.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.add.setText("Add")
        self.add.clicked.connect(self.add_timestamp)
        #clear timestamps
        self.clear = QPushButton()
        self.clear.setEnabled(False)
        self.clear.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.clear.setText("Clear")
        self.clear.clicked.connect(self.clear_timestamps)

        #--------------------
        #timestamp list
        self.list = QLabel()
        self.list.setText("Timestamps: ")
        self.list.setWordWrap(True)

        #*------------------

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        #Create save action
        self.saveAction = QAction(QIcon('save.png'), '&Save', self)        
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save .txt file')
        self.saveAction.triggered.connect(self.saveFile)
        self.saveAction.setEnabled(False)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(exitAction)
        

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QGridLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton,0,0)
        controlLayout.addWidget(self.positionSlider,0,1)
        controlLayout.addWidget(self.add,1,0)
        controlLayout.addWidget(self.list,1,1,2,1)
        controlLayout.addWidget(self.clear,2,0)

        layout = QVBoxLayout()
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def saveFile(self):
    	global audio_path
    	path = audio_path
    	file = ntpath.basename(path)
    	text_file = open(file + " - data.txt", "w")
    	justgimmedata = sorted(timestamps, key=float)
    	for i in justgimmedata:
    		text_file.write(str(i) + "\n")
    	text_file.close()

    def clear_timestamps(self):
    	del timestamps[:]
    	self.clear.setEnabled(False)
    	output="Timestamps: "
    	self.list.setText(output)

    def add_timestamp(self):
    	print("timestamp added: ", self.mediaPlayer.position())
    	timestamps.append(self.mediaPlayer.position()/1000)
    	iwannadie = sorted(timestamps, key=float)
    	output="Timestamps: "+str(' '.join(str(iwannadie)))
    	self.list.setText(output)
    	self.clear.setEnabled(True)

    def openFile(self):
        fileName = filedialog.askopenfilename(filetypes=(("Audio Files", ".wav .mp3"),   ("All Files", "*.*")))

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))

            global audio_path
            audio_path = fileName

            self.playButton.setEnabled(True)
            self.add.setEnabled(True)

            self.saveAction.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setText("Play")
        else:
            self.mediaPlayer.play()
            self.playButton.setText("Pause")

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(690, 100)
    player.show()
    sys.exit(app.exec_())