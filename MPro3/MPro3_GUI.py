import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from dv2 import youtube_to_mp3, youtube_to_mp4, get_video_title
from tkinter import messagebox

# Création de la fenêtre principale
root = ttk.Window(themename="darkly")
root.title("YouTube Downloader")
root.geometry("500x450")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 11))

def update_progress(value):
    progress_bar["value"] = value
    percent_label.config(text=f"{int(value)}%")
    root.update_idletasks()

# Fonction pour récupérer le titre avant le téléchargement
def get_video_info():
    url = entry_url.get().strip()
    if not url:
        return

    original_title_label.config(text="Chargement des infos...", foreground="yellow")

    def fetch_title():
        try:
            title = get_video_title(url)
            original_title_label.config(text=f"Titre original : {title}", foreground="white")
        except Exception:
            original_title_label.config(text="Impossible de récupérer le titre", foreground="red")

    threading.Thread(target=fetch_title, daemon=True).start()

# Fonction de téléchargement
def start_download():
    url = entry_url.get().strip()
    custom_title = entry_title.get().strip()
    format_selected = format_choice.get()

    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube.")
        return

    status_label.config(text="Téléchargement en cours...", foreground="yellow")
    progress_bar["value"] = 0
    percent_label.config(text="0%")

    def run_download():
        try:
            if format_selected == "mp3":
                original_title, message = youtube_to_mp3(url, custom_title, update_progress)
            else:
                original_title, message = youtube_to_mp4(url, custom_title, update_progress)

            if original_title:
                original_title_label.config(text=f"Titre original : {original_title}", foreground="white")
            status_label.config(text=message, foreground="green")
        except Exception as e:
            status_label.config(text=f"Erreur : {e}", foreground="red")

    threading.Thread(target=run_download, daemon=True).start()

# Widgets modernes
frame = ttk.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=True)

label_url = ttk.Label(frame, text="Entrez l'URL de la vidéo YouTube :", bootstyle=PRIMARY)
label_url.pack(anchor=W)
entry_url = ttk.Entry(frame, width=50, font=("Arial", 12))
entry_url.pack(pady=5)
entry_url.bind("<FocusOut>", lambda event: get_video_info())

label_title = ttk.Label(frame, text="Titre personnalisé (optionnel) :", bootstyle=PRIMARY)
label_title.pack(anchor=W)
entry_title = ttk.Entry(frame, width=50, font=("Arial", 12))
entry_title.pack(pady=5)

# Choix du format de sortie
format_choice = ttk.StringVar(value="mp3")
radio_mp3 = ttk.Radiobutton(frame, text="MP3", variable=format_choice, value="mp3")
radio_mp4 = ttk.Radiobutton(frame, text="MP4", variable=format_choice, value="mp4")
radio_mp3.pack(anchor=W)
radio_mp4.pack(anchor=W)

download_button = ttk.Button(frame, text="Télécharger", command=start_download, bootstyle=SUCCESS)
download_button.pack(pady=10)

progress_bar = ttk.Progressbar(frame, length=300, mode="determinate", bootstyle=INFO)
progress_bar.pack(pady=10)
percent_label = ttk.Label(frame, text="0%", bootstyle=INFO)
percent_label.pack()

original_title_label = ttk.Label(frame, text="Titre original : Inconnu", bootstyle=SECONDARY)
original_title_label.pack(pady=5)

status_label = ttk.Label(frame, text="", bootstyle=SECONDARY)
status_label.pack()

root.mainloop()
