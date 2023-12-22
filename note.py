import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class NoteApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Note Taking App")

        self.text_widget = tk.Text(self.master, wrap="word", width=150, height=30)
        self.text_widget.pack(pady=10)

        # Create menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Create file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_note)
        self.file_menu.add_command(label="Open", command=self.open_note)

    def save_note(self):
        note = self.text_widget.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(note)
                messagebox.showinfo("Note Saved", "Note has been saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_note(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            try:
                with open(file_path, "r") as file:
                    note = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, note)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
