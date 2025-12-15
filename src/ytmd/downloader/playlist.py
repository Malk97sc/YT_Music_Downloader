from pytubefix import Playlist, YouTube
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

import os

from mutagen.mp4 import MP4, MP4Cover
from ytmd.utils.files import sanitize_filename

def downloadPlaylist(url, progress_callback, cancel_event, playlist_name, num_wk=4):
    pl = Playlist(url)
    total = len(pl.videos)
    completed = 0

    base_dir = os.path.join("Songs", sanitize_filename(playlist_name))
    os.makedirs(base_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=num_wk) as executor:
        futures = [
            executor.submit(
                download_single_video,
                video,
                base_dir,
                playlist_name,
                cancel_event
            )
            for video in pl.videos
        ]

        for future in as_completed(futures):
            if cancel_event.is_set():
                for f in futures:
                    f.cancel()
                break

            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")

            completed += 1
            progress_callback(completed, total)

def download_single_video(video, base_dir, playlist_name, cancel_event):
    if cancel_event.is_set():
        return "canceled"

    yt = YouTube(video.watch_url)

    title = sanitize_filename(yt.title)
    #print(f"Downloading {title}")
    artist = sanitize_filename(yt.author) if yt.author else "Unknown"
    thumbnail_url = yt.thumbnail_url

    stream = yt.streams.get_audio_only()
    if stream is None:
        raise RuntimeError("No audio stream found")

    filename = f"{title}.m4a"
    filepath = os.path.join(base_dir, filename)

    if os.path.exists(filepath):
        return "skipped"

    if cancel_event.is_set():
        return "canceled"

    stream.download(output_path=base_dir, filename=filename)

    img_data = None
    try:
        r = requests.get(thumbnail_url, timeout=10)
        img_data = r.content
    except Exception as e:
        print(f"Thumbnail error: {e}")

    audiofile = MP4(filepath)
    audiofile["\xa9nam"] = title
    audiofile["\xa9ART"] = artist
    audiofile["\xa9alb"] = playlist_name

    if img_data:
        audiofile["covr"] = [MP4Cover(img_data, MP4Cover.FORMAT_JPEG)]

    audiofile.save()
    return "downloaded"
