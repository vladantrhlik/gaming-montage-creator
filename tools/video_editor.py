from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QSpinBox)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QGridLayout
from PyQt5.QtGui import QIcon
import sys
import os
import glob
import ntpath
from tkinter import filedialog
import tkinter as tk

frameRate = 60
global path

root = tk.Tk()
root.withdraw()

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video timestamp editor") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        #add timestamp button
        self.add_t = QPushButton()
        self.add_t.setEnabled(False)
        self.add_t.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))
        self.add_t.setToolTip("Add timestamp")
        self.add_t.clicked.connect(self.add)

        #timestamp slider
        self.timestamp = QSlider(Qt.Horizontal)
        self.timestamp.setRange(0, 0)
        self.timestamp.setToolTip("Position of timestamp")
        self.timestamp.sliderMoved.connect(self.set_timestamp)


        #video control buttons
        self.forward = QPushButton()
        self.forward.setEnabled(False)
        self.forward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forward.setToolTip("Next frame")
        self.forward.clicked.connect(self.f)

        self.backward = QPushButton()
        self.backward.setEnabled(False)
        self.backward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backward.setToolTip("Previous frame")
        self.backward.clicked.connect(self.b)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setToolTip("Play/Pause")
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setToolTip("Position slider")
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        #order of clip
        self.order = QSpinBox()
        self.order.setMinimum(1)
        self.order.setValue(1)
        self.order.setEnabled(False)

        self.lbl = QLabel()
        self.lbl.setText("Order:")
        self.lbl.setAlignment(Qt.AlignCenter)

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
        self.saveAction.setEnabled(False)     
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save clip with timestamp')
        self.saveAction.triggered.connect(self.saveCall)


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
        controlLayout.addWidget(self.backward,0,0)
        controlLayout.addWidget(self.playButton,0,1)
        controlLayout.addWidget(self.forward,0,2)
        controlLayout.addWidget(self.add_t,0,4)
        controlLayout.addWidget(self.positionSlider,1,0,1,3)
        controlLayout.addWidget(self.timestamp,1,4,1,3)
        controlLayout.addWidget(self.order,0,6)
        controlLayout.addWidget(self.lbl,0,5)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def saveCall(self):
    	global path
    	file = ntpath.basename(path)
    	path = os.path.dirname(path)
    	os.rename(path+"/"+file, path+"/"+str(self.order.value())+"_"+str(self.timestamp.value())+".mp4")
    	print("saved")

    def b(self):
    	print("backward")
    	if self.mediaPlayer.position() >= 1000/frameRate:
    		self.mediaPlayer.setPosition(self.mediaPlayer.position()-(1000/frameRate))

    def f(self):
    	print("forward")
    	if self.mediaPlayer.position() <= self.mediaPlayer.duration()-(1000/frameRate):
    		self.mediaPlayer.setPosition(self.mediaPlayer.position()+(1000/frameRate))


    def add(self, position):
       	print("added timestamp")
       	self.timestamp.setValue(self.positionSlider.value())

    def set_timestamp(self):
    	print("timestamp sat")

    def openFile(self):
        fileName = filedialog.askopenfilename(filetypes=(("Video Files", ".mp4"),   ("All Files", "*.*")))

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))

            global path
            path = fileName

            self.playButton.setEnabled(True)
            self.add_t.setEnabled(True)
            self.forward.setEnabled(True)
            self.backward.setEnabled(True)
            self.saveAction.setEnabled(True)
            self.order.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

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
        self.timestamp.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())