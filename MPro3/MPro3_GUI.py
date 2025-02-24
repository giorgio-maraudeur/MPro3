import threading
import tkinter as tk
from tkinter import messagebox
from downloader import youtube_to_mp3  # Import du module séparé

# Fonction appelée par le bouton
def start_download():
    url = entry_url.get().strip()
    custom_title = entry_title.get().strip()

    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube.")
        return

    status_label.config(text="Téléchargement en cours...", fg="blue")

    def run_download():
        try:
            original_title,message = youtube_to_mp3(url, custom_title)
            if original_title:
                original_title_label.config(text=f"Titre original : {original_title}", fg = "black")
            status_label.config(text=message, fg="green")
        except Exception as e:
            status_label.config(text=f"Erreur : {e}", fg="red")

    threading.Thread(target=run_download, daemon=True).start()



# --------------- Interface Tkinter ---------------
root = tk.Tk()
root.title("YouTube to MP3 Downloader")

label_url = tk.Label(root, text="Entrez l'URL de la vidéo YouTube :")
label_url.pack()
entry_url = tk.Entry(root, width=50)
entry_url.pack()


label_title = tk.Label(root, text="Titre personnalisé (optionnel) :")
label_title.pack()
entry_title = tk.Entry(root, width=50)
entry_title.pack()

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
