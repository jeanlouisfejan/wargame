import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

class WargameMap:
    """Représente une carte de wargame"""
    def __init__(self, name, width, height, terrain_data):
        self.name = name
        self.width = width
        self.height = height
        self.terrain_data = terrain_data

class WargameViewer:
    """Visualiseur de carte de wargame avec pan et zoom"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wargame Map Viewer")
        self.root.geometry("1200x800")

        # Variables de pan (déplacement)
        self.pan_x = 0
        self.pan_y = 0
        self.is_panning = False
        self.last_mouse_pos = (0, 0)

        # Variables de zoom
        self.zoom_level = 1.0
        self.min_zoom = 0.3
        self.max_zoom = 3.0
        self.tile_size = 50

        # Carte actuelle
        self.current_map = None

        # Couleurs pour différents types de terrain
        self.terrain_colors = {
            'grass': '#228B22',
            'water': '#0077BE',
            'mountain': '#8B8989',
            'forest': '#006400',
            'desert': '#EDC9AF',
            'plains': '#90EE90'
        }

        # Liste des maps disponibles
        self.available_maps = self.load_available_maps()

        # Créer l'interface
        self.create_ui()

    def load_available_maps(self):
        """Charge la liste des maps disponibles"""
        maps_dir = Path("maps")
        maps_dir.mkdir(exist_ok=True)

        available_maps = []
        for map_file in maps_dir.glob("*.json"):
            available_maps.append(map_file.stem)

        # Si aucune map n'existe, créer des maps par défaut
        if not available_maps:
            self.create_default_maps()
            for map_file in maps_dir.glob("*.json"):
                available_maps.append(map_file.stem)

        return available_maps if available_maps else ["Aucune map disponible"]

    def create_default_maps(self):
        """Crée des maps par défaut pour l'exemple"""
        maps_dir = Path("maps")
        maps_dir.mkdir(exist_ok=True)

        # Map 1: Plaines et forêts
        map1 = {
            "name": "Plaines et Forêts",
            "width": 20,
            "height": 15,
            "terrain": [
                ["grass" if (x + y) % 3 != 0 else "forest"
                 for x in range(20)] for y in range(15)
            ]
        }

        with open(maps_dir / "plaines_forets.json", "w") as f:
            json.dump(map1, f, indent=2)

        # Map 2: Île
        map2_terrain = []
        for y in range(15):
            row = []
            for x in range(20):
                # Créer une île au centre
                dist_from_center = ((x - 10) ** 2 + (y - 7.5) ** 2) ** 0.5
                if dist_from_center < 4:
                    row.append("mountain")
                elif dist_from_center < 7:
                    row.append("grass")
                else:
                    row.append("water")
            map2_terrain.append(row)

        map2 = {
            "name": "Île Centrale",
            "width": 20,
            "height": 15,
            "terrain": map2_terrain
        }

        with open(maps_dir / "ile_centrale.json", "w") as f:
            json.dump(map2, f, indent=2)

        # Map 3: Désert et oasis
        map3_terrain = []
        for y in range(15):
            row = []
            for x in range(20):
                if 8 <= x <= 12 and 6 <= y <= 9:
                    row.append("water")
                elif 7 <= x <= 13 and 5 <= y <= 10:
                    row.append("grass")
                else:
                    row.append("desert")
            map3_terrain.append(row)

        map3 = {
            "name": "Désert et Oasis",
            "width": 20,
            "height": 15,
            "terrain": map3_terrain
        }

        with open(maps_dir / "desert_oasis.json", "w") as f:
            json.dump(map3, f, indent=2)

        # Map 4: Grande carte de bataille
        map4_terrain = []
        for y in range(30):
            row = []
            for x in range(40):
                # Rivière au milieu
                if 18 <= x <= 22:
                    row.append("water")
                # Montagnes au nord
                elif y < 5:
                    row.append("mountain")
                # Forêts éparpillées
                elif (x % 7 == 0 and y % 5 == 0):
                    row.append("forest")
                # Désert au sud
                elif y > 25:
                    row.append("desert")
                # Plaines ailleurs
                else:
                    row.append("plains")
            map4_terrain.append(row)

        map4 = {
            "name": "Grande Bataille",
            "width": 40,
            "height": 30,
            "terrain": map4_terrain
        }

        with open(maps_dir / "grande_bataille.json", "w") as f:
            json.dump(map4, f, indent=2)

    def create_ui(self):
        """Crée l'interface utilisateur"""
        # Frame supérieur pour les contrôles
        control_frame = tk.Frame(self.root, bg='#2E2E2E', height=100)
        control_frame.pack(fill=tk.X, side=tk.TOP)

        # Label pour le titre
        title_label = tk.Label(
            control_frame,
            text="WARGAME MAP VIEWER",
            font=('Arial', 16, 'bold'),
            bg='#2E2E2E',
            fg='white'
        )
        title_label.pack(pady=10)

        # Frame pour les contrôles
        controls = tk.Frame(control_frame, bg='#2E2E2E')
        controls.pack()

        # Label et menu déroulant
        map_label = tk.Label(
            controls,
            text="Sélectionner une carte:",
            font=('Arial', 10),
            bg='#2E2E2E',
            fg='white'
        )
        map_label.pack(side=tk.LEFT, padx=5)

        self.map_var = tk.StringVar()
        self.map_dropdown = ttk.Combobox(
            controls,
            textvariable=self.map_var,
            values=self.available_maps,
            state='readonly',
            width=30
        )
        self.map_dropdown.pack(side=tk.LEFT, padx=5)
        if self.available_maps:
            self.map_dropdown.set(self.available_maps[0])
        self.map_dropdown.bind('<<ComboboxSelected>>', self.on_map_selected)

        # Label de zoom
        self.zoom_label = tk.Label(
            controls,
            text=f"Zoom: {self.zoom_level:.2f}x",
            font=('Arial', 10),
            bg='#2E2E2E',
            fg='white'
        )
        self.zoom_label.pack(side=tk.LEFT, padx=20)

        # Instructions
        instructions = tk.Label(
            control_frame,
            text="Clic gauche + glisser: Déplacer | Molette: Zoom/Dézoom",
            font=('Arial', 9),
            bg='#2E2E2E',
            fg='#AAAAAA'
        )
        instructions.pack(pady=5)

        # Canvas pour la carte
        self.canvas = tk.Canvas(
            self.root,
            bg='#1A1A1A',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Lier les événements souris
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)

        # Charger la première carte
        if self.available_maps and self.available_maps[0] != "Aucune map disponible":
            self.load_map(self.available_maps[0])

    def on_map_selected(self, event):
        """Appelé quand une map est sélectionnée"""
        selected_map = self.map_var.get()
        self.load_map(selected_map)

    def load_map(self, map_name):
        """Charge une map depuis un fichier JSON"""
        map_path = Path("maps") / f"{map_name}.json"

        if not map_path.exists():
            print(f"La map {map_name} n'existe pas")
            return

        try:
            with open(map_path, "r") as f:
                map_data = json.load(f)

            self.current_map = WargameMap(
                name=map_data["name"],
                width=map_data["width"],
                height=map_data["height"],
                terrain_data=map_data["terrain"]
            )

            # Réinitialiser le zoom et le pan
            self.zoom_level = 1.0
            self.pan_x = 100
            self.pan_y = 100

            # Redessiner
            self.draw_map()

            print(f"Map '{map_data['name']}' chargée avec succès!")

        except Exception as e:
            print(f"Erreur lors du chargement de la map: {e}")

    def draw_map(self):
        """Dessine la carte sur le canvas"""
        self.canvas.delete('all')

        if not self.current_map:
            # Afficher un message si aucune carte
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text="Sélectionnez une carte dans le menu",
                fill='white',
                font=('Arial', 16)
            )
            return

        # Calculer la taille des tuiles avec le zoom
        scaled_tile_size = int(self.tile_size * self.zoom_level)

        # Dessiner chaque tuile
        for y in range(self.current_map.height):
            for x in range(self.current_map.width):
                terrain_type = self.current_map.terrain_data[y][x]
                color = self.terrain_colors.get(terrain_type, '#FFFFFF')

                # Position à l'écran
                screen_x = self.pan_x + x * scaled_tile_size
                screen_y = self.pan_y + y * scaled_tile_size

                # Dessiner la tuile
                self.canvas.create_rectangle(
                    screen_x,
                    screen_y,
                    screen_x + scaled_tile_size,
                    screen_y + scaled_tile_size,
                    fill=color,
                    outline='black',
                    width=1
                )

        # Mettre à jour le label de zoom
        self.zoom_label.config(text=f"Zoom: {self.zoom_level:.2f}x")

    def on_mouse_press(self, event):
        """Début du drag"""
        self.is_panning = True
        self.last_mouse_pos = (event.x, event.y)

    def on_mouse_drag(self, event):
        """Déplacement avec la souris"""
        if self.is_panning:
            dx = event.x - self.last_mouse_pos[0]
            dy = event.y - self.last_mouse_pos[1]
            self.pan_x += dx
            self.pan_y += dy
            self.last_mouse_pos = (event.x, event.y)
            self.draw_map()

    def on_mouse_release(self, event):
        """Fin du drag"""
        self.is_panning = False

    def on_mouse_wheel(self, event):
        """Gestion du zoom avec la molette"""
        if not self.current_map:
            return

        # Position de la souris
        mouse_x = event.x
        mouse_y = event.y

        # Zoom en fonction de la direction
        old_zoom = self.zoom_level

        if event.delta > 0:  # Zoom in
            self.zoom_level = min(self.zoom_level * 1.1, self.max_zoom)
        else:  # Zoom out
            self.zoom_level = max(self.zoom_level / 1.1, self.min_zoom)

        # Ajuster le pan pour zoomer vers la position de la souris
        zoom_ratio = self.zoom_level / old_zoom
        self.pan_x = mouse_x - (mouse_x - self.pan_x) * zoom_ratio
        self.pan_y = mouse_y - (mouse_y - self.pan_y) * zoom_ratio

        # Redessiner
        self.draw_map()

    def run(self):
        """Lance l'application"""
        self.root.mainloop()


def main():
    viewer = WargameViewer()
    viewer.run()


if __name__ == "__main__":
    main()
