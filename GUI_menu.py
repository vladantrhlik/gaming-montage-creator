from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon
import sys
import ntpath
import os
from tkinter import filedialog
import tkinter as tk
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from os import listdir
from os.path import isfile, join
from mutagen.mp3 import MP3

root = tk.Tk()
root.withdraw()


timestamps = []

global audio_path

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):


        self.setStyleSheet(qdarkgraystyle.load_stylesheet())

        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Insane gaming montage editr omguwuowo") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()
#---------------------------------------------------offset
        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setRange(0, 0)
        self.offset_slider.setEnabled(False)
        self.offset_slider.sliderMoved.connect(self.set_offset)
        

        self.offset_label = QLabel()
        self.offset_label.setText("Offset: 0s")
#---------------------------------------------------ostatni slidery uwu
        self.input_slider = QSlider(Qt.Horizontal)
        self.after_slider = QSlider(Qt.Horizontal)
        self.last_slider = QSlider(Qt.Horizontal)

        self.input_slider.setRange(-100,100)
        self.after_slider.setRange(0,100)
        self.last_slider.setRange(0,100)

        self.input_slider.setEnabled(True)
        self.after_slider.setEnabled(True)
        self.last_slider.setEnabled(True)

        self.input_slider.sliderMoved.connect(self.input_slider_input)
        self.after_slider.sliderMoved.connect(self.after_slider_input)
        self.last_slider.sliderMoved.connect(self.last_slider_input)

        self.input_label = QLabel()
        self.input_label.setText("Input delay (audio): 0s")
        self.after_label = QLabel()
        self.after_label.setText("Delay after clip: 0s")
        self.last_label = QLabel()
        self.last_label.setText("Delay after last clip: 0s")


        #output filename
        self.output_name = QLineEdit(self)
        self.output_label = QLabel()
        self.output_label.setText("Output file name (*.mp4):")

#---------------------------------------------------
        self.load_s = QPushButton()
        self.load_s.setEnabled(False)
        self.load_s.setText("Load sound")
        self.load_s.setEnabled(True)
        self.load_s.clicked.connect(self.load_song)
        self.load_s_label = QLabel()
        self.load_s_label.setText("-")
#---------------------------------------------------
        self.load_d = QPushButton()
        self.load_d.setEnabled(False)
        self.load_d.setText("Load data")
        self.load_d.setEnabled(True)
        self.load_d.clicked.connect(self.load_data)
        self.load_d_label = QLabel()
        self.load_d_label.setText("-")
#---------------------------------------------------
        self.load_c = QPushButton()
        self.load_c.setEnabled(False)
        self.load_c.setText("Load clips")
        self.load_c.setEnabled(True)
        self.load_c.clicked.connect(self.load_clips)
        self.load_c_label = QLabel()
        self.load_c_label.setText("-")
