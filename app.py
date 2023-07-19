import tkinter as tk
from tkinter import filedialog
import subprocess

# get file input
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Word files","*.docx")])
    file_name.configure(text=file_path)

# convert using bash command
def convert(file):
    if file not in ("No file yet.", None):
        command = f"doc2pdf \"{file}\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        message_window_1 = tk.Tk()
        if result.returncode == 0:
            message1 = tk.Label(message_window_1, text="Conversion successful.")

            # after successful conversion, copy the converted files to a directory in the home folder
            new_file = file[:-4] + "pdf"
            command = f"mkdir -p ~/\"Converted DOCX Files\" && mv \"{new_file}\" ~/\"Converted DOCX Files\""
            subprocess.run(command, shell=True, capture_output=True, text=True)
            message2 = tk.Label(message_window_1, text="Moved to ~/\"Converted DOCX Files\"")

            # open PDF file immediately after
            command = f"basename \"{new_file}\""
            basename = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.removesuffix("\n")

            command = f"open ~/\"Converted DOCX Files\"/\"{basename}\""
            subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            message1 = tk.Label(message_window_1, text="Conversion failed.")
        message1.pack()
        message2.pack()


# display window
root = tk.Tk()

# Open File frame
open_frame = tk.Frame(root)
open_frame.grid(row=0, column=0)

open_button = tk.Button(open_frame, text="Open File", command=open_file)
open_button.grid(row=0, column=0)

file_name = tk.Label(open_frame, text="No file yet.")
file_name.grid(row=0, column=1)

# Convert frame
convert_button = tk.Button(root, text="Convert", command=lambda: convert(file_name.cget("text")))
convert_button.grid(row=1, column=0)

root.mainloop()