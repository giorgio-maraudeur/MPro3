import yt_dlp
from moviepy.editor import *
import os
import re

def sanitize_filename(filename):
    """Nettoie le nom du fichier en remplaçant les caractères invalides."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename) # Remplace les caractères invalides par "_"

def youtube_to_mp3(url, custom_title=None):
    """Télécharge l'audio d'une vidéo YouTube et le convertit en MP3."""
    desktop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Desktop") # expanduser("~") renvoie le chemin du répertoire personnel de l'utilisateur
    download_path = os.path.join(desktop_path, "YouTube Downloads") # Joint le chemin du bureau avec le nom du dossier "YouTube Downloads"
    os.makedirs(download_path, exist_ok=True) # Crée le dossier s'il n'existe pas

    temp_path = os.path.join(os.getcwd(), "temp_download") # Joint le répertoire de travail actuel avec le nom du dossier "temp_download"
    os.makedirs(temp_path, exist_ok=True) # Crée le dossier s'il n'existe pas

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': os.path.join(temp_path, '%(title)s.%(ext)s') # Chemin de sortie du fichier téléchargé
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
            info_dict = ydl.extract_info(url, download=True)
            original_title = info_dict.get('title', 'Titre inconnu')

            downloaded_file_path = ydl.prepare_filename(info_dict)

        if custom_title:
            safe_title = sanitize_filename(custom_title)
        else:
            safe_title = sanitize_filename(original_title)

        mp3_file = os.path.join(download_path, f"{safe_title}.mp3")

        audio_clip = AudioFileClip(downloaded_file_path)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()

        os.remove(downloaded_file_path)
        os.rmdir(temp_path)

        return original_title, f"Téléchargement terminé : {mp3_file}"

    except Exception as e:
        return f"Erreur : {e}"


def youtube_to_mp4(url, custom_title=None):
    """Télécharge une vidéo YouTube et la convertit en MP4."""
    desktop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Desktop")
    download_path = os.path.join(desktop_path, "YouTube Downloads")
    os.makedirs(download_path, exist_ok=True)

    temp_path = os.path.join(os.getcwd(), "temp_download")
    os.makedirs(temp_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': os.path.join(temp_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            original_title = info_dict.get('title', 'Titre inconnu')

            downloaded_file_path = ydl.prepare_filename(info_dict)

        if custom_title:
            safe_title = sanitize_filename(custom_title)
        else:
            safe_title = sanitize_filename(original_title)

        mp4_file = os.path.join(download_path, f"{safe_title}.mp4")

        video_clip = VideoFileClip(downloaded_file_path)
        video_clip.write_videofile(mp4_file)
        video_clip.close()

        os.remove(downloaded_file_path)
        os.rmdir(temp_path)

        return original_title, f"Téléchargement terminé : {mp4_file}"

    except Exception as e:
        return f"Erreur : {e}"
    

"""url = input("Enter the URL of the video or song: ")
custom_title = input("Enter a title of the mp4 file (leave empty if you want to keep the original title): ")

youtube_to_mp4(url, custom_title)"""