#---------------------------------------------------
        
        self.generate = QPushButton()
        self.generate.setEnabled(False)
        self.generate.setText("Generate montage")
        self.generate.clicked.connect(self.generate_montage)



        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QGridLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.load_s,1,0)
        controlLayout.addWidget(self.load_d,2,0)
        controlLayout.addWidget(self.load_c,3,0)

        controlLayout.addWidget(self.load_s_label,1,1)
        controlLayout.addWidget(self.load_d_label,2,1)
        controlLayout.addWidget(self.load_c_label,3,1)
        controlLayout.addWidget(self.generate,10,0)

        controlLayout.addWidget(self.offset_label,4,0)
        controlLayout.addWidget(self.offset_slider,4,1)

        controlLayout.addWidget(self.input_label,5,0)
        controlLayout.addWidget(self.input_slider,5,1)

        controlLayout.addWidget(self.after_label,6,0)
        controlLayout.addWidget(self.after_slider,6,1)

        controlLayout.addWidget(self.last_label,7,0)
        controlLayout.addWidget(self.last_slider,7,1)

        controlLayout.addWidget(self.output_name,8,1)
        controlLayout.addWidget(self.output_label,8,0)


        layout = QVBoxLayout()
        layout.addLayout(controlLayout)


        # Set widget to contain window contents
        wid.setLayout(layout)

    def input_slider_input(self):
        self.input_label.setText("Input delay (audio): " + str(self.input_slider.value()/100) + "s")
        print(str(self.output_name.text()))

    def last_slider_input(self):
        self.last_label.setText("Delay after last clip: " + str(self.last_slider.value()/10) +"s")

    def after_slider_input(self):
        self.after_label.setText("Delay after clip: " + str(self.after_slider.value()/10) +"s")
    
    def set_offset(self):
        #print(self.offset_slider.value())
        self.offset_label.setText("Offset: " + str(self.offset_slider.value()) + "s")


    def load_song(self):
        songName = filedialog.askopenfilename(filetypes=(("Audio Files", ".wav .mp3"),   ("All Files", "*.*")))
        self.load_s_label.setText(songName) 

        audio = MP3(songName)

        print(audio.info.length)

        self.offset_slider.setRange(0,audio.info.length)
        self.offset_slider.setEnabled(True)

        data_path = self.load_d_label.text()
        clips_path = self.load_c_label.text()
        output = self.output_name.text()
        if data_path != "-" and clips_path != "-" and output != None:
            self.generate.setEnabled(True)


    def load_data(self):
        dataName = filedialog.askopenfilename(filetypes=(("Text Files", ".txt"),   ("All Files", "*.*")))
        self.load_d_label.setText(dataName) 

        song_path = self.load_s_label.text()
        clips_path = self.load_c_label.text()
        output = self.output_name.text()
        if song_path != "-" and clips_path != "-" and output != None:
            self.generate.setEnabled(True)


    def load_clips(self):
        clipDirName = filedialog.askdirectory()
        self.load_c_label.setText(clipDirName)   

        song_path = self.load_s_label.text()
        data_path = self.load_d_label.text()
        output = self.output_name.text()
        if song_path != "-" and data_path != "-" and output != None:
            self.generate.setEnabled(True)

    def generate_montage(self):

        song_path = self.load_s_label.text()
        data_path = self.load_d_label.text()
        clip_path = self.load_c_label.text() + "/"

        print("generating")

        print(song_path)
        print(data_path)
        print(clip_path)

        paths = []
        shots = []

        if(len(str(self.output_name.text()))>0):
            output_video_path = self.output_name.text() + '.mp4'
        else:
            output_video_path = "output.mp4"
        

        start = self.offset_slider.value() #offset; must be higher than input_delay
        input_delay = self.input_slider.value()/100 #++ kdyz je hudba driv, -- kdyz je pozdeji

        #_---------------------------------------------------


        delay = start-input_delay #o kolik sekund je posunuty audio
        position = start


        beats_in = open(data_path).readlines()
        beats = [float(i) for i in beats_in]

        after_delay = self.after_slider.value()/10
        last_delay = self.last_slider.value()/10

        fdin = 2
        fdout = 2


        paths_in = [f for f in listdir(clip_path) if isfile(join(clip_path, f))]
        number_of_clips = len(paths_in)

        print("Loading all clips...")

        for i in range(len(paths_in)):
            paths.append(0)
            shots.append(0)
            for j in range(len(paths_in)):  
                order = int(paths_in[j].partition("_")[0])
                
                if(int(order) == i+1):
                    paths[i] = clip_path + paths_in[j]
                    #print(len(str(order)))
                    shots[i] = paths_in[j][len(str(order))+1:]
                    shots[i] = int(shots[i].partition(".")[0])/1000
        print("Loaded clips:")
        for i in paths: print(i)
        print("Timestamps of clips:")
        for i in shots: print(i)

        print("Cutting clips...")
        for i in range(number_of_clips):
            paths.append("clips/"+str(i+1)+".mp4")

        print("shots[0] = ",shots[0]+delay)
        print("beats[0] = ",beats[0])


        if shots[0]+delay < beats[0]:
            print("Error: First shot (", shots[0]+delay ,") is earlier than first beat (",beats[0],")") 
            print("Tip: Increase start offset") 
            exit()




        clips = []



        for i in range(number_of_clips):

            length_of_clip = beats[i]+after_delay-position
            start = shots[i]+after_delay-length_of_clip

            shot=start+length_of_clip-after_delay
            print(length_of_clip)

            if i == number_of_clips-1:
                #making last frame a bit longer
                clips.append(VideoFileClip(paths[i]).subclip(start,start+length_of_clip+last_delay))
            else:
                clips.append(VideoFileClip(paths[i]).subclip(start,start+length_of_clip))
            
            position+=length_of_clip

        clips[0] = clips[0].fx(vfx.fadein, duration=fdin, initial_color=[0,0,0])
        clips[number_of_clips-1] = clips[number_of_clips-1].fx(vfx.fadeout, duration=fdout, final_color=[0,0,0])


        audioclip = AudioFileClip(song_path).subclip(delay,beats[number_of_clips-1]+last_delay).audio_fadein(2)

        final_clip = concatenate_videoclips(clips).set_audio(audioclip)
        final_clip = final_clip.afx( afx.audio_fadein, 0)
        final_clip = final_clip.afx( afx.audio_fadeout, 2)


        final_clip.write_videofile(output_video_path, audio_codec='aac')








if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(200,200)
    player.show()
    sys.exit(app.exec_())
