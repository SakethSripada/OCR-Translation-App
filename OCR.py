import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from googletrans import Translator, LANGUAGES


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

        self.translate_button = ttk.Button(self.root, text="TRANSLATE", command=self.translate_window)
        self.translate_button.pack()

        self.textbox = tk.Text(self.root, height=5.5, font=("Arial", 16), foreground="black", background="white")
        self.textbox.pack(padx=10, pady=10)

        self.textbox2 = tk.Text(self.root, height=5.5, font=("Arial", 16), foreground="black", background="white")
        self.textbox2.pack(padx=10, pady=10)

        self.filename = ""

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
            messagebox.showinfo("Info", "File not selected. Please select a file and try again.")

    def translate_window(self):
        translate_window = tk.Toplevel(self.root)
        translate_window.title("Translate Text")
        translate_window.geometry("1000x200")

        language = tk.StringVar(translate_window)
        language.set("es")

        select_language_label = ttk.Label(translate_window, text="Select Language:")
        select_language_label.pack()

        whitespace = tk.Label(translate_window, text="")
        whitespace.pack()

        dropdown = ttk.OptionMenu(translate_window, language, "es", *LANGUAGES.keys())
        dropdown.pack()

        whitespace = tk.Label(translate_window, text="")
        whitespace.pack()

        translate_button = ttk.Button(translate_window, text="Translate",
                                      command=lambda: self.translate_text(language.get()))
        translate_button.pack()

    def translate_text(self, lang_code):
        translator = Translator()
        original_text = self.textbox.get("1.0", tk.END)
        translated_text = translator.translate(original_text, dest=lang_code).text
        self.textbox2.delete("1.0", tk.END)
        self.textbox2.insert(tk.END, translated_text)


OCR()
