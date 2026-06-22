import yt_dlp
import traceback

url = "https://www.youtube.com/watch?v=tav0XtpFN4A&list=RDMMtav0XtpFN4A&start_radio=1"
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

print("Starting yt-dlp test...")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        print("Success! Title:", info.get('title'))
except Exception as e:
    print("Error during download:")
    traceback.print_exc()
