import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class MapViewer:
    """Visualiseur de carte de wargame simple"""

    def __init__(self):
        # Fenêtre principale
        self.root = tk.Tk()
        self.root.title("Wargame Map Viewer")
        self.root.geometry("1200x800")

        # Variables pour l'image
        self.original_image = None  # Image PIL originale
        self.photo_image = None  # PhotoImage pour Tkinter
        self.image_id = None  # ID de l'image sur le canvas

        # Variables de déplacement
        self.pan_x = 0
        self.pan_y = 0
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Variables de zoom
        self.zoom_level = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0

        # Créer l'interface
        self.create_menu()
        self.create_canvas()

    def create_menu(self):
        """Crée la barre de menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Charger carte JPG...", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)

        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Zoom +", command=self.zoom_in)
        view_menu.add_command(label="Zoom -", command=self.zoom_out)
        view_menu.add_command(label="Réinitialiser vue", command=self.reset_view)

        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.show_about)

    def create_canvas(self):
        """Crée le canvas pour afficher la carte"""
        # Frame pour le canvas et la barre d'état
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(
            main_frame,
            bg='#2C2C2C',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Barre d'état
        self.status_bar = tk.Label(
            self.root,
            text="Prêt | Utilisez Fichier > Charger carte JPG pour commencer",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#E0E0E0',
            padx=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Lier les événements souris
        self.canvas.bind('<ButtonPress-1>', self.on_drag_start)
        self.canvas.bind('<B1-Motion>', self.on_drag_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_drag_end)
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)

        # Message d'accueil
        self.canvas.create_text(
            600, 400,
            text="Chargez une carte JPG via le menu Fichier",
            fill='white',
            font=('Arial', 14),
            tags='welcome'
        )

    def load_image(self):
        """Charge une image JPG depuis un fichier"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner une carte",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("Tous les fichiers", "*.*")
            ]
        )

        if file_path:
            try:
                # Charger l'image avec PIL
                self.original_image = Image.open(file_path)

                # Réinitialiser la vue
                self.zoom_level = 1.0
                self.pan_x = 0
                self.pan_y = 0

                # Afficher l'image
                self.update_display()

                # Mettre à jour la barre d'état
                width, height = self.original_image.size
                self.status_bar.config(
                    text=f"Carte chargée: {file_path} | Dimensions: {width}x{height}px | Zoom: {self.zoom_level:.2f}x"
                )

            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de charger l'image:\n{str(e)}"
                )

    def update_display(self):
        """Met à jour l'affichage de l'image avec le zoom et le déplacement actuels"""
        if self.original_image is None:
            return

        try:
            # Calculer les nouvelles dimensions
            orig_width, orig_height = self.original_image.size
            new_width = int(orig_width * self.zoom_level)
            new_height = int(orig_height * self.zoom_level)

            # Redimensionner l'image
            resized = self.original_image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            # Convertir pour Tkinter
            self.photo_image = ImageTk.PhotoImage(resized)

            # Supprimer l'ancienne image et le message d'accueil
            self.canvas.delete('all')

            # Afficher la nouvelle image
            self.image_id = self.canvas.create_image(
                self.pan_x,
                self.pan_y,
                image=self.photo_image,
                anchor='nw'
            )

            # Mettre à jour la barre d'état
            self.status_bar.config(
                text=f"Zoom: {self.zoom_level:.2f}x | Position: ({self.pan_x}, {self.pan_y})"
            )

        except Exception as e:
            print(f"Erreur lors de l'affichage: {e}")

    def on_drag_start(self, event):
        """Début du déplacement"""
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_move(self, event):
        """Déplacement en cours"""
        if self.is_dragging and self.original_image:
            # Calculer le déplacement
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            # Mettre à jour la position
            self.pan_x += dx
            self.pan_y += dy

            # Mettre à jour le point de départ pour le prochain mouvement
            self.drag_start_x = event.x
            self.drag_start_y = event.y

            # Redessiner
            self.update_display()

    def on_drag_end(self, event):
        """Fin du déplacement"""
        self.is_dragging = False

    def on_mouse_wheel(self, event):
        """Gestion du zoom avec la molette"""
        if self.original_image is None:
            return

        # Position de la souris
        mouse_x = event.x
        mouse_y = event.y

        # Ancien zoom
        old_zoom = self.zoom_level

        # Calculer le nouveau zoom
        if event.delta > 0:  # Zoom avant
            self.zoom_level = min(self.zoom_level * 1.1, self.max_zoom)
        else:  # Zoom arrière
            self.zoom_level = max(self.zoom_level / 1.1, self.min_zoom)

        # Ajuster le pan pour zoomer vers la position de la souris
        zoom_ratio = self.zoom_level / old_zoom
        self.pan_x = mouse_x - (mouse_x - self.pan_x) * zoom_ratio
        self.pan_y = mouse_y - (mouse_y - self.pan_y) * zoom_ratio

        # Redessiner
        self.update_display()

    def zoom_in(self):
        """Zoom avant (depuis le menu)"""
        if self.original_image:
            self.zoom_level = min(self.zoom_level * 1.2, self.max_zoom)
            self.update_display()

    def zoom_out(self):
        """Zoom arrière (depuis le menu)"""
        if self.original_image:
            self.zoom_level = max(self.zoom_level / 1.2, self.min_zoom)
            self.update_display()

    def reset_view(self):
        """Réinitialise la vue"""
        if self.original_image:
            self.zoom_level = 1.0
            self.pan_x = 0
            self.pan_y = 0
            self.update_display()

    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        messagebox.showinfo(
            "À propos",
            "Wargame Map Viewer\n\n"
            "Version 1.0\n\n"
            "Visualiseur de cartes pour wargames\n\n"
            "Fonctionnalités:\n"
            "- Chargement d'images JPG/PNG\n"
            "- Déplacement à la souris\n"
            "- Zoom/Dézoom à la molette"
        )

    def run(self):
        """Lance l'application"""
        self.root.mainloop()


def main():
    app = MapViewer()
    app.run()


if __name__ == "__main__":
    main()
