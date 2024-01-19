import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from googletrans import Translator, LANGUAGES
import pyttsx3


class OCR:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OCR")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.root.geometry("1000x500")

        ttk.Label(self.root, text="OCR Application", font=("Arial", 18)).pack()

        self.menubar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Quit App", command=self.quit_app)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit Immediately", command=self.quit_app_imm)

        self.download_menu = tk.Menu(self.menubar, tearoff=0)
        self.download_menu.add_command(label="Download OCR", command=self.write_file_ocr)

        self.download_menu.add_separator()
        self.download_menu.add_command(label="Download Translation", command=self.write_file_trans)

        self.menubar.add_cascade(menu=self.file_menu, label="File")
        self.menubar.add_cascade(menu=self.download_menu, label="Download")

        self.root.config(menu=self.menubar)

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

        self.speak_button = ttk.Button(self.root, text="HEAR TEXT", command=self.speak_text)
        self.speak_button.pack()

        self.textbox = tk.Text(self.root, height=5.5, font=("Arial", 16), foreground="black", background="white")
        self.textbox.pack(padx=10, pady=10)

        self.textbox2 = tk.Text(self.root, height=5.5, font=("Arial", 16), foreground="black", background="white")
        self.textbox2.pack(padx=10, pady=10)

        self.filename = ""

        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

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

        window_width = 400
        window_height = 200
        translate_window.geometry(f"{window_width}x{window_height}")

        screen_width = translate_window.winfo_screenwidth()
        screen_height = translate_window.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        translate_window.geometry(f"+{int(x)}+{int(y)}")

        language = tk.StringVar(translate_window)
        language.set("es")

        select_language_label = ttk.Label(translate_window, text="Select Language:")
        select_language_label.pack()

        whitespace = tk.Label(translate_window, text="")
        whitespace.pack()
        language_list = list(LANGUAGES.values())
        dropdown = ttk.OptionMenu(translate_window, language, "spanish", *language_list)
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

    def write_file_ocr(self):
        text_content = self.textbox.get("1.0", tk.END)
        if text_content.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),
                                                                                         ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text_content)
        else:
            error_win = tk.Toplevel(self.root)
            error_win.title("ERROR")

            window_width = 400
            window_height = 200

            error_win.geometry(f"{window_width}x{window_height}")

            error_msg = ttk.Label(error_win, text="There is no OCR text to download. "
                                                  "Please upload an image for OCR and try again.", font=("Arial", 27),
                                  wraplength=window_width, foreground="red")
            error_msg.pack()

    def write_file_trans(self):
        text_content = self.textbox2.get("1.0", tk.END)
        if text_content.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),
                                                                                         ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text_content)
        else:
            error_win = tk.Toplevel(self.root)
            error_win.title("ERROR")

            window_width = 400
            window_height = 200

            error_win.geometry(f"{window_width}x{window_height}")

            error_msg = ttk.Label(error_win, text="There is no translated text to download. "
                                                  "Please translate text and try again.", font=("Arial", 30),
                                  wraplength=window_width, foreground="red")
            error_msg.pack()

    def quit_app(self):
        if messagebox.askyesno(title="Close Application?", message="Are you sure you want to exit?"):
            self.root.destroy()

    def quit_app_imm(self):
        self.root.destroy()

    def speak_text(self):
        engine = pyttsx3.init()
        text = self.textbox.get("1.0", tk.END)
        engine.say(text)
        engine.runAndWait()


OCR()
