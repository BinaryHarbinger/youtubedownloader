# YouTube Downloader

![image](https://raw.githubusercontent.com/BinaryHarbinger/youtubedownloader/main/preview.png)

A Python-based application for downloading YouTube videos and audio, built with **PyQt6** and **yt-dlp**. Designed for simplicity and speed, with a focus on cross-platform functionality.  

> ⚠️ yt-dlp and ffmpeg must be installed system wide in order to run program!

## Features

- Download YouTube videos and audio
- Simple and intuitive GUI with PyQt6
- Cross-platform support (Linux, macOS; Windows partial)
- Configurable download options

## Requirements

- Python 3.7+
- PyQt6
- yt-dlp

Install dependencies:

```bash
pip install -r requirements.txt
````

## Usage

1. Launch the application:

```bash
python main.py
```

2. Enter a YouTube URL.
3. Select download options (video/audio, resolution, format).
4. Click **Download** to start.

## Development

Clone the repository:

```bash
git clone https://github.com/BinaryHarbinger/youtubedownloader.git
cd youtubedownloader
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run for development:

```bash
python main.py
```

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Open a Pull Request

## License

This project is licensed under the **GPL-3.0 License**. See the [LICENSE](LICENSE) file for details.

