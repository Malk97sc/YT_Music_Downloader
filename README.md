# YT Music Downloader

A desktop application to download audio from a YouTube playlists and automatically embed metadata. The project supports CLI and GUI modes, was designed to download the music using *pytubefix* and a integration using thread pools.

> **Current support:** Linux only (tested on Ubuntu-based systems). Windows/macOS support and standalone binaries will be added later.

## Features

- Download audio-only streams from YouTube playlists
- Output format: M4A (AAC)
- Automatic metadata:
  - Title
  - Artist
  - Album
  - Cover video thumbnail
- Parallel downloads using thread pools
- Cancelable downloads
- Two execution modes:
  - **CLI** (terminal)
  - **GUI** (desktop app using Flet)

## Project Structure

```bash
YT-Music-Downloader/
├── src/
│    ├── ytmd/
│    │    ├── downloader/
│    │    ├── interfaces/
│    │    ├── utils/
│    │    ├── app.py
│    │    └── __init__.py
│    └── __init__.py
├── pyproject.toml
├── .gitignore
└── README.md
```

## System dependencies

Need a Python 3.12+ version. The GUI relies on `mpv` through Flet, which requires the following system libraries:

```bash
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
```

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:Malk97sc/YT_Music_Downloader.git
cd YT_Music_Downloader
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv ytVenv
source ytVenv/bin/activate
```

### 3. Install the package

```bash
pip install .
```

## Usage

After installation, the command `ytmd` becomes available system-wide inside the virtual environment.

### CLI mode

```bash
ytmd --cli
```

You will be prompted to enter a YouTube playlist URL:

```text
Playlist URL: <URL_link>
```

### GUI mode

```bash
ytmd --gui
```

This launches the desktop interface where you can:
- Paste a playlist URL
- Cancel downloads at any time

## Output

Downloaded files are saved in:

```bash
YT_Music_Downloader/Songs/<Playlist Name>/
```

- The application downloads audio-only streams, not MP3.  
- M4A is chosen to preserve original quality and metadata support.
- Playlist downloads are parallelized for better performance.

Each track is saved as:

- Format: `.m4a`
- Metadata: embedded using `mutagen`


## Note

This project is intended for educational and personal use only. Please respect YouTube’s Terms of Service and copyright laws in your jurisdiction.