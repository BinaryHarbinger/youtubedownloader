
import os
import subprocess
from typing import Optional

def download_file(video_url: str, 
                  custom_output_dir: Optional[str] = None,
                  output_dir_s: str = "~/Music",
                  archive_file_s: str = "archive_sound.txt",
                  file_format: str = "sound",
                  redownload_file: bool = False) -> None:
    """
    Download audio or video from YouTube with 1:1 cropped cover embedded.
    Handles playlists or single videos (NA folder for singles).
    """

    # Expand paths
    output_dir_s = os.path.expanduser(output_dir_s)
    if custom_output_dir:
        output_dir = os.path.expanduser(custom_output_dir)
    else:
        output_dir = output_dir_s

    os.makedirs(output_dir, exist_ok=True)

    # Archive file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    archive_file_s = os.path.join(current_dir, archive_file_s)
    if not redownload_file:
        if not os.path.exists(archive_file_s):
            open(archive_file_s, 'a').close()

    if file_format.lower() == "sound":
        # Download thumbnail using PPA
        thumb_cmd = [
            "yt-dlp",
            "--ppa",
            "--write-thumbnail",
            "--convert-thumbnails", "jpg",
            "--skip-download",
            "-o", os.path.join(output_dir, "%(playlist)s", "%(title)s.%(ext)s"),
            video_url
        ]
        subprocess.run(thumb_cmd, check=True)

        # Crop thumbnail to square
        for root, _, files in os.walk(output_dir):
            for f in files:
                if f.endswith(".jpg"):
                    full_path = os.path.join(root, f)
                    tmp_path = os.path.join(root, "_"+f)
                    subprocess.run([
                        "ffmpeg", "-y", "-i", full_path,
                        "-vf", "crop='if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'",
                        tmp_path
                    ], check=True)
                    os.replace(tmp_path, full_path)

        # Download audio and embed metadata & thumbnail
        audio_cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "opus",
            "-f", "bestaudio",
            "--embed-thumbnail",
            "--embed-metadata",
            "--add-metadata",
            "--yes-playlist",
            "--no-post-overwrites",
            "-o", os.path.join(output_dir, "%(playlist)s", "%(title)s.%(ext)s"),
            video_url
        ]
        if not redownload_file:
            audio_cmd.extend(["--download-archive", archive_file_s])

        subprocess.run(audio_cmd, check=True)
        print(f"Audio download completed: {video_url}")

    else:
        # Video download with thumbnail and metadata embed
        video_cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio",
            "--embed-thumbnail",
            "--embed-metadata",
            "--add-metadata",
            "--yes-playlist",
            "--no-post-overwrites",
            "-o", os.path.join(output_dir, "%(playlist)s", "%(title)s.%(ext)s"),
            video_url
        ]
        if not redownload_file:
            video_cmd.extend(["--download-archive", archive_file_s])
        
        subprocess.run(video_cmd, check=True)
        print(f"Video download completed: {video_url}")


if __name__ == "__main__":
    download_file(video_URL)

