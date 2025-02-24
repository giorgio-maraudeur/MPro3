import threading
import tkinter as tk
from tkinter import messagebox
from downloader import youtube_to_mp3, youtube_to_mp4  # Import du module séparé
import yt_dlp
# bonne docu tkinter : https://python.doctor/page-tkinter-interface-graphique-python-tutoriel 

# Fonction appelée par le bouton
def start_download():
    url = entry_url.get().strip()
    custom_title = entry_title.get().strip()
    format_selected = format_choice.get() # Récupérer le format choisi

    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube.")
        return

    status_label.config(text="Téléchargement en cours...", fg="blue")

    def run_download():
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(url, download=False) # Télécharge les informations de la vidéo sans la télécharger
                original_title = info_dict.get('title', 'Titre inconnu')
                original_title_label.config(text=f"Titre original : {original_title}", fg = "black")

                # Exécuter la bonne fonction selon le format choisi

                if format_selected == "mp3":
                    message = youtube_to_mp3(url, custom_title)
                else:
                    message = youtube_to_mp4(url, custom_title)

                status_label.config(text=message, fg="green")
        except Exception as e:
            status_label.config(text=f"Erreur : {e}", fg="red")

    threading.Thread(target=run_download, daemon=True).start() # Créer un thread pour ne pas bloquer l'interface 




# --------------- Interface Tkinter ---------------
root = tk.Tk()
root.title("YouTube to MP3 Downloader")
root.geometry("400x200")

label_url = tk.Label(root, text="Entrez l'URL de la vidéo YouTube :")
label_url.pack()
entry_url = tk.Entry(root, width=50)
entry_url.pack()


label_title = tk.Label(root, text="Titre personnalisé (optionnel) :")
label_title.pack()
entry_title = tk.Entry(root, width=50)
entry_title.pack()

# ---- Choix du format de sortie 
format_choice = tk.StringVar(value="mp3") # Valeur par défaut

radio_mp3 = tk.Radiobutton(root, text="MP3", variable=format_choice, value="mp3")
radio_mp4 = tk.Radiobutton(root, text="MP4", variable=format_choice, value="mp4")
radio_mp3.pack()
radio_mp4.pack()



download_button = tk.Button(root, text="Télécharger", command=start_download)
download_button.pack()

#Déplacer le focus sur ke champ titre en appuyant sur Entrée dans l'URL
def focus_title(event):
    entry_title.focus_set() # le focus c'est le curseur

#Lancer le téléchargement en appuyant sur Entrée dans le champ titre
def start_download_enter(event):
    start_download() 

# Associer les touches Entrée aux champs URL et titre
entry_url.bind("<Return>", focus_title) # bind = associer
entry_title.bind("<Return>", start_download_enter) # "<Return>" = touche Entrée

original_title_label = tk.Label(root, text="Titre original : Inconnu", fg="gray")
original_title_label.pack()

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()


root.mainloop()
