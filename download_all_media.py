import os
import urllib.request

audio_files = [
    "ding.ogg",
    "playerfight.ogg",
    "playerdamaged.ogg",
    "sansspeak.ogg",
    "gasterblaster.ogg",
    "bonestab.ogg",
    "warning.ogg",
    "heartshatter.ogg",
    "gasterblast.ogg",
    "flash.ogg",
    "slam.ogg",
    "menuselect.ogg",
    "heartsplit.ogg",
    "menucursor.ogg",
    "battletext.ogg",
    "playerheal.ogg",
    "gasterblast2.ogg",
    "mus_zz_megalovania.ogg",
    "gameover.ogg"
]

base_url = "https://sans-simulator.github.io/c2-sans-fight/media/"
media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")

if not os.path.exists(media_dir):
    os.makedirs(media_dir)
    print(f"Created directory: {media_dir}")

for file_name in audio_files:
    dest_path = os.path.join(media_dir, file_name)
    if os.path.exists(dest_path):
        print(f"File {file_name} already exists. Skipping.")
        continue
        
    url = base_url + file_name
    print(f"Downloading {file_name} from {url}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Successfully downloaded {file_name}")
    except Exception as e:
        print(f"Failed to download {file_name}: {e}")

print("Audio download process finished.")
