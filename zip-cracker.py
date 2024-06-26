import zipfile
from time import time
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import os

class ZipCracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Zip Cracker")

        self.zip_label = tk.Label(root, text="Zip file:")
        self.zip_label.pack()

        self.zip_entry = tk.Entry(root, width=50)
        self.zip_entry.pack()

        self.zip_button = tk.Button(root, text="Browse", command=self.select_zip_file)
        self.zip_button.pack()

        self.wordlist_label = tk.Label(root, text="Wordlist:")
        self.wordlist_label.pack()

        self.wordlist_entry = tk.Entry(root, width=50)
        self.wordlist_entry.pack()

        self.wordlist_button = tk.Button(root, text="Browse", command=self.select_wordlist)
        self.wordlist_button.pack()

        self.start_button = tk.Button(root, text="Start cracking", command=self.start_cracking)
        self.start_button.pack()

        self.result_label = tk.Label(root, text="", fg="black")
        self.result_label.pack()

        self.progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack()

    def select_zip_file(self):
        zip_file = filedialog.askopenfilename(title="Select zip file", filetypes=[("Zip files", "*.zip")])
        self.zip_entry.delete(0, tk.END)
        self.zip_entry.insert(0, zip_file)

    def select_wordlist(self):
        wordlist = filedialog.askopenfilename(title="Select wordlist", filetypes=[("Text files", "*.txt")])
        self.wordlist_entry.delete(0, tk.END)
        self.wordlist_entry.insert(0, wordlist)

    def crack_password(self, zip_file, wordlist):
        try:
            myZip = zipfile.ZipFile(zip_file)
        except zipfile.BadZipfile:
            self.result_label.config(text="Error: Invalid zip file.", fg="red")
            return

        timeStart = time()
        with open(wordlist, "r") as f:
            passes = f.readlines()
            total_passes = len(passes)
            for pass_count, x in enumerate(passes):
                password = x.strip()
                self.result_label.config(text=f"Trying password: {password} ({pass_count+1}/{total_passes})")
                self.root.update_idletasks()
                self.progress_bar.config(value=(pass_count+1)/total_passes*100)
                self.progress_bar.update_idletasks()
                try:
                    myZip.set_password(password.encode())
                    zip_folder = os.path.splitext(os.path.basename(zip_file))[0]
                    os.makedirs(zip_folder, exist_ok=True)
                    myZip.extractall(zip_folder)
                    totalTime = time() - timeStart
                    self.result_label.config(text=f"Password correct: \"{password}\"", fg="green")
                    print(f"Password correct: \"{password}\"")
                    return
                except Exception as e:
                    if str(e) == 'Bad password for file':
                        pass
                    elif 'Error -3 while decompressing' in str(e):
                        pass  # TODO: properly handle exceptions?
                    else:
                        print(e)
        self.result_label.config(text="Sorry, password not found.", fg="red")

    def start_cracking(self):
        zip_file = self.zip_entry.get()
        wordlist = self.wordlist_entry.get()
        self.result_label.config(text="Cracking...")
        self.progress_bar.config(value=0)
        threading.Thread(target=self.crack_password, args=(zip_file, wordlist)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipCracker(root)
    root.mainloop()