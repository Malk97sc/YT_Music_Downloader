import threading
from pytubefix import Playlist
from ytmd.downloader.playlist import downloadPlaylist

def progress(completed, total):
    print(f"\rDownloaded {completed}/{total}", end="", flush=True)

def print_banner():
    banner = r"""
    ╔══════════════════════════════════════╗
    ║        YT Music Downloader           ║
    ║            CLI Mode                  ║
    ║          Malak Sanchez               ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    url = input("Playlist URL: ").strip()
    if not url:
        print("Invalid URL")
        return

    cancel_event = threading.Event()

    try:
        pl = Playlist(url)
        playlist_name = pl.title if pl.title else "MyPlaylist"
    except Exception:
        playlist_name = "MyPlaylist"

    try:
        downloadPlaylist(
            url=url,
            progress_callback = progress,
            cancel_event = cancel_event,
            playlist_name = playlist_name
        )
        print(f"The playlist '{playlist_name}' has been successfully downloaded.")
    except KeyboardInterrupt:
        cancel_event.set()
        print("\nCanceled by user.")
