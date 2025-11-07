import subprocess
from pathlib import Path
from typing import Optional

def download_file(
    video_url: str,
    custom_output_dir: Optional[str] = None,
    archive_file_s: str = "archive_sound.txt",
    file_format: str = "sound",
    redownload_file: bool = False
) -> None:
    """Download audio or video from YouTube with embedded metadata and thumbnail."""

    file_format = file_format.lower()

    # Choose default output folder based on file type
    home = Path.home()
    if "music" in file_format or "sound" in file_format:
        default_dir = home / "Music"
    else:
        default_dir = home / "Videos"

    # Use custom directory if provided
    output_dir = Path(custom_output_dir).expanduser() if custom_output_dir else default_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Archive file setup
    archive_file = Path(__file__).resolve().parent / archive_file_s
    if not redownload_file and not archive_file.exists():
        archive_file.touch()

    # Determine file extension
    if "m4a" in file_format:
        file_ext = "m4a"
    elif "opus" in file_format:
        file_ext = "opus"
    else:
        file_ext = "m4a"

    # Output file pattern for yt-dlp
    output_pattern = str(output_dir / "%(playlist)s" / "%(title)s.%(ext)s")

    # yt-dlp command setup
    if "music" in file_format or "sound" in file_format:
        cmd = [
            "yt-dlp", "-x",
            "--audio-format", file_ext,
            "-f", "bestaudio",
            "--embed-thumbnail", "--embed-metadata", "--add-metadata",
            "--yes-playlist", "--no-post-overwrites",
            "-o", output_pattern,
            video_url
        ]
    else:
        cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio",
            "--embed-thumbnail", "--embed-metadata", "--add-metadata",
            "--yes-playlist", "--no-post-overwrites",
            "-o", output_pattern,
            video_url
        ]

    # Add archive option if redownload is not requested
    if not redownload_file:
        cmd.extend(["--download-archive", str(archive_file)])

    subprocess.run(cmd, check=True)
    print(f"Download completed: {video_url}")
    print(f"Saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    download_file("https://www.youtube.com/watch?v=dQw4w9WgXcQ", file_format="video")

