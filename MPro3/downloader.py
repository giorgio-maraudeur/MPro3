import yt_dlp
from moviepy import *
import os
import re
import time

def sanitize_filename(filename):
    """Nettoie le nom du fichier en remplaçant les caractères invalides."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def youtube_to_mp3(url, custom_title=None, update_progress=None):
    """Télécharge l'audio d'une vidéo YouTube et le convertit en MP3."""
    desktop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    download_path = os.path.join(desktop_path, "YouTube Downloads")
    os.makedirs(download_path, exist_ok=True)

    temp_path = os.path.join(os.getcwd(), "temp_download")
    os.makedirs(temp_path, exist_ok=True)

    def progress_hook(d):
        """Mise à jour de la barre de progression pendant le téléchargement."""
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', None)

            if total:
                percent = (downloaded / total) * 80 + 10
                if update_progress:
                    update_progress(percent)
                time.sleep(0.1)

    if update_progress:
        update_progress(5)
        time.sleep(0.5)
        update_progress(10)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': False,
        'progress_hooks': [progress_hook],
        'outtmpl': os.path.join(temp_path, '%(title)s.%(ext)s')
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            original_title = info_dict.get('title', 'Titre inconnu')
            downloaded_file_path = ydl.prepare_filename(info_dict)

        safe_title = sanitize_filename(custom_title if custom_title else original_title)
        mp3_file = os.path.join(download_path, f"{safe_title}.mp3")

        if update_progress:
            update_progress(95)

        audio_clip = AudioFileClip(downloaded_file_path)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()

        os.remove(downloaded_file_path)
        os.rmdir(temp_path)

        if update_progress:
            update_progress(100)

        return original_title, f"Téléchargement terminé : {mp3_file}"

    except Exception as e:
        return None, f"Erreur : {e}"

def youtube_to_mp4(url, custom_title=None, update_progress=None):
    """Télécharge une vidéo YouTube et la convertit en MP4."""
    desktop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    download_path = os.path.join(desktop_path, "YouTube Downloads")
    os.makedirs(download_path, exist_ok=True)

    temp_path = os.path.join(os.getcwd(), "temp_download")
    os.makedirs(temp_path, exist_ok=True)

    def progress_hook(d):
        """Mise à jour de la barre de progression pendant le téléchargement."""
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', None)

            if total:
                percent = (downloaded / total) * 100
                if update_progress:
                    update_progress(percent)
                time.sleep(0.1)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'progress_hooks': [progress_hook],
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

        safe_title = sanitize_filename(custom_title if custom_title else original_title)
        mp4_file = os.path.join(download_path, f"{safe_title}.mp4")

        # Vérification de l'écriture de la vidéo
        if os.path.exists(downloaded_file_path):
            video_clip = VideoFileClip(downloaded_file_path)
            video_clip.write_videofile(mp4_file)
            video_clip.close()

            os.remove(downloaded_file_path)
            os.rmdir(temp_path)

            if update_progress:
                update_progress(100)

            return original_title, f"Téléchargement terminé : {mp4_file}"
        else:
            return None, "Erreur : Le fichier vidéo n'a pas été téléchargé correctement."

    except Exception as e:
        return None, f"Erreur : {e}"

def get_video_title(url):
    """Récupère le titre d'une vidéo YouTube sans la télécharger."""
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', 'Titre inconnu')
