from moviepy.editor import *
import random,os
import PIL
import time

resolution = (1080,1920)

def render(data, appid, game_name):

    path = f"./assets/{appid}/"

    # Load all the clips
# Display cover art for 5 seconds
    image_clips = []
    sound_clips = []
    intro_sound = AudioFileClip(path + "intro.mp3")
    intro = ImageClip(path + 'intro.png').set_duration(intro_sound.duration).fx(vfx.resize,width=resolution[0]*0.9).set_position(("center","center")) 
    sound_clips.append(intro_sound)
    image_clips.append(intro)
    duration = sound_clips[-1].duration
    for dict in data['comments']:
        sound_clips.append(AudioFileClip(dict["screenshot_path"].replace(".png", ".mp3")))
        image_clips.append(ImageClip(dict["screenshot_path"]).set_duration(sound_clips[-1].duration).fx(vfx.resize,width=resolution[0]*0.9).set_position(("center","center")))

        duration += sound_clips[-1].duration
        # Ensure length of video
        time.sleep(5)
        if duration > 90:
            break

    # Combine all the clips into one
    image_clips = concatenate_videoclips(image_clips).set_position(("center","center"))
    sound_clips = concatenate_audioclips(sound_clips)



    # 3 minute limit
    if sound_clips.duration > 60*2.9:
        return False

    #Loading background
    background_clip = "backgrounds/" + random.choice(os.listdir("backgrounds"))
    background = VideoFileClip(background_clip).loop(n=None).set_duration(sound_clips.duration).resize((resolution[0],resolution[1]), PIL.Image.LANCZOS) 

    # Overlaying background
    final = CompositeVideoClip([background, image_clips]).set_audio(sound_clips)

    # Save video
    os.mkdir(f'/resultados/steam/{game_name}')
    final.write_videofile(f"/resultados/steam/{game_name}/{appid}.mp4", fps=24, threads=8, preset='ultrafast', audio_codec='aac', remove_temp=True)

    return True