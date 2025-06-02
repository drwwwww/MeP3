import tkinter as tk
import traceback
from tkinter import messagebox
import ffmpeg
import pytubefix
from pytubefix import YouTube
import moviepy
import os
import re
import sys


def cleanup_temp_log(temp_log):
    try:
        temp_log.close()
        os.remove(temp_log.name)
    except Exception as e:
        print(f"Failed to delete temp log: {e}")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def garbageCollection(url):
    url.delete(0, tk.END) 
    url.insert(0, "default value")

def resource_path(relative_path):
    try:
        base_path = os.sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def convert(url_link):
    print(f"Trying to convert: {url_link}")
    print("Theme path:", resource_path("themes/red.json"))
    print("FFmpeg path:", resource_path("ffmpeg_bin/ffmpeg.exe"))
    print("Icon path:", resource_path("icon.ico"))
    print("Image path:", resource_path("M.png"))

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    if not url_link or "youtube.com" not in url_link:
        messagebox.showerror("Invalid URL", "Please enter a valid YouTube link.")
        return
    
    try:
        yt = YouTube(url_link)
        stream = yt.streams.filter(only_audio=True).first()
        
        if stream is None:
            raise Exception("No audio streams available for this video.")

        downloaded_file = stream.download(output_path=downloads_path)

        if not downloaded_file or not os.path.exists(downloaded_file):
            raise Exception("Failed to download the audio file.")

        try:
            clip = moviepy.AudioFileClip(downloaded_file)
            safe_title = sanitize_filename(yt.title)
            output_path = os.path.join(downloads_path, safe_title + ".mp3")
            print(f"Saving to: {output_path}")
            clip.write_audiofile(output_path)
            clip.close()

        except Exception as e:
            messagebox.showerror("Conversion Failed", traceback.format_exc())
            return

        os.remove(downloaded_file)
        messagebox.showinfo("Download Complete", "Your Download is Finished")
    except Exception as e:
        messagebox.showerror("Conversion Failed", str(e))