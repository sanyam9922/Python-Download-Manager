import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class Downloader:
    def __init__(self):
        self.save_to = ""
        self.window = tk.Tk()
        self.window.title("Gui Downloader")
        self.window.geometry("420x200")

        # url_label url_entry browse_button download_button progress_bar progress_label location_entry
        self.url_label = tk.Label(self.window, text="Enter URL:")
        self.url_label.grid(row=1, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.grid(row=1, column=1)
        self.browse_button = tk.Button(self.window, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=2, column=0, padx=10, pady=10)
        self.location_entry = tk.Entry(self.window, width=50)
        self.location_entry.grid(row=2, column=1)

        self.download_button = tk.Button(self.window, text="Download", command=self.download, width=40)
        self.download_button.grid(row=3, column=1)

        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", maximum=100, length=300)
        self.progress_bar.grid(row=5, column=1, padx=10, pady=10)
        self.progress_label = tk.Label(self.window, text="")
        self.progress_label.grid(row=5, column=0, padx=10, pady=10)
        self.window.mainloop()

    def browse_file(self):
        self.save_to = filedialog.asksaveasfilename(initialfile=self.url_entry.get().split("/")[-1].split("?")[0])
        self.location_entry.insert(0, self.save_to)
        self.save_to = self.location_entry.get()
        print(self.save_to)

    def download(self):
        url = self.url_entry.get()
        try:
            response = requests.get(url, stream=True)
            file_size = int(response.headers.get("content-length"))
            file_name = self.url_entry.get().split("/")[-1].split("?")[0]
            self.save_to = self.location_entry.get()
            if self.save_to != "":
                file_name = self.save_to
            print(file_name)
            print(file_size)
            block_size = 4069
            self.progress_bar["value"] = 0

            with open(file_name, "wb") as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    percentage = (os.path.getsize(file_name)/file_size)*100
                    self.progress_bar["value"] = percentage
                    print(os.path.getsize(file_name), "/", file_size)
                    self.progress_label.config(text=f"{round(percentage)}%")
                    self.window.update()

                print(os.path.getsize(file_name), "/", file_size)
                messagebox.showinfo("Info", "Download Complete")
                self.progress_bar["value"] = 0
                self.progress_label.config(text="Downloaded", fg="white", bg="green")

        except:
            print("Invalid URL")
            messagebox.showerror("Error", "Invalid URL")


Downloader()
