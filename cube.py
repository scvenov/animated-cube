import tkinter as tk
import math
import colorsys

class AnimatedCube:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Анимированный Куб")
        self.root.geometry("800x600")
        
        # Создаем холст для рисования
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Вершины куба
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1],  # Нижняя грань
            [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]        # Верхняя грань
        ]
        
        # Ребра куба
        self.edges = [
            (0,1), (1,2), (2,3), (3,0),  # Нижняя грань
            (4,5), (5,6), (6,7), (7,4),  # Верхняя грань
            (0,4), (1,5), (2,6), (3,7)   # Боковые ребра
        ]
        
        # Грани куба (для заливки цветом)
        self.faces = [
            ([0,1,2,3], "красный"),      # нижняя
            ([4,5,6,7], "синий"),        # верхняя
            ([0,1,5,4], "зеленый"),      # передняя
            ([2,3,7,6], "желтый"),       # задняя
            ([0,3,7,4], "пурпурный"),    # левая
            ([1,2,6,5], "оранжевый")     # правая
        ]
        
        # Углы вращения
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
        # Скорость вращения
        self.speed_x = 0.02
        self.speed_y = 0.03
        self.speed_z = 0.01
        
        # Центр экрана
        self.center_x = 400
        self.center_y = 300
        
        # Запускаем анимацию
        self.animate()
        
    def rotate_point(self, point, angle_x, angle_y, angle_z):
        """Вращает точку в 3D пространстве"""
        x, y, z = point
        
        # Вращение по X
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x
        y, z = y1, z1
        
        # Вращение по Y
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x1 = x * cos_y + z * sin_y
        z1 = -x * sin_y + z * cos_y
        x, z = x1, z1
        
        # Вращение по Z
        cos_z = math.cos(angle_z)
        sin_z = math.sin(angle_z)
        x1 = x * cos_z - y * sin_z
        y1 = x * sin_z + y * cos_z
        x, y = x1, y1
        
        # Перспективная проекция
        distance = 5
        scale = 100  # Масштаб
        if z + distance != 0:
            factor = scale / (z + distance)
            screen_x = int(x * factor + self.center_x)
            screen_y = int(y * factor + self.center_y)
            return (screen_x, screen_y, z)
        return (self.center_x, self.center_y, z)
    
    def draw_face(self, points, color_name):
        """Рисует грань куба с заливкой"""
        colors = {
            "красный": "#FF4444",
            "синий": "#4444FF",
            "зеленый": "#44FF44",
            "желтый": "#FFFF44",
            "пурпурный": "#FF44FF",
            "оранжевый": "#FF8844"
        }
        
        # Проверяем, видима ли грань (по нормали)
        if len(points) >= 3:
            # Вычисляем нормаль для проверки видимости
            x1, y1, _ = points[0]
            x2, y2, _ = points[1]
            x3, y3, _ = points[2]
            
            # Векторное произведение для определения направления
            z1 = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
            
            # Рисуем только если грань обращена к камере
            if z1 > 0:
                coords = []
                for point in points:
                    coords.extend([point[0], point[1]])
                
                # Рисуем залитый многоугольник
                self.canvas.create_polygon(
                    coords,
                    fill=colors[color_name],
                    outline="white",
                    width=2,
                    stipple="gray50"  # Добавляем текстуру для эффекта 3D
                )
    
    def draw_edge(self, point1, point2):
        """Рисует ребро куба"""
        x1, y1, _ = point1
        x2, y2, _ = point2
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill="white",
            width=2
        )
    
    def animate(self):
        """Основной цикл анимации"""
        # Очищаем холст
        self.canvas.delete("all")
        
        # Вращаем куб
        self.angle_x += self.speed_x
        self.angle_y += self.speed_y
        self.angle_z += self.speed_z
        
        # Проецируем все вершины
        projected_points = []
        for vertex in self.vertices:
            projected = self.rotate_point(
                vertex,
                self.angle_x,
                self.angle_y,
                self.angle_z
            )
            projected_points.append(projected)
        
        # Рисуем грани (сначала задние, потом передние для правильного перекрытия)
        # Сортируем грани по средней глубине
        faces_with_depth = []
        for face_indices, color in self.faces:
            # Вычисляем среднюю глубину грани
            avg_z = sum(projected_points[i][2] for i in face_indices) / len(face_indices)
            faces_with_depth.append((avg_z, face_indices, color))
        
        # Сортируем от дальних к ближним
        faces_with_depth.sort(reverse=True)
        
        # Рисуем грани
        for _, face_indices, color in faces_with_depth:
            face_points = [projected_points[i] for i in face_indices]
            self.draw_face(face_points, color)
        
        # Рисуем ребра поверх граней
        for edge in self.edges:
            self.draw_edge(
                projected_points[edge[0]],
                projected_points[edge[1]]
            )
        
        # Добавляем информационный текст
        self.canvas.create_text(
            400, 580,
            text=f"3D Вращающийся Куб | Press 'R' for reset | 'ESC' to exit",
            fill="white",
            font=("Arial", 12)
        )
        
        # Продолжаем анимацию
        self.root.after(16, self.animate)  # ~60 FPS


