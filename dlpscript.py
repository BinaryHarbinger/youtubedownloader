#!/usr/bin/env python3

import os
import subprocess


video_URL= ""

def download_file(video_url, output_dir_s="~/Music",output_dir_v="~/Videos", archive_file_s="~/.yt-dlp-archive_s",archive_file_v="~/.yt-dlp-archive_v",file_format="sound"):
    
    # Çıkış klasörünü genişlet
    archive_file_v = os.path.expanduser(archive_file_v)
    archive_file_s = os.path.expanduser(archive_file_s)

    if file_format == "Sound":

        output_dir = os.path.expanduser(output_dir_s)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        command = [
            "yt-dlp",
            "-x",  # Sadece sesi indir
            "--audio-format", "m4a",  # Formatı m4a yap
            "--embed-metadata",  # Metadata dosyaya göm
            "--embed-thumbnail",  # Kapak fotoğrafını göm
            "--add-metadata",  # Ek metadata ekle
            "--yes-playlist",  # Playlist için destek
            "--download-archive", archive_file_s,  # Daha önce indirilenleri kaydet
            "--no-post-overwrites",  # Eğer dosya varsa yeniden işlem yapma
            "-o", f"{output_dir_s}/%(playlist)s/%(title)s.%(ext)s",  # Playlist adıyla klasör oluştur
            "-f", "bestaudio",  # En yüksek kaliteli ses formatını seç
            video_url
        ]
    elif file_format == "Video":

        output_dir = os.path.expanduser(output_dir_v)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


        command = [
                    "yt-dlp",
                    "--embed-metadata",  # Metadata dosyaya göm
                    "--embed-thumbnail",  # Kapak fotoğrafını göm
                    "--add-metadata",  # Ek metadata ekle
                    "--yes-playlist",  # Playlist için destek
                    "--download-archive", archive_file_v,  # Daha önce indirilenleri kaydet
                    "--no-post-overwrites",  # Eğer dosya varsa yeniden işlem yapma
                    "-o", f"{output_dir}/%(playlist)s/%(title)s.%(ext)s",  # Playlist adıyla klasör oluştur
                    "-f", "bestvideo+bestaudio",  # En yüksek video ve ses formatlarını seç
                    video_url
                ]



    # Run download command
    try:
        subprocess.run(command, check=True)
        print(f"Download successful: {video_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Kullanıcıdan URL al
    video_url = video_URL
    download_file(video_url)
