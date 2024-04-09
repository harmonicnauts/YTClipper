# YTClipper

YTClipper is a simple and small fun project of mine that uses ffmpeg, yt-dlp, and streamlit to simple tool built with Streamlit that allows you to download and cut fragments of YouTube videos.

![Screenshot](assets/Screenshot%202024-04-09%20142115.png)

## Features

- Download YouTube videos
- Cut fragments of downloaded videos
- Generate embed element for YouTube videos

## Setup

1. Clone the repository:

```bash
git clone https://github.com/harmonicnauts/YTClipper.git
```

2. Install the required dependencies:

pip install -r requirements.txt

3. Download the `yt-dlp.exe`(if you want to use the latest version) and `ffmpeg` executables. The `yt-dlp.exe` can be placed inside the ./app/ folder.

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Enter the YouTube video URL in the provided input box.

3. Set the start and end time for the fragment you want to cut. Optionally, click the "Generate Embed" button to generate an embed code for the YouTube video so that you can find the timestamp you want to clip.

4. Click the "Download and Cut" button to download the video and cut the fragment.