class CubeWithCustomTKinter:
    """Версия с customtkinter (более современный вид)"""
    
    def __init__(self):
        try:
            import customtkinter as ctk
            
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            self.root = ctk.CTk()
            self.root.title("3D Анимированный Куб - Modern Edition")
            self.root.geometry("900x700")
            
            # Создаем фрейм для управления
            control_frame = ctk.CTkFrame(self.root)
            control_frame.pack(pady=10, padx=10, fill="x")
            
            # Заголовок
            title_label = ctk.CTkLabel(
                control_frame,
                text="3D Вращающийся Куб",
                font=("Arial", 20, "bold")
            )
            title_label.pack(pady=5)
            
            # Создаем холст для рисования
            self.canvas_frame = ctk.CTkFrame(self.root)
            self.canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)
            
            self.canvas = tk.Canvas(
                self.canvas_frame,
                width=850,
                height=600,
                bg='black',
                highlightthickness=0
            )
            self.canvas.pack(fill=tk.BOTH, expand=True)
            
            # Панель управления
            controls = ctk.CTkFrame(self.root)
            controls.pack(pady=10, padx=10, fill="x")
            
            # Кнопки управления
            ctk.CTkButton(
                controls,
                text="⏸ Пауза",
                command=self.toggle_pause,
                width=100
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                controls,
                text="⟳ Сброс",
                command=self.reset_rotation,
                width=100
            ).pack(side="left", padx=5)
            
            # Скорость вращения
            speed_frame = ctk.CTkFrame(controls)
            speed_frame.pack(side="left", padx=20)
            
            ctk.CTkLabel(speed_frame, text="Скорость:").pack(side="left", padx=5)
            
            self.speed_var = tk.DoubleVar(value=1.0)
            speed_slider = ctk.CTkSlider(
                speed_frame,
                from_=0.1,
                to=3.0,
                variable=self.speed_var,
                command=self.change_speed,
                width=150
            )
            speed_slider.pack(side="left", padx=5)
            
            self.speed_label = ctk.CTkLabel(speed_frame, text="1.0x")
            self.speed_label.pack(side="left", padx=5)
            
            # Инициализация куба
            self.vertices = [
                [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1],
                [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]
            ]
            
            self.edges = [
                (0,1), (1,2), (2,3), (3,0),
                (4,5), (5,6), (6,7), (7,4),
                (0,4), (1,5), (2,6), (3,7)
            ]
            
            self.faces = [
                ([0,1,2,3], "#FF6B6B"),  # красный
                ([4,5,6,7], "#4ECDC4"),  # бирюзовый
                ([0,1,5,4], "#45B7D1"),  # голубой
                ([2,3,7,6], "#96CEB4"),  # зеленый
                ([0,3,7,4], "#FFEAA7"),  # желтый
                ([1,2,6,5], "#DDA0DD")   # пурпурный
            ]
            
            self.angle_x = 0
            self.angle_y = 0
            self.angle_z = 0
            self.base_speed = 0.02
            self.paused = False
            
            self.center_x = 425
            self.center_y = 300
            
            self.animate()
            self.root.mainloop()
            
        except ImportError:
            print("customtkinter не установлен. Установите: pip install customtkinter")
            print("Запускается стандартная версия...")
            root = tk.Tk()
            app = AnimatedCube(root)
            root.mainloop()
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def reset_rotation(self):
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
    
    def change_speed(self, value):
        speed_mult = float(value)
        self.speed_label.configure(text=f"{speed_mult:.1f}x")
        self.base_speed = 0.02 * speed_mult
    
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
            screen_x = int(x * factor + self.center_x)
            screen_y = int(y * factor + self.center_y)
            return (screen_x, screen_y, z)
        return (self.center_x, self.center_y, z)
    
    def draw_face(self, points, color):
        if len(points) >= 3:
            x1, y1, _ = points[0]
            x2, y2, _ = points[1]
            x3, y3, _ = points[2]
            
            if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) > 0:
                coords = []
                for point in points:
                    coords.extend([point[0], point[1]])
                
                self.canvas.create_polygon(coords, fill=color, outline="white", width=2)
    
    def draw_edge(self, point1, point2):
        x1, y1, _ = point1
        x2, y2, _ = point2
        self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)
    
    def animate(self):
        if not self.paused:
            self.canvas.delete("all")
            
            if not self.paused:
                self.angle_x += self.base_speed
                self.angle_y += self.base_speed * 1.5
                self.angle_z += self.base_speed * 0.5
            
            projected_points = []
            for vertex in self.vertices:
                projected = self.rotate_point(vertex, self.angle_x, self.angle_y, self.angle_z)
                projected_points.append(projected)
            
            # Рисуем грани от дальних к ближним
            faces_with_depth = []
            for face_indices, color in self.faces:
                avg_z = sum(projected_points[i][2] for i in face_indices) / len(face_indices)
                faces_with_depth.append((avg_z, face_indices, color))
            
            faces_with_depth.sort(reverse=True)
            
            for _, face_indices, color in faces_with_depth:
                face_points = [projected_points[i] for i in face_indices]
                self.draw_face(face_points, color)
            
            for edge in self.edges:
                self.draw_edge(projected_points[edge[0]], projected_points[edge[1]])
        
        self.root.after(16, self.animate)


if __name__ == "__main__":
    print("Запуск 3D анимации куба...")
    print("Выберите версию:")
    print("1. Стандартный tkinter")
    print("2. Modern (customtkinter - если установлен)")
    
    choice = input("Ваш выбор (1/2): ").strip()
    
    if choice == "2":
        try:
            app = CubeWithCustomTKinter()
        except:
            print("Ошибка при запуске customtkinter, запускаю стандартную версию...")
            root = tk.Tk()
            app = AnimatedCube(root)
            root.mainloop()
    else:
        root = tk.Tk()
        app = AnimatedCube(root)
        root.mainloop()