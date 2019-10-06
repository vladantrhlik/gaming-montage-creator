from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from os import listdir
from os.path import isfile, join

paths = []
shots = []

#_---------------------------------------------------

song_path = "audio/RUDE - Eternal Youth.mp3"
data_path = "data/RUDE - Eternal Youth.mp3 - data.txt"
clip_path = "clips/mc/"

output_video_path = 'test.mp4'

start = 3.81 #offset; must be higher than input_delay
input_delay = 0.0 #++ kdyz je hudba driv, -- kdyz je pozdeji

#_---------------------------------------------------


delay = start-input_delay #o kolik sekund je posunuty audio
position = start


beats_in = open(data_path).readlines()
beats = [float(i) for i in beats_in]

after_delay = 0.2
last_delay = 2

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


print("shots:")
print(shots)
print("beats:")
print(beats_i)
print("paths:")
print(paths)




if shots[0]+delay < beats[0]:
	print("Error: First shot (", shots[0]+delay ,") is earlier than first beat (",beats[0],")") 
	print("Tip: Increase start offset") 
	exit()




clips = []

'''

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
'''