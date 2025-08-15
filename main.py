import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font

# === Theme Colors ===
BG_COLOR = "#1e0f3c"       # Dark purple background
PANEL_BG = "#2b1a55"       # Panel dark background (NTLite feel)
FG_COLOR = "#e0c3ff"       # Light purple text
BTN_COLOR = "#7b3fe4"      # Button purple
BTN_HOVER = "#9a5eff"      # Button hover glow
LOG_BG = "#2a1a5c"         # Log background
LOG_FG = "#ffffff"         

class EXEConvertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EXEConvert - WGE + NTLite Themed")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Variables
        self.file_path = tk.StringVar()
        self.icon_path = tk.StringVar()
        self.one_file = tk.BooleanVar(value=True)
        self.console = tk.BooleanVar(value=True)

        # Fonts
        self.title_font = font.Font(family="Press Start 2P", size=18)
        self.log_font = font.Font(family="Courier", size=10)

        self.create_widgets()
        self.setup_drag_and_drop()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="EXEConvert", font=self.title_font, bg=BG_COLOR, fg=FG_COLOR)
        title.pack(pady=10)

        # File selection panel
        file_panel = tk.Frame(self.root, bg=PANEL_BG, padx=10, pady=10)
        file_panel.pack(pady=5, padx=10, fill="x")
        tk.Label(file_panel, text="Python File:", bg=PANEL_BG, fg=FG_COLOR).pack(side="left")
        tk.Entry(file_panel, textvariable=self.file_path, width=40, bg=LOG_BG, fg=LOG_FG).pack(side="left", padx=5)
        browse_btn = tk.Button(file_panel, text="Browse", bg=BTN_COLOR, fg=LOG_FG, command=self.browse_file)
        browse_btn.pack(side="left")
        self.add_hover_effect(browse_btn)

        # Icon selection panel
        icon_panel = tk.Frame(self.root, bg=PANEL_BG, padx=10, pady=10)
        icon_panel.pack(pady=5, padx=10, fill="x")
        tk.Label(icon_panel, text="Icon (Optional):", bg=PANEL_BG, fg=FG_COLOR).pack(side="left")
        tk.Entry(icon_panel, textvariable=self.icon_path, width=35, bg=LOG_BG, fg=LOG_FG).pack(side="left", padx=5)
        icon_btn = tk.Button(icon_panel, text="Browse", bg=BTN_COLOR, fg=LOG_FG, command=self.browse_icon)
        icon_btn.pack(side="left")
        self.add_hover_effect(icon_btn)

        # Options panel
        options_panel = tk.Frame(self.root, bg=PANEL_BG, padx=10, pady=10)
        options_panel.pack(pady=10)
        tk.Checkbutton(options_panel, text="One-File Mode", variable=self.one_file, bg=PANEL_BG, fg=FG_COLOR, selectcolor=PANEL_BG).pack(side="left", padx=10)
        tk.Checkbutton(options_panel, text="Show Console", variable=self.console, bg=PANEL_BG, fg=FG_COLOR, selectcolor=PANEL_BG).pack(side="left", padx=10)

        # Convert button
        convert_btn = tk.Button(self.root, text="Convert to EXE", bg=BTN_COLOR, fg=LOG_FG, font=("Arial", 12), command=self.convert)
        convert_btn.pack(pady=10)
        self.add_hover_effect(convert_btn)

        # Log panel
        log_panel = tk.Frame(self.root, bg=PANEL_BG, padx=5, pady=5)
        log_panel.pack(padx=10, fill="both", expand=True)
        self.log = scrolledtext.ScrolledText(log_panel, height=12, bg=LOG_BG, fg=LOG_FG, font=self.log_font)
        self.log.pack(fill="both", expand=True)

    def add_hover_effect(self, widget):
        def on_enter(e):
            widget['bg'] = BTN_HOVER
        def on_leave(e):
            widget['bg'] = BTN_COLOR
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py *.pyw")])
        if file:
            self.file_path.set(file)

    def browse_icon(self):
        icon = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if icon:
            self.icon_path.set(icon)

    def log_message(self, message):
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)
        self.root.update()

    def convert(self):
        py_file = self.file_path.get()
        if not py_file or not os.path.isfile(py_file):
            messagebox.showerror("Error", "Please select a valid Python file.")
            return

        # Build PyInstaller command
        cmd = ["pyinstaller", f'"{py_file}"']
        if self.one_file.get():
            cmd.append("--onefile")
        if not self.console.get():
            cmd.append("--noconsole")
        icon = self.icon_path.get()
        if icon and os.path.isfile(icon):
            cmd.append(f'--icon="{icon}"')

        self.log_message(f"Running: {' '.join(cmd)}")
        try:
            subprocess.run(" ".join(cmd), shell=True, check=True)
            self.log_message("✅ Conversion finished successfully!")
            messagebox.showinfo("Success", "EXE file created successfully!")
        except subprocess.CalledProcessError as e:
            self.log_message(f"❌ Error: {e}")
            messagebox.showerror("Error", "Conversion failed. See log for details.")

    def setup_drag_and_drop(self):
        # Drag-and-drop support (Windows only, requires tkinterdnd2)
        def drop(event):
            path = event.data.strip("{}")
            if path.lower().endswith((".py", ".pyw")):
                self.file_path.set(path)
                self.log_message(f"File dropped: {path}")

        try:
            import tkinterdnd2
            self.root = tkinterdnd2.TkinterDnD.Tk()
            self.root.drop_target_register(tkinterdnd2.DND_FILES)
            self.root.dnd_bind('<<Drop>>', drop)
        except ImportError:
            self.log_message("Drag-and-drop not available (tkinterdnd2 not installed)")

if __name__ == "__main__":
    root = tk.Tk()
    app = EXEConvertApp(root)
    root.mainloop()
