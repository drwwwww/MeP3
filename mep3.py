import traceback
from tkinter import messagebox
import sys
import tempfile
import atexit

temp_log = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
sys.stdout = temp_log
sys.stderr = temp_log

atexit.register(lambda: log.cleanup_temp_log(temp_log))


try:
    import customtkinter as ctk
    import ffmpeg
    import pytubefix
    import moviepy
    import log
    import os
    from PIL import Image, ImageTk

    ffmpeg_path = log.resource_path("ffmpeg_bin/ffmpeg.exe")
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    print("FFmpeg path:", ffmpeg_path)
    print("FFmpeg exists?", os.path.exists(ffmpeg_path))
    print("FFMPEG_BINARY env var:", os.environ.get("FFMPEG_BINARY"))



    theme_path = log.resource_path("themes/red.json")

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme(theme_path)

    root = ctk.CTk()
    (root.iconbitmap(log.resource_path("icon.ico")))

    root.title("MeP3")
    root.geometry("700x400")
    root.resizable(False, False)

    image = Image.open(log.resource_path("M.png"))
    image = image.resize((100, 100))
    logo = ImageTk.PhotoImage(image)

    logolabel = ctk.CTkLabel(master=root, image=logo, text="")
    logolabel.place(relx=0.5, rely=0.2, anchor="center")

    title = ctk.CTkLabel(root, 
                        text="MeP3 | Youtube to MP3 Converter", 
                        font=("Arial", 16, "bold")).place(relx=0.5, rely=0.3, anchor="center")

    url_entry = ctk.CTkEntry(root, width=250)
    url_entry.place(relx=0.5, rely=0.5, anchor="center")

    convert = ctk.CTkButton(root, text="Convert Link", command=lambda: log.convert(url_entry.get())).place(relx=0.5, rely=0.6, anchor="center")

    def on_close():
        log.cleanup_temp_log(temp_log)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

except  Exception as e:
    messagebox.showerror("App Crash", f"Something went wrong:\n\n{e}\n\n{traceback.format_exc()}")