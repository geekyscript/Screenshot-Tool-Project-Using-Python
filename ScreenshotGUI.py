import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import ImageGrab, Image, ImageDraw, ImageTk
import datetime


class ScreenshotTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Tool")
        self.root.geometry("400x400")
        self.root.configure(bg='#2e3f4f')
        self.root.iconbitmap('icon.ico')  # Make sure you have an 'icon.ico' file

        self.title_label = tk.Label(root, text="Screenshot Tool", font=("Arial", 20, "bold"), bg='#2e3f4f', fg='white')
        self.title_label.pack(pady=10)

        self.capture_button = tk.Button(root, text="Capture Full Screen", command=self.capture_screenshot, height=2,
                                        width=25, bg='#4caf50', fg='white', font=("Arial", 12))
        self.capture_button.pack(pady=10)

        self.area_button = tk.Button(root, text="Capture Area", command=self.capture_area, height=2, width=25,
                                     bg='#2196f3', fg='white', font=("Arial", 12))
        self.area_button.pack(pady=10)

        self.edit_button = tk.Button(root, text="Edit Last Screenshot", command=self.edit_screenshot, height=2,
                                     width=25, bg='#ff9800', fg='white', font=("Arial", 12), state=tk.DISABLED)
        self.edit_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Last Screenshot", command=self.save_screenshot, height=2,
                                     width=25, bg='#1c27b0', fg='white', font=("Arial", 12), state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.last_screenshot = None

    def capture_screenshot(self):
        self.root.withdraw()
        self.root.after(500, self._do_screenshot)

    def _do_screenshot(self):
        screenshot = ImageGrab.grab()
        self.last_screenshot = screenshot
        self.save_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.NORMAL)
        self.root.deiconify()
        messagebox.showinfo("Screenshot Taken", "Screenshot captured successfully!")

    def capture_area(self):
        self.root.withdraw()
        self.selection_window = tk.Toplevel()
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)
        self.selection_window.configure(background='black')

        self.start_x = self.start_y = None
        self.rect = None

        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red',
                                                 width=2)

    def on_move_press(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.selection_window.destroy()
        self.root.after(500, lambda: self._grab_area(self.start_x, self.start_y, end_x, end_y))

    def _grab_area(self, x1, y1, x2, y2):
        screenshot = ImageGrab.grab(bbox=(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
        self.last_screenshot = screenshot
        self.save_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.NORMAL)
        self.root.deiconify()
        messagebox.showinfo("Area Screenshot Taken", "Area screenshot captured successfully!")

    def edit_screenshot(self):
        if self.last_screenshot:
            self.editor_window = tk.Toplevel(self.root)
            self.editor_window.title("Edit Screenshot")
            self.editor_window.geometry("800x600")

            self.image_copy = self.last_screenshot.copy()
            self.tk_image = ImageTk.PhotoImage(self.image_copy)

            self.canvas_edit = tk.Canvas(self.editor_window, width=self.tk_image.width(), height=self.tk_image.height())
            self.canvas_edit.pack()

            self.canvas_edit.create_image(0, 0, anchor="nw", image=self.tk_image)
            self.canvas_edit.bind("<B1-Motion>", self.draw_on_image)

            self.draw = ImageDraw.Draw(self.image_copy)

            color_btn = tk.Button(self.editor_window, text="Choose Color", command=self.choose_color)
            color_btn.pack(pady=10)

            save_btn = tk.Button(self.editor_window, text="Update Screenshot", command=self.update_screenshot)
            save_btn.pack(pady=10)

            self.pen_color = 'red'

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Pen Color")
        if color[1]:
            self.pen_color = color[1]

    def draw_on_image(self, event):
        x, y = event.x, event.y
        self.draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=self.pen_color, outline=self.pen_color)
        self.tk_image = ImageTk.PhotoImage(self.image_copy)
        self.canvas_edit.create_image(0, 0, anchor="nw", image=self.tk_image)

    def update_screenshot(self):
        self.last_screenshot = self.image_copy
        self.editor_window.destroy()
        messagebox.showinfo("Updated", "Screenshot updated!")

    def save_screenshot(self):
        if self.last_screenshot:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.last_screenshot.save(file_path)
                messagebox.showinfo("Saved", f"Screenshot saved to:\n{file_path}")
        else:
            messagebox.showwarning("No Screenshot", "No screenshot to save!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotTool(root)
    root.mainloop()
