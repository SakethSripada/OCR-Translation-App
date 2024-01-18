import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image


class OCR:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OCR")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.root.geometry("1000x500")

        ttk.Label(self.root, text="OCR Application", font=("Arial", 18)).pack()

        self.whitespace = tk.Label(self.root, text="")
        self.whitespace.pack()

        self.upload_button = ttk.Button(self.root, text="UPLOAD FILE", command=self.upload_file)
        self.upload_button.pack()

        self.whitespace = tk.Label(self.root, text="")
        self.whitespace.pack()

        self.ocr_button = ttk.Button(self.root, text="PERFORM OCR", command=self.perform_ocr)
        self.ocr_button.pack()

        self.whitespace = tk.Label(self.root, text="")
        self.whitespace.pack()

        self.textbox = tk.Text(self.root, height=15, font=("Arial", 16), foreground="black", background="white")
        self.textbox.pack(padx=10, pady=10)

        self.filename = ""  # To store the path of the selected file

        self.root.mainloop()

    def upload_file(self):
        self.filename = filedialog.askopenfilename()
        if self.filename:
            print(f"Selected file: {self.filename}")
        else:
            print("File not selected")

    def perform_ocr(self):
        if self.filename:
            try:
                image = Image.open(self.filename)
                text = pytesseract.image_to_string(image)
                self.textbox.delete(1.0, tk.END)  
                self.textbox.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showinfo("Info", "Please select a file first")


OCR()
