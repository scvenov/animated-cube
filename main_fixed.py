import tkinter as tk
import math

class TkinterMode:
    def __init__(self, root):
        self.root = root
        self.root.title("cube")
        self.root.geometry("800x600")
        self.root.resizable(width=False, height=False)
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1],
            [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]
        ]

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        self.faces = [
            ([0, 1, 2, 3], "#FF4444"),
            ([4, 5, 6, 7], "#4444FF"),
            ([0, 1, 5, 4], "#44FF44"),
            ([2, 3, 7, 6], "#FFFF44"),
            ([0, 3, 7, 4], "#FF44FF"),
            ([1, 2, 6, 5], "#FF8844")
        ]

        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0
        self.speed_x = 0.02
        self.speed_y = 0.03
        self.speed_z = 0.01
        self.center_x = 400
        self.center_y = 300

        self.root.bind("r", lambda _: self.reset_rotation())
        self.root.bind("<Escape>", lambda _: self.root.destroy())

        self.animate()

    def reset_rotation(self):
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0

    def rotate_point(self, point, angle_x, angle_y, angle_z):
        x, y, z = point
        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
        y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
        cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
        x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

        distance = 5
        scale = 100
        if z + distance != 0:
            factor = scale / (z + distance)
            return (int(x * factor + self.center_x), int(y * factor + self.center_y), z)
        return (self.center_x, self.center_y, z)

    def draw_face(self, points, color):
        if len(points) < 3:
            return
        coords = []
        for point in points:
            coords.extend([point[0], point[1]])
        self.canvas.create_polygon(coords, fill=color, outline="white", width=2)

    def draw_edge(self, point1, point2):
        x1, y1, _ = point1
        x2, y2, _ = point2
        self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

    def animate(self):
        self.canvas.delete("all")

        self.angle_x += self.speed_x
        self.angle_y += self.speed_y
        self.angle_z += self.speed_z

        projected_points = [self.rotate_point(v, self.angle_x, self.angle_y, self.angle_z) for v in self.vertices]

        faces_with_depth = []
        for face_indices, color in self.faces:
            avg_z = sum(projected_points[i][2] for i in face_indices) / len(face_indices)
            faces_with_depth.append((avg_z, face_indices, color))

        faces_with_depth.sort(reverse=True)

        for _, face_indices, color in faces_with_depth:
            self.draw_face([projected_points[i] for i in face_indices], color)

        for edge in self.edges:
            self.draw_edge(projected_points[edge[0]], projected_points[edge[1]])

        self.canvas.create_text(400, 580, text="R for reset ESC to exit", fill="white", font=("Arial", 12))
        self.root.after(16, self.animate)


class CustomtkinterMode:
    def __init__(self):
        try:
            import customtkinter as ctk
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

            self.root = ctk.CTk()
            self.root.title("cube animate")
            self.root.geometry("900x700")
            self.root.resizable(False, False)

            self.canvas_frame = ctk.CTkFrame(self.root)
            self.canvas_frame.pack(padx=15, pady=5, fill="both", expand=True)

            self.canvas = tk.Canvas(self.canvas_frame, width=870, height=500, bg="black", highlightthickness=0)
            self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

            self.controls_frame = ctk.CTkFrame(self.root)
            self.controls_frame.pack(pady=10, padx=15, fill="x")

            ctk.CTkButton(self.controls_frame, text="Pause", command=self.toggle_pause, width=110).pack(side=tk.LEFT, padx=5)
            ctk.CTkButton(self.controls_frame, text="Reset", command=self.reset_rotation, width=110).pack(side=tk.LEFT, padx=5)

            radio_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
            radio_frame.pack(side=tk.LEFT, padx=25)

            self.speed_mult = tk.DoubleVar(value=1.0)
            for val, lbl in [(0.5, "0.5x"), (1.0, "1.0x"), (2.0, "2.0x")]:
                ctk.CTkRadioButton(radio_frame, text=lbl, variable=self.speed_mult, value=val,
                                   command=self.update_speed).pack(side=tk.LEFT, padx=10)

            self.speed_label = ctk.CTkLabel(self.controls_frame, text="speed: 1.0x", width=100)
            self.speed_label.pack(side=tk.LEFT, padx=5)

            self.vertices = [
                [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1],
                [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]
            ]

            self.edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),
                (4, 5), (5, 6), (6, 7), (7, 4),
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]

            self.faces = [
                ([0, 1, 2, 3], "#FF6B6B"),
                ([4, 5, 6, 7], "#4ECDC4"),
                ([0, 1, 5, 4], "#45B7D1"),
                ([2, 3, 7, 6], "#96CEB4"),
                ([0, 3, 7, 4], "#FFEAA7"),
                ([1, 2, 6, 5], "#DDA0DD")
            ]

            self.angle_x = 0.0
            self.angle_y = 0.0
            self.angle_z = 0.0
            self.base_speed = 0.02
            self.paused = False
            self.center_x = 435
            self.center_y = 250

            self.root.bind("r", lambda _: self.reset_rotation())
            self.root.bind("<Escape>", lambda _: self.root.destroy())

            self.animate()
            self.root.mainloop()

        except ImportError:
            print("default verison running..")
            tk_root = tk.Tk()
            TkinterMode(tk_root)
            tk_root.mainloop()

    def toggle_pause(self):
        self.paused = not self.paused

    def reset_rotation(self):
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0

    def update_speed(self):
        mult = self.speed_mult.get()
        self.speed_label.configure(text=f"speed: {mult:.1f}x")
        self.base_speed = 0.02 * mult

    def rotate_point(self, point, angle_x, angle_y, angle_z):
        x, y, z = point
        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
        y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
        cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
        x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

        distance = 5
        scale = 100
        if z + distance != 0:
            factor = scale / (z + distance)
            return (int(x * factor + self.center_x), int(y * factor + self.center_y), z)
        return (self.center_x, self.center_y, z)

    def draw_face(self, points, color):
        if len(points) < 3:
            return
        coords = []
        for point in points:
            coords.extend([point[0], point[1]])
        self.canvas.create_polygon(coords, fill=color, outline="white", width=2)

    def draw_edge(self, point1, point2):
        x1, y1, _ = point1
        x2, y2, _ = point2
        self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

    def animate(self):
        self.canvas.delete("all")

        if not self.paused:
            self.angle_x += self.base_speed
            self.angle_y += self.base_speed * 1.5
            self.angle_z += self.base_speed * 0.5

        projected_points = [self.rotate_point(v, self.angle_x, self.angle_y, self.angle_z) for v in self.vertices]

        faces_with_depth = []
        for face_indices, color in self.faces:
            avg_z = sum(projected_points[i][2] for i in face_indices) / len(face_indices)
            faces_with_depth.append((avg_z, face_indices, color))

        faces_with_depth.sort(reverse=True)

        for _, face_indices, color in faces_with_depth:
            self.draw_face([projected_points[i] for i in face_indices], color)

        for edge in self.edges:
            self.draw_edge(projected_points[edge[0]], projected_points[edge[1]])

        self.root.after(16, self.animate)


if __name__ == "__main__":
    print("1. tkinter")
    print("2. customtkinter")

    choice = input("//:  ").strip()

    if choice == "2":
        try:
            CustomtkinterMode()
        except (ImportError, ModuleNotFoundError, AttributeError):
            print("customtkinter not installed, running default verison")
            tk_root = tk.Tk()
            TkinterMode(tk_root)
            tk_root.mainloop()
    else:
        tk_root = tk.Tk()
        TkinterMode(tk_root)
        tk_root.mainloop()