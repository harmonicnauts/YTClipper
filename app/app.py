import streamlit as st
import subprocess, os, re, requests


# file/folder paths
YTDLP_PATH = os.path.join(os.getcwd(), "./app/yt-dlp.exe")
FFMPEG_PATH = "ffmpeg"
VIDEO_FOLDER_PATH = os.path.join(os.getcwd(), "./",  "videos/")
DOWNLOADED_VIDEO_FILE_PATH = os.path.join(VIDEO_FOLDER_PATH, "video.webm")

# check if the URL is a valid YouTube video URL
def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return re.match(youtube_regex, url)

# check if the YouTube video exists or not privated
def is_youtube_video_exist(video_url):
    try:
        response = requests.head(video_url)
        return response.status_code == 200
    except:
        return False

# download the video using yt-dlp
def download_video(video_url, start_time, end_time):
    try:
        if is_youtube_url(video_url):
            if is_youtube_video_exist(video_url):
                if os.path.exists(DOWNLOADED_VIDEO_FILE_PATH):
                    os.remove(DOWNLOADED_VIDEO_FILE_PATH)
                command = [YTDLP_PATH, video_url, "--downloader", "ffmpeg", "--downloader-args", f"ffmpeg_i:-ss {start_time} -to {end_time}", "-o", DOWNLOADED_VIDEO_FILE_PATH, "--progress", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                with st.spinner('Downloading the video...'):
                    while True:
                        line = process.stdout.readline()
                        print(line)
                        if not line:
                            break
                st.success("Video downloaded successfully!")
                return True
            else:
                st.error("YouTube video does not exist or maybe have been privated.")
        else:
            st.error("Invalid YouTube video URL.")
    except Exception as e:
        st.error(f"An error occurred during video download: {str(e)}")
    return False

# cut fragments using ffmpeg
# def cut_fragment(start_time, end_time, video_id):
#     try:
#         output_placeholder = st.empty()
#         error_placeholder = st.empty()

#         if os.path.exists(DOWNLOADED_VIDEO_FILE_PATH):
#             output_file = os.path.join(VIDEO_FOLDER_PATH, f"video-{start_time}-{end_time}-{video_id}.mp4")
#             command = [FFMPEG_PATH, "-ss", str(start_time), "-t", str(end_time - start_time), "-i", DOWNLOADED_VIDEO_FILE_PATH, "-y", "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_file]
#             process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             while True:
#                 output = process.stdout.readline().decode().strip()
#                 error = process.stderr.readline().decode().strip()
#                 if not output and not error:
#                     break
#                 if output:
#                     output_placeholder.text("ffmpeg Output: " + output)
#                 if error:
#                     error_placeholder.error("ffmpeg Errors: " + error)
#         else:
#             st.error("Download the video first before cutting.")
#     except Exception as e:
#         st.error(f"An error occurred during video cutting: {str(e)}")

def main():
    st.title("YTClipper")
    st.write("This is a small fun project where you can pass the URL into a box and set the start and end time to clip a video!")
    st.markdown("<font color='red'>Note:</font> This program will use your internet to download the  video onto your device.", unsafe_allow_html=True)
    video_url = st.text_input("Enter YouTube Video URL:")
    embed_div_placeholder = st.empty()
    embed_button_placeholder = st.empty()
    start_time = st.number_input("Enter Start Time (in seconds):", min_value=0.0, step=0.1)
    end_time = st.number_input("Enter End Time (in seconds):", min_value=0.0, step=0.1)

    if st.button("Download"):
        try:
            download_video(video_url, start_time, end_time)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    if embed_button_placeholder.button("Generate Embed"):
        if is_youtube_url(video_url):
            video_id = video_url.split('=')[-1]
            if is_youtube_video_exist(video_url):
                embed_div_placeholder.write(f'<iframe width="560" height="315" src=https://www.youtube.com/embed/{video_id} frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
            else:
                st.error("YouTube video does not exist.")
        else:
            st.error("Invalid YouTube video URL.")

    st.markdown("#### Convert Video Timestamp to Seconds")
    st.markdown("This may feel clunky because in streamlit it always refreshes the page :(")

    time_stamp = st.text_input("Enter Video Timestamp HH MM SS (Split with spaces)")
    if st.button("Convert to Seconds"):
        try:
            h, m, s = map(int, time_stamp.split(' '))
            total_seconds = h * 3600 + m * 60 + s
            st.success(f"The timestamp '{time_stamp}' is equivalent to {total_seconds} seconds.")
        except ValueError:
            st.error("Invalid timestamp format. Please use the format HH:MM:SS.")

if __name__ == "__main__":
    main()