from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *

pocet_klipu = 16

paths = []

for i in range(pocet_klipu):
	paths.append("clips/"+str(i+1)+".mp4")


#song_path = "atlas - eulogy.mp3"
#beats = [12.283, 13.722, 15.185, 16.718, 18.227]

#song_path = "Macky Gee - Lighters Up.mp3"
#beats = [67.662,71.795,74.558,77.322,80.038]

song_path = "Geoxor - Euphoria.mp3"
#beats = [37.356,39.492,41.674,43.880,45.993,48.176,52.611,54.817,56.953,59.136,61.295,63.501,65.614,67.843,70.072,72.209,74.438,76.597,78.803,80.963,83.145,85.374,87.487]
beats = [8.986, 13.281, 17.693, 26.447, 35.131, 43.862, 52.593, 56.981, 61.323, 63.576, 67.871, 70.031, 74.466, 78.738, 83.173, 87.492,92]
#17,35,52
shots = [9.77,9.77,12.55,9.1,11.5,8.4,11,9.87,11.55,10.39,10.45,10.78,15,11.825,9.6,11.8,7.2]

after_delay = 1

input_delay = 0.35 #++ kdyz je hudba driv, -- kdyz je pozdeji
delay = 0.36-input_delay #o kolik sekund je posunuty audio
position = 0.36


output_video_path = 'test.mp4'

clips = []



for i in range(pocet_klipu):

	delka = beats[i]+after_delay-position
	zacatek = shots[i]+after_delay-delka

	shot=zacatek+delka-after_delay
	print(delka)

	clips.append(VideoFileClip(paths[i]).subclip(zacatek,zacatek+delka))
	position+=delka


audioclip = AudioFileClip(song_path).subclip(delay,beats[pocet_klipu-1]+after_delay)



final_clip = concatenate_videoclips(clips).set_audio(audioclip)

final_clip.write_videofile(output_video_path, audio_codec='aac')
#final_clip.preview()