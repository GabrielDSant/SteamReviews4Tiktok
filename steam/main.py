import json
import os
import requests
import voice, video, steam_reviews
from pathlib import Path
import argparse

def main():
    # Fetching posts from r/AskReddit


    # Path("/steam/backgrounds").mkdir(exist_ok=True)
    Path("/steam/render").mkdir(exist_ok=True)
    
    if len(os.listdir("/steam/backgrounds")) == 0:
        raise Exception("Please move a background video to backgrounds/ folder")


    parser = argparse.ArgumentParser(description="Process Steam AppId and generate video")
    parser.add_argument("appid", type=str, help="The AppId of the Steam game")
    args = parser.parse_args()  # Analisa os argumentos fornecidos na CLI

    appid = args.appid  # Obtém o valor do argumento `appid`
    print(f"⏱ Processing post: {appid}")

    # Make sure we have not already rendered/uploaded post
    if appid in os.listdir('/steam/render'):
        print("❌ Post already processed!")



    # setup 
    folder_path = f"/steam/assets/{appid}"
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    # getting cover and game name
    print("Fetching game name and downloading cover")
    response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    game_data = response.json().get(str(appid))
    if game_data:
        game_name = game_data["data"]["name"]
        cover_art_url = game_data["data"]["header_image"]
        # Download cover art
        cover_art_path = f"/steam/assets/{appid}/intro.png"
        with open(cover_art_path, 'wb') as cover_art_file:
            cover_art_file.write(requests.get(cover_art_url).content)
    else:
        print("❌ Error Fetching gamedata, make sure the appid is correct")
        return

    #Scraping the post, screenshotting, etc
    print("📸 Screenshotting post...")
    steam_reviews.download_funny_steam_reviews(app_id=appid, thread_title=game_name)


    # # Generate TTS clips for each comment
    print("\n📢 Generating voice clips...",end="",flush=True)
    json_file = open(f"/steam/assets/{appid}/review_data.json", 'r')
    dictList = json.load(json_file)

    # generating audio 
    
    intro = {
        "thread_id": "570",
        "thread_title": game_name,
        "intro": True,
        "comments": [{
            "comment_body": game_name,
            "screenshot_path": f"/steam/assets/{appid}/intro.png",
            "thread_id": "570",
            "thread_title": "steam"
        }
        ]
    }
   
    audio_length = voice.makeTTS(intro)
    audio_length += voice.makeTTS(dictList)

    # # Render & Upload
    print("\n🎥 Rendering video...")
    video.render(dictList, appid, game_name)

if __name__ == '__main__':
    main()