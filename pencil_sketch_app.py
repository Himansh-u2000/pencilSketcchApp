import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageGrab, ImageTk
import os

class PencilSketchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencil Sketch App")

        self.pen_color = "black"
        self.pen_width = 5
        self.eraser_mode = False
        self.undo_stack = []
        self.bg_color = "white"
        self.tool = "pencil"
        self.start_x = self.start_y = None

        # Canvas
        self.canvas = tk.Canvas(root, bg=self.bg_color, width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Controls
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        tk.Button(self.controls_frame, text="Choose Color", command=self.choose_color).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls_frame, text="Eraser", command=self.toggle_eraser).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls_frame, text="Save as PNG", command=self.save_as_image).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls_frame, text="Toggle Background", command=self.toggle_background).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls_frame, text="Set Image Background", command=self.set_image_background).pack(side=tk.LEFT, padx=5)

        self.width_slider = tk.Scale(self.controls_frame, from_=1, to=20, orient=tk.HORIZONTAL, label="Pen Width")
        self.width_slider.set(self.pen_width)
        self.width_slider.pack(side=tk.LEFT)

        # Tool selectors
        tools = ["pencil", "line", "rectangle", "circle"]
        for t in tools:
            tk.Button(self.controls_frame, text=t.capitalize(), command=lambda tool=t: self.set_tool(tool)).pack(side=tk.LEFT, padx=2)

        # Events
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Control-z>", self.undo)

    def choose_color(self):
        color = askcolor(title="Select Pencil Color")[1]
        if color:
            self.pen_color = color
            self.eraser_mode = False

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode

    def clear_canvas(self):
        self.canvas.delete("all")
        self.undo_stack.clear()

    def toggle_background(self):
        self.bg_color = "light gray" if self.bg_color == "white" else "white"
        self.canvas.config(bg=self.bg_color)

    def set_image_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            bg_img = Image.open(file_path)
            bg_img = bg_img.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))
            self.bg_image_tk = ImageTk.PhotoImage(bg_img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image_tk)

    def set_tool(self, tool_name):
        self.tool = tool_name
        self.eraser_mode = False

    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.tool == "pencil":
            self.draw_line(event)

    def on_draw(self, event):
        if self.tool == "pencil":
            self.draw_line(event)
        elif self.tool in ("line", "rectangle", "circle"):
            self.canvas.delete("preview")
            if self.tool == "line":
                self.preview_item = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.pen_color, width=self.width_slider.get(), tags="preview")
            elif self.tool == "rectangle":
                self.preview_item = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.width_slider.get(), tags="preview")
            elif self.tool == "circle":
                self.preview_item = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.width_slider.get(), tags="preview")

    def on_button_release(self, event):
        if self.tool in ("line", "rectangle", "circle"):
            self.canvas.delete("preview")
            if self.tool == "line":
                item = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.pen_color, width=self.width_slider.get())
            elif self.tool == "rectangle":
                item = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.width_slider.get())
            elif self.tool == "circle":
                item = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.width_slider.get())
            self.undo_stack.append(item)
        self.start_x = self.start_y = None

    def draw_line(self, event):
        color = "white" if self.eraser_mode else self.pen_color
        line = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                       fill=color, width=self.width_slider.get(),
                                       capstyle=tk.ROUND, smooth=True)
        self.undo_stack.append(line)
        self.start_x, self.start_y = event.x, event.y

    def undo(self, event=None):
        if self.undo_stack:
            last = self.undo_stack.pop()
            self.canvas.delete(last)

    def save_as_image(self):
        # Save canvas content to file
        self.root.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if filepath:
            ImageGrab.grab().crop((x, y, x1, y1)).save(filepath)
            print(f"Image saved to {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PencilSketchApp(root)
    root.mainloop()
