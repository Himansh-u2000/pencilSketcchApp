import tkinter as tk
from tkinter.colorchooser import askcolor

class PencilSketchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencil Sketch App")

        # Default pencil settings
        self.pen_color = "black"
        self.pen_width = 5

        # UI Layout
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        # Color chooser button
        self.color_btn = tk.Button(self.controls_frame, text="Choose Color", command=self.choose_color)
        self.color_btn.pack(side=tk.LEFT, padx=5)

        # Pen width slider
        self.width_slider = tk.Scale(self.controls_frame, from_=1, to=20, orient=tk.HORIZONTAL, label="Pen Width")
        self.width_slider.set(self.pen_width)
        self.width_slider.pack(side=tk.LEFT, padx=5)

        # Bind drawing events
        self.canvas.bind("<B1-Motion>", self.draw)
        self.last_x, self.last_y = None, None
        self.canvas.bind("<Button-1>", self.set_start_pos)

    def choose_color(self):
        color = askcolor(title="Select Pencil Color")[1]
        if color:
            self.pen_color = color

    def set_start_pos(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.last_x and self.last_y:
            self.pen_width = self.width_slider.get()
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    fill=self.pen_color, width=self.pen_width,
                                    capstyle=tk.ROUND, smooth=True)
        self.last_x, self.last_y = event.x, event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = PencilSketchApp(root)
    root.mainloop()
