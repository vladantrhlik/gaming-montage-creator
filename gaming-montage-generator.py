from PyQt5.QtCore import QDir, Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QAudioProbe
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QLineEdit, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QSpinBox, QTabWidget, QListWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QGridLayout
from PyQt5.QtGui import QIcon, QCursor
from PyQt5 import QtCore
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import sys
import os
import subprocess
import glob
import ntpath
from tkinter import filedialog
import tkinter as tk
from os import listdir
from os.path import isfile, join
import math
import time
from mutagen.mp3 import MP3
import random

root = tk.Tk()
root.withdraw()

frameRate = 60

clips = []
clipTimemstamps = []
clipOrder = []

audioPath = ""

audioTimestamps = []
audioDelayedT = []

global deleting
deleting = 0          

global user_in
user_in = True          


global lastSelectedAT
lastSelectedAT = 0



class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

            #ffcc01

        self.color = 0

        self.stylesheet = """

        QLineEdit{
            background: #272727;
            color: #e3c800;
            border: 2px solid #e3c800;
            padding: 5px;
        }

        QScrollBar:vertical{
            background: #272727;
            border: 2px solid #e3c800;
            border-right: none;
            border-top: none;
        }

        QScrollBar::handle:vertical{
            background: #e3c800;
            border: 2px solid #e3c800;
            border-right: none
        }

        QScrollBar:horizontal{
            background: #272727;
            border: 2px solid #e3c800;
            border-bottom: none;
            border-left: none;
        }

        QScrollBar::handle:horizontal{
            background: #e3c800;
            border: 2px solid #e3c800;
            border-bottom: none
        }

        




        QScrollBar::add-line{
            background: transparent;
            border: none;
        }
        QScrollBar::sub-line{
            background: transparent;
            border: none;
        }


        QMainWindow::separator:hover {
            background: #e3c800;
        }



        QListWidget{
            background: #272727;
            color: #e3c800;
            border: 2px solid #e3c800;
            border-radius: 0px;
        }

        QListWidget::item{
            padding: 1px 0px;
        }

        QListWidget::item:selected {
            background: #e3c800;
            color: #272727;
        }

        QSpinBox{
            background: #272727;
            color: #e3c800;
            border-radius: 0px;
            border: 2px solid #e3c800;
            padding: 3px 2px;
            width: 100px;
            
        }

        QSpinBox:disabled{
            background: #737373;
            color: #555555;
            border: 2px solid #737373;
        }

        QSpinBox::up-button{
            background: transparent;
        }
        QSpinBox::up-arrow{
            color: transparent;
        }
        QSpinBox::down-button{
            background: transparent;
        }
        QSpinBox::down-arrow{
            color: transparent;
        }

        QMediaPlayer{
            border-width: 0px; 
            border-style: solid
        }

        QSlider::groove:horizontal {
            border: 2px solid #e3c800;
            height: 10px;
            background: #272727;
            border-radius: 0px;
            margin: 10px 0px;

            }
        QSlider::handle:horizontal {
            background-color: #e3c800;
            border: 3px solid #e3c800;
            height: 30px;
            width: 10px;

            }

        QPushButton{
            background-color: #e3c800;
            color: #272727;
            border-radius: 0px;
            padding: 5 10;
            width: 100px;
            height: 20px;
            font: bold;
        }



        QPushButton:pressed{
            background-color: #272727;
            color: #e3c800;
            border: 3px solid #e3c800;
        }

        QPushButton:disabled{
            background: #737373;
            color: #555555
        }

        QTabWidget::pane { /* The tab widget frame */
            border-top: 3px solid #e3c800;
            margin: 5px 2px;

        }

        QTabBar::tab{
            background: #272727;
            border: 2px solid #e3c800;
            padding: 5px 10px;
            height: 20px;
            border-radius:0px; 
            margin-right: 5px;
            font: bold;
            color: #e3c800;
            width: 100px;
        }

        QTabBar::tab:selected{
            background: #e3c800;
            border: 2px solid #e3c800;
            color: #272727;

        }

    



        QMainWindow{
            background-color: #272727;
        }


        QSlider{
            color: #FDD036;
        }

        QLabel{
            font: bold;
            color: #e3c008;
        }



        """

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkTimestamp)
        self.timer.start(1)


        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.audioPlayer = QMediaPlayer(None)

        videoWidget = QVideoWidget()
        audioWidget = QVideoWidget()

        #WIDGETS

        
        #CONTROL PANEL
        #audio control
        self.loadAudio = QPushButton()
        self.loadAudio.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.loadAudio.setEnabled(True)
        self.loadAudio.setText("Load audio")
        self.loadAudio.clicked.connect(self.loadAudioFile)

        self.audioPlayButton = QPushButton()
        self.audioPlayButton.setEnabled(False)
        '''self.audioPlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))'''
        self.audioPlayButton.setText("Play")
        self.audioPlayButton.clicked.connect(self.audioPlay)
        self.audioPlayButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.audioPositionSlider = QSlider(Qt.Horizontal)
        self.audioPositionSlider.setRange(0, 0)
        self.audioPositionSlider.sliderMoved.connect(self.audioSetPosition)

        self.audioLabel = QLabel()
        self.audioLabel.setText("...")

        self.addAudioTimestamp = QPushButton()
        self.addAudioTimestamp.setText("Add timestamp")
        self.addAudioTimestamp.setEnabled(False)
        self.addAudioTimestamp.clicked.connect(self.addAT)
        self.addAudioTimestamp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.posLabel = QLabel()
        self.posLabel.setText("-/-")
        self.posLabel.setAlignment(Qt.AlignCenter)

        self.audioTList = QListWidget()
        self.audioTList.itemClicked.connect(self.changeTimestamp)

        self.dltAT = QPushButton()
        self.dltAT.setText("Delete timestamp")
        self.dltAT.clicked.connect(self.deleteAT)
        self.dltAT.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.dltAT.setEnabled(False)

        self.changeAT = QSlider(Qt.Horizontal)
        self.changeAT.setMinimum(-100)
        self.changeAT.setMaximum(100)
        self.changeAT.sliderMoved.connect(self.changeInputDelay)

        self.inputDelay = QLabel()
        self.inputDelay.setText("Input delay: 0ms")
        self.inputDelay.setAlignment(Qt.AlignCenter)

        self.TDelayLbl = QLabel()
        self.TDelayLbl.setText("Change timestamp:")

        self.TDelay = QSpinBox()
        self.TDelay.setEnabled(True)
        self.TDelay.setMinimum(0)
        self.TDelay.setMaximum(99999)  #'xd'
        self.TDelay.valueChanged.connect(self.changeTDelay)

        self.visualizer = QPushButton()
        self.visualizer.setEnabled(True)
        self.visualizer.setObjectName("vizz")
        self.visualizer.setStyleSheet("""
                    
                    #vizz{
                        background: #272727;
                        color: white;
                        border-radius: 0;
                        border: 2px solid #e3c800;
                    }
                    """)


        #video control
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        '''self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))'''
        self.playButton.setText("Play")
        self.playButton.clicked.connect(self.play)
        self.playButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.forward = QPushButton()
        self.forward.setEnabled(False)
        '''self.forward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))'''
        self.forward.setText(">")
        self.forward.setToolTip("Next frame")
        self.forward.clicked.connect(self.f)
        self.forward.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.backward = QPushButton()
        self.backward.setEnabled(False)
        '''self.backward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))'''
        self.backward.setText("<")
        self.backward.setToolTip("Previous frame")
        self.backward.clicked.connect(self.b)
        self.backward.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        #delete clip from list
        self.deleteClip = QPushButton()
        self.deleteClip.setEnabled(False)
        self.deleteClip.setText("Delete")
        self.deleteClip.clicked.connect(self.dltClip)
        self.deleteClip.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        #timestamp
        self.addT = QPushButton()
        self.addT.setEnabled(False)
        '''self.addT.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))'''
        self.addT.setText("+")
        self.addT.setToolTip("Add timestamp")
        self.addT.clicked.connect(self.addTimestamp)
        self.addT.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.timestamp = QSlider(Qt.Horizontal)
        self.timestamp.setRange(0, 0)
        self.timestamp.setToolTip("Position of timestamp")
        self.timestamp.sliderMoved.connect(self.setTimestamp)
        self.timestamp.setEnabled(False)

        #order of clip
        self.order = QSpinBox()
        self.order.setMinimum(1)
        self.order.setValue(1)
        self.order.setEnabled(False)

        self.lbl = QLabel()
        self.lbl.setText("Order:")
        self.lbl.setAlignment(Qt.AlignCenter)

        #ADDING CLIPS
        self.clipList = QListWidget()
        self.clipList.itemClicked.connect(self.changeClip)

        self.addClip = QPushButton()
        self.addClip.setEnabled(True)
        self.addClip.clicked.connect(self.openFile)
        self.addClip.setText("Add clip")
        self.addClip.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.addFolder = QPushButton()
        self.addFolder.setEnabled(True)
        self.addFolder.clicked.connect(self.openFolder)
        self.addFolder.setText("Add folder")
        self.addFolder.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        #GENERATE TAB
        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setRange(0, 0)
        self.offset_slider.setEnabled(False)
        self.offset_slider.sliderMoved.connect(self.set_offset)
        

        self.offset_label = QLabel()
        self.offset_label.setText("Offset: 0s")


        self.after_slider = QSlider(Qt.Horizontal)
        self.last_slider = QSlider(Qt.Horizontal)

        self.after_slider.setRange(0,100)
        self.last_slider.setRange(0,100)

        self.after_slider.setEnabled(True)
        self.last_slider.setEnabled(True)

        self.after_slider.sliderMoved.connect(self.after_slider_input)
        self.last_slider.sliderMoved.connect(self.last_slider_input)

        self.input_label = QLabel()
        self.input_label.setText("Input delay (audio): 0s")
        self.after_label = QLabel()
        self.after_label.setText("Delay after clip: 0s")
        self.last_label = QLabel()
        self.last_label.setText("Delay after last clip: 0s")

        self.output_name = QLineEdit(self)
        self.output_label = QLabel()
        self.output_label.setText("Output file name (*.mp4):")

        self.generateBut = QPushButton()
        self.generateBut.clicked.connect(self.generate)
        self.generateBut.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.generateBut.setText("Generate")


        #TOP BAR
        openAction = QAction(QIcon('open.png'), '&Open Project', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open project')
        openAction.triggered.connect(self.openProject)

        saveAction = QAction(QIcon('save.png'), '&Save Project', self)        
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save project')
        saveAction.triggered.connect(self.saveProject)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        
        wid = QWidget(self)
        self.setCentralWidget(wid)


        self.randomAudioLabel = QLabel()

        #generate tab layout
        generatorTabLayout = QGridLayout()
        generatorTabLayout.setContentsMargins(5, 5, 5, 5)

        generatorTabLayout.addWidget(self.offset_label,0,0)
        generatorTabLayout.addWidget(self.offset_slider,0,1)

        generatorTabLayout.addWidget(self.after_label,2,0)
        generatorTabLayout.addWidget(self.last_label,3,0)

        generatorTabLayout.addWidget(self.after_slider,2,1)
        generatorTabLayout.addWidget(self.last_slider,3,1)

        generatorTabLayout.addWidget(self.output_label,4,0)
        generatorTabLayout.addWidget(self.output_name,4,1)

        generatorTabLayout.addWidget(self.generateBut,5,0,1,2)


        #VIDEO LAYOUT
        videoTabLayout = QGridLayout()
        videoTabLayout.setContentsMargins(5, 5, 5, 5)
        #video controls
        videoTabLayout.addWidget(self.playButton,2,3)
        videoTabLayout.addWidget(self.forward,2,4)
        videoTabLayout.addWidget(self.backward,2,2)
        videoTabLayout.addWidget(self.positionSlider,1,2,1,3)
        #clip menu
        videoTabLayout.addWidget(self.clipList,1,0,4,2)
        videoTabLayout.addWidget(self.addClip,5,0)
        videoTabLayout.addWidget(self.addFolder,5,1)
        videoTabLayout.addWidget(self.deleteClip,6,0)
        #timestamps
        videoTabLayout.addWidget(self.addT,4,2)
        videoTabLayout.addWidget(self.timestamp,3,2,1,3)
        #order
        videoTabLayout.addWidget(self.lbl,4,3)
        videoTabLayout.addWidget(self.order,4,4)
        

        videoTabLayout.addWidget(videoWidget,0,0,1,5)

        #AUDIO LAYOUT
        self.audioTabLayout = QGridLayout()
        self.audioTabLayout.setContentsMargins(5, 5, 5, 5)

        self.audioTabLayout.addWidget(audioWidget,100,0)
        self.audioTabLayout.addWidget(self.loadAudio,0,0,1,2)
        self.audioTabLayout.addWidget(self.audioLabel,0,2,1,2)
        self.audioTabLayout.addWidget(self.audioPlayButton,2,0,1,2)
        self.audioTabLayout.addWidget(self.audioPositionSlider,1,0,1,3)
        self.audioTabLayout.addWidget(self.addAudioTimestamp,4,2,1,1)
        self.audioTabLayout.addWidget(self.posLabel,2,2)
        self.audioTabLayout.addWidget(self.audioTList,4,0,5,2)
        self.audioTabLayout.addWidget(self.dltAT,5,2)
        self.audioTabLayout.addWidget(self.changeAT,3,2)
        self.audioTabLayout.addWidget(self.inputDelay,3,0,1,2)
        self.audioTabLayout.addWidget(self.TDelayLbl,6,2)
        self.audioTabLayout.addWidget(self.TDelay,7,2)
        self.audioTabLayout.addWidget(self.visualizer,8,2)

        



        layout = QVBoxLayout()

        tabs = QTabWidget()
        videoTab = QWidget()
        audioTab = QWidget()
        generateTab = QWidget()

        videoTab.layout = QVBoxLayout()
        audioTab.layout = QVBoxLayout()
        generateTab.layout = QVBoxLayout()
        
        videoTab.setLayout(videoTabLayout)
        audioTab.setLayout(self.audioTabLayout)
        generateTab.setLayout(generatorTabLayout)
        
        tabs.addTab(videoTab, "Video")
        tabs.addTab(audioTab, "Audio")
        tabs.addTab(generateTab, "Generate")

        layout.addWidget(tabs)
        wid.setLayout(layout)

        app.setStyleSheet(self.stylesheet)



        '''
       
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(videoTabLayout)

        wid.setLayout(layout)

'''



        self.mediaPlayer.setVideoOutput(videoWidget)
        '''self.audioPlayer.setVideoOutput(audioWidget)'''

        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.audioPlayer.stateChanged.connect(self.audioStateChanged)

        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.audioPlayer.positionChanged.connect(self.audioPositionChanged)

        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.audioPlayer.durationChanged.connect(self.audioDurationChanged)


        self.mediaPlayer.error.connect(self.handleError)
        self.clipList.currentItemChanged.connect(self.updateClipInfo)
        self.order.valueChanged.connect(self.setOrder)


    def saveProject(self):
        print("saving project")


        '''
        Structure:
            audiopath
            audioT
            clipPaths
            clipT
            clipOrder
            startDel
            inputDel
            afterDel
            lasDel
        '''


        text2save = ""

        #adding audio data
        text2save += str(self.randomAudioLabel.text())+"\n"
        for i in audioTimestamps:
            text2save += str(i)+", "
        text2save+= "\n"
        #adding clip data
        for i in clips:
            text2save += str(i)+", "
        text2save+= "\n"
        for i in clipTimemstamps:
            text2save += str(i)+", "
        text2save+= "\n"
        for i in clipOrder:
            text2save += str(i)+", "
        text2save+= "\n"

        output_video_path = self.output_name.text()+".mp4"

        start = self.offset_slider.value() #offset; must be higher than input_delay
        input_delay = self.changeAT.value() #++ kdyz je hudba driv, -- kdyz je pozdeji
        after_delay = self.after_slider.value()
        last_delay = self.last_slider.value()

        text2save+= str(start)+"\n"
        text2save+= str(input_delay)+"\n"
        text2save+= str(after_delay)+"\n"
        text2save+= str(last_delay)+"\n"

        fileOut = filedialog.asksaveasfile(mode='w', defaultextension=".gmg")
        fileOut.write(text2save)
        fileOut.close()


    def openProject(self):
        print("opening project")
        fileName = filedialog.askopenfilename(filetypes=(("Gaming montage generator", ".gmg"),   ("All Files", "*.*")))
        file = open(fileName, "r") 
        data = file.readlines()
        '''
        Structure:
            audiopath
            audioT
            clipPaths
            clipT
            clipOrder
        '''
        #loading audio file
        fileName = data[0].partition("\n")[0]
        if fileName != '':
                #audio stuff
            self.audioPlayer.setMedia(
                        QMediaContent(QUrl.fromLocalFile(fileName)))
            self.audioPlayButton.setEnabled(True)
            self.audioLabel.setText(os.path.basename(fileName))
            self.addAudioTimestamp.setEnabled(True)
            self.randomAudioLabel.setText(fileName)
            audio = MP3(fileName)
            self.offset_slider.setRange(0,audio.info.length)
            self.offset_slider.setEnabled(True)
            self.TDelay.setMaximum(audio.info.length*1000)

        #load audio timestamps
        audioT = data[1].split(", ")
        audioT.remove(audioT[len(audioT)-1])

        for i in audioT:
            print("timestamp added",i)
            audioTimestamps.append(int(i))
            audioTimestamps.sort()

        for j in audioTimestamps:
            print(j)
            #(calcandupdate()) doesnt work lol
        audioDelayedT = []
        val = self.changeAT.value()*10

        for i in range(0,len(audioTimestamps)):
            audioDelayedT.append(audioTimestamps[i]+val)

        audioDelayedT.sort()

        self.audioTList.clear()

        for i in audioDelayedT:
            self.audioTList.addItem(str(i))
        #adding clips, timestamps and order
        clipPaths = data[2].split(", ")
        clipPaths.remove(clipPaths[len(clipPaths)-1])

        clipT = data[3].split(", ")
        clipT.remove(clipT[len(clipT)-1])

        clipO = data[4].split(", ")
        clipO.remove(clipO[len(clipO)-1])

        for i in range(len(clipPaths)):


            clips.append(clipPaths[i])
            clipTimemstamps.append(int(clipT[i]))
            clipOrder.append(int(clipO[i]))

            print("clipInfo: " + clipPaths[i] + ", " + clipT[i] + ", " + clipO[i])
            
        self.clipList.clear()
        for i in clips:
            self.clipList.addItem(ntpath.basename(i))

        self.enableAll()
        #other stuff (delay)
        self.offset_slider.setValue(int(data[5])) #offset; must be higher than input_delay
        self.changeAT.setValue(int(data[6])) #++ kdyz je hudba driv, -- kdyz je pozdeji
        self.after_slider.setValue(int(data[7]))
        self.last_slider.setValue(int(data[8]))

        self.last_label.setText("Delay after last clip: " + str(self.last_slider.value()/10) +"s")
        self.after_label.setText("Delay after clip: " + str(self.after_slider.value()/10) +"s")
        self.offset_label.setText("Offset: " + str(self.offset_slider.value()) + "s")
        self.inputDelay.setText("Input delay: "+str(val)+"ms")
#------------------------------------------------------------

    def checkTimestamp(self):

        pos = self.audioPlayer.position()
        #print(pos)

        string = 0
        for i in audioDelayedT:
            string+=i
       
        val = self.changeAT.value()*10

        for i in audioTimestamps:

            space = 5
            changed = False

            if pos-space<i+val and pos+space>i+val:
                print("timestamp")

                if self.color==0:
                    self.visualizer.setStyleSheet("""
                    
                    #vizz{
                        background: #e3c800;
                        color: white;
                        border-radius: 0;
                        border: 2px solid #e3c800;
                    }
                    """)
                    self.color = 1
                else:
                    self.visualizer.setStyleSheet("""
                    
                    #vizz{
                        background: #272727;
                        color: white;
                        border-radius: 0;
                        border: 2px solid #e3c800;
                    }
                    """)

                    self.color = 0

                break;
                time.sleep(0.01)


    def last_slider_input(self):
        self.last_label.setText("Delay after last clip: " + str(self.last_slider.value()/10) +"s")

    def after_slider_input(self):
        self.after_label.setText("Delay after clip: " + str(self.after_slider.value()/10) +"s")
    
    def set_offset(self):
        #print(self.offset_slider.value())
        self.offset_label.setText("Offset: " + str(self.offset_slider.value()) + "s")


    def generate(self):
        print("generating...")
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #loading and ordering data
        global clips
        orderedClips = [x for _,x in sorted(zip(clipOrder,clips))]
        orderedClipTimestamps = [x for _,x in sorted(zip(clipOrder,clipTimemstamps))]

        for i in range(len(orderedClipTimestamps)):
            orderedClipTimestamps[i] = orderedClipTimestamps[i]/1000
            

        calculatedAudioTimestamp = []
        for i in audioTimestamps:
            calculatedAudioTimestamp.append((i+self.changeAT.value())/1000)

        output_video_path = self.output_name.text()+".mp4"
        start = self.offset_slider.value() #offset; must be higher than input_delay
        input_delay = self.changeAT.value()/100 #++ kdyz je hudba driv, -- kdyz je pozdeji
        after_delay = self.after_slider.value()/10
        last_delay = self.last_slider.value()/10

        song_path = self.randomAudioLabel.text()

        if orderedClipTimestamps[0] > calculatedAudioTimestamp[0]:
            print("setting offset automatically")
            start = orderedClipTimestamps[0]-calculatedAudioTimestamp[0]



        delay = start-input_delay
        position = start

        beats = calculatedAudioTimestamp
        paths = orderedClips
        shots = orderedClipTimestamps

        print(beats)
        print(paths)
        print(shots)

        fdin = 2
        fdout = 2

        number_of_clips = len(clips)

        if shots[0] > beats[0]:
            print("setting offset automatically")
            start = shots[0]-beats[0]

        output_clips = []

        for i in range(number_of_clips):
            length_of_clip = abs(beats[i]+after_delay-position)
            start = abs(shots[i]+after_delay-length_of_clip)

            shot=abs(start+length_of_clip-after_delay)
            print(length_of_clip)

            if i == number_of_clips-1:
                #making last frame a bit longer
                output_clips.append(VideoFileClip(paths[i]).subclip(start,start+length_of_clip+last_delay))
            else:
                output_clips.append(VideoFileClip(paths[i]).subclip(start,start+length_of_clip))
            print("("+str(start)+", "+str(start+length_of_clip)+")")
            
            position+=length_of_clip

        output_clips[0] = output_clips[0].fx(vfx.fadein, duration=fdin, initial_color=[0,0,0])
        output_clips[number_of_clips-1] = output_clips[number_of_clips-1].fx(vfx.fadeout, duration=fdout, final_color=[0,0,0])


        audioclip = AudioFileClip(song_path).subclip(delay,beats[number_of_clips-1]+last_delay).audio_fadein(2)

        final_clip = concatenate_videoclips(output_clips).set_audio(audioclip)
        final_clip = final_clip.afx( afx.audio_fadein, 0)
        final_clip = final_clip.afx( afx.audio_fadeout, 2)


        final_clip.write_videofile(output_video_path, audio_codec='aac', codec = "libx264")



        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def changeTDelay(self):
        val = self.TDelay.value()
        self.TDelayLbl.setText("Change timestamp:")
        pos = self.audioTList.currentRow()
        global lastSelectedAT

        if(pos>-1):

            
            lastSelectedAT = pos
            #audioTimestamps[pos] = val
            self.calcAndUpdate()
        else:
            pos = lastSelectedAT
            audioTimestamps[pos] = val
            self.calcAndUpdate()


    def changeInputDelay(self):
        val = self.changeAT.value()*10
        self.inputDelay.setText("Input delay: "+str(val)+"ms")
        print(val)
        self.calcAndUpdate()

    def calcAndUpdate(self):
        audioDelayedT = []
        val = self.changeAT.value()*10

        for i in range(0,len(audioTimestamps)):
            audioDelayedT.append(audioTimestamps[i]+val)

        audioDelayedT.sort()

        self.audioTList.clear()

        for i in audioDelayedT:
            self.audioTList.addItem(str(i))
       
            

    def deleteAT(self):
        print("dltAT")
        num = self.audioTList.currentRow()
        global lastSelectedAT
        del audioTimestamps[lastSelectedAT]

        self.calcAndUpdate()
        
        self.dltAT.setEnabled(False)

    def changeTimestamp(self):
        self.dltAT.setEnabled(True)
        pos = self.audioTList.currentRow()
        
        self.TDelayLbl.setText("Change timestamp:")
        val = self.changeAT.value()*10

        print("value ",str(audioTimestamps[pos]+val))
        self.TDelay.setValue(audioTimestamps[pos]+val)
        



    def addAT(self):
        pos = self.audioPlayer.position()
        print("timestamp added",pos)
        audioTimestamps.append(pos)
        audioTimestamps.sort()

        for i in audioTimestamps:
            print(i)

        self.calcAndUpdate()


    def audioSetPosition(self, position):
        self.audioPlayer.setPosition(position)

    def audioPlay(self):
        if self.audioPlayer.state() == QMediaPlayer.PlayingState:
            self.audioPlayer.pause()
        else:
            self.audioPlayer.play()

    def audioStateChanged(self, state):
        if self.audioPlayer.state() == QMediaPlayer.PlayingState:
            self.audioPlayButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.audioPlayButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def audioPositionChanged(self, position):
        #print(self.audioPlayer.position())
        self.audioPositionSlider.setValue(position)
        self.posLabel.setText(str(self.audioPlayer.position())+" / "+str(self.audioPlayer.duration()))

    def audioDurationChanged(self, duration):
        self.audioPositionSlider.setRange(0, duration)

    def loadAudioFile(self):
        fileName = filedialog.askopenfilename(filetypes=(("Audio Files", ".wav .mp3"),   ("All Files", "*.*")))



        if fileName != '':
            self.audioPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.audioPlayButton.setEnabled(True)
            self.audioLabel.setText(os.path.basename(fileName))
            self.addAudioTimestamp.setEnabled(True)
            self.randomAudioLabel.setText(fileName)
            audio = MP3(fileName)
            self.offset_slider.setRange(0,audio.info.length)
            self.offset_slider.setEnabled(True)
            self.TDelay.setMaximum(audio.info.length*1000)
            

    def printData(self):
        print('data:')
        for i in range(0,len(clips)):
            print(clips[i], clipOrder[i], clipTimemstamps[i])

    def setOrder(self):
        num = self.clipList.currentRow()
        clipOrder[num] = self.order.value()

        global user_in

        if (user_in):
            self.clipList.insertItem(num,str(str(clipOrder[num])+".  "+ntpath.basename(clips[num])))
            self.clipList.takeItem(num+1)

            self.clipList.setCurrentRow(num)

        
        user_in = True
        


    def updateClipInfo(self):

        global user_in
        user_in = False

        num = self.clipList.currentRow()
        self.timestamp.setValue(clipTimemstamps[num])
        self.order.setValue(clipOrder[num])

    def enableAll(self):
        self.playButton.setEnabled(True)
        self.deleteClip.setEnabled(True)
        '''self.timestamp.setEnabled(True)'''
        self.forward.setEnabled(True)
        self.backward.setEnabled(True)
        self.order.setEnabled(True)
        self.addT.setEnabled(True)

    def b(self):
        if self.mediaPlayer.position() >= 1000/frameRate:
            self.mediaPlayer.setPosition(self.mediaPlayer.position()-(1000/frameRate))

    def f(self):
        if self.mediaPlayer.position() <= self.mediaPlayer.duration()-(1000/frameRate):
            self.mediaPlayer.setPosition(self.mediaPlayer.position()+(1000/frameRate))

    def addTimestamp(self):
        num = self.clipList.currentRow()
        pos = self.mediaPlayer.position()
        print('add')
        self.timestamp.setValue(pos)
        clipTimemstamps[num] = pos

    def setTimestamp(self):
        print('set')

    def dltClip(self):
        num = self.clipList.currentRow()
        clips.remove(clips[num])
        clipOrder.remove(clipOrder[num])
        clipTimemstamps.remove(clipTimemstamps[num])
        self.updateClipList()
        self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile('')))

    def openFolder(self):
        clipDirName = filedialog.askdirectory()

        if clipDirName != '':
            paths_in = [f for f in listdir(clipDirName) if isfile(join(clipDirName, f))]
            for i in range(0,len(paths_in)):
                print(clipDirName+'/'+paths_in[i])
                clips.append(clipDirName+'/'+paths_in[i])
                clipTimemstamps.append(0)
                clipOrder.append(i+1)
            self.updateClipList()
            self.enableAll()
            

    def changeClip(self,item):
        global clips
        print("number of clips: "+str(len(clips)))
        num = self.clipList.currentRow()
        print(num)
        self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(clips[num])))
        

    def updateClipList(self):
        self.clipList.clear()
        for i in range(len(clips)):
            self.clipList.addItem(str(str(clipOrder[i])+".  "+ntpath.basename(clips[i])))

    def openFile(self):
        fileName = filedialog.askopenfilename(filetypes=(("Video Files", ".mp4"),   ("All Files", "*.*")))


        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            clips.append(fileName)
            clipTimemstamps.append(0)
            clipOrder.append(0)
            self.enableAll()
            self.updateClipList()

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")

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
    player = Window()
    player.resize(640, 480)
    player.show()


    sys.exit(app.exec_())