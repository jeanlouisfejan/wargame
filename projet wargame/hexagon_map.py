import tkinter as tk
import math

# --- Constants ---
GRID_WIDTH = 10
GRID_HEIGHT = 10
HEX_SIZE = 30  # From center to a corner
CANVAS_BG = "#f0f0f0"
HEX_OUTLINE = "black"
HEX_FILL = "white"

# --- Calculated dimensions ---
# For pointy-top hexagons
HEX_HEIGHT = 2 * HEX_SIZE
HEX_WIDTH = math.sqrt(3) * HEX_SIZE
VERT_SPACING = HEX_HEIGHT * 3/4
HORIZ_SPACING = HEX_WIDTH

# --- Main Application Class ---
class HexagonGrid(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hexagon Map")

        # Calculate canvas size
        canvas_width = (GRID_WIDTH * HORIZ_SPACING) + (HORIZ_SPACING / 2) + HEX_SIZE
        canvas_height = (GRID_HEIGHT * VERT_SPACING) + (VERT_SPACING) + HEX_SIZE
        
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg=CANVAS_BG)
        self.canvas.pack(padx=10, pady=10)

        self.draw_grid()

    def draw_hexagon(self, center_x, center_y, size):
        """Draws a single pointy-top hexagon on the canvas."""
        points = []
        for i in range(6):
            angle_deg = 60 * i + 30  # +30 degrees to make it pointy-top
            angle_rad = math.pi / 180 * angle_deg
            px = center_x + size * math.cos(angle_rad)
            py = center_y + size * math.sin(angle_rad)
            points.append((px, py))
        
        self.canvas.create_polygon(points, outline=HEX_OUTLINE, fill=HEX_FILL, width=2)

    def draw_grid(self):
        """Draws the 10x10 grid of hexagons."""
        start_x = HEX_WIDTH / 2 + 10
        start_y = HEX_HEIGHT / 2 + 10

        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                offset_x = 0
                if row % 2 != 0:
                    offset_x = HORIZ_SPACING / 2  # Offset every other row

                center_x = start_x + col * HORIZ_SPACING + offset_x
                center_y = start_y + row * VERT_SPACING

                self.draw_hexagon(center_x, center_y, HEX_SIZE)

# --- Run the application ---
if __name__ == "__main__":
    app = HexagonGrid()
    app.mainloop()
