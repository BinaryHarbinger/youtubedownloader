

import os
import subprocess
from typing import Optional


video_URL = ""
if os.name == "nt":
    homepath = os.path.expanduser(os.getenv('USERPROFILE'))

def download_file(video_url: str, 
                 custom_output_dir: Optional[str] = None,
                 output_dir_s: str = "~/Music",
                 output_dir_v: str = "~/Videos",
                 archive_file_s: str = "archive_sound.txt",
                 archive_file_v: str = "archive_video.txt",
                 file_format: str = "sound",
                 redownload_file: bool = False) -> None:
    """
    Download a video or audio file from YouTube.
    
    Args:
        video_url: YouTube video URL
        custom_output_dir: Custom download directory (optional)
        output_dir_s: Default audio files directory
        output_dir_v: Default video files directory
        archive_file_s: Audio archive file location
        archive_file_v: Video archive file location
        file_format: Download format ("Sound" or "Video")
        redownload_file: Re-download previously downloaded files
    """
    # Expand all paths
    output_dir_s = os.path.expanduser(output_dir_s)
    output_dir_v = os.path.expanduser(output_dir_v)

    # Keep archive files in script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    archive_file_s = os.path.join(current_dir, archive_file_s)
    archive_file_v = os.path.join(current_dir, archive_file_v)

    # Use custom directory if provided, otherwise use default
    if custom_output_dir:
        output_dir = os.path.expanduser(custom_output_dir)
    else:
        output_dir = output_dir_s if file_format == "Sound" else output_dir_v

    # Create directory if it doesn't exist
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except PermissionError:
        raise Exception(f"Permission denied: Cannot create directory {output_dir}")

    # Initialize base command
    command = ["yt-dlp"]
    
    if file_format == "Sound":
        command.extend([
            "-x",                    # Extract audio
            "--audio-format", "m4a", # Convert to m4a format
            "-f", "bestaudio",       # Select best audio quality
        ])
    else:  # Video
        command.extend([
            "-f", "bestvideo+bestaudio", # Select best video and audio quality
        ])

    # Common parameters
    command.extend([
        "--embed-metadata",   # Embed metadata
        "--embed-thumbnail",  # Embed thumbnail
        "--add-metadata",     # Add additional metadata
        "--yes-playlist",     # Enable playlist support
        "--no-post-overwrites", # Don't process if file exists
        "-o", os.path.join(output_dir, "%(playlist)s", "%(title)s.%(ext)s").replace("\\", "/"), # Output format
    ])

    # Archive file handling
    if not redownload_file:
        archive_file = archive_file_s if file_format == "Sound" else archive_file_v
        try:
            # Create or check archive file
            archive_dir = os.path.dirname(archive_file)
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)
            if not os.path.exists(archive_file):
                open(archive_file, 'a').close()
            command.extend(["--download-archive", archive_file])
        except PermissionError:
            print(f"Warning: Cannot create archive file {archive_file}. Continuing without archive.")

    # Add video URL
    command.append(video_url)

    # Execute download command
    try:
        subprocess.run(command, check=True)
        print(f"Download successful: {video_url}")
        print(f"Files saved to: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        raise

if __name__ == "__main__":
    video_url = video_URL
    download_file(video_url)
