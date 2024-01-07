import os
import shutil
import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import time
from ttkthemes import ThemedTk

class Game:
    def __init__(self, name, is_fsr_compatible, default_path):
        self.name = name
        self.is_fsr_compatible = is_fsr_compatible
        self.default_path = default_path

def check_game_compatibility(game):
    print(f"Checking compatibility for {game.name}...")
    time.sleep(1)
    return game.is_fsr_compatible

def enable_amd_fsr_simulation(progress_var, progress_label, progress_bar, activation_button, game_path, inject_gpu_plugin):
    def update_progress():
        nonlocal activation_button
        progress_label.config(text=activation_steps[progress_var.get()])
        progress_var.set(progress_var.get() + 1)
        progress_bar["value"] = progress_var.get()

        if progress_var.get() < len(activation_steps):
            root.after(2000, update_progress)
        else:
            messagebox.showinfo("AMD FSR Activation", "AMD FSR has been successfully enabled!")
            activation_button.config(state=tk.NORMAL)
            progress_label.config(text="")
            progress_var.set(0)
            progress_bar["value"] = 0

            # Open Instagram link after activation
            os.system("start https://instagram.com/c4gwn")

    try:
        activation_steps = [
            "Step 1: Backup original files",
            "Step 2: Copy FSR files to game directory",
            "Step 3: Inject GPU Plugin" if inject_gpu_plugin else "Step 3: Finish"
        ]

        progress_var.set(0)
        progress_bar["maximum"] = len(activation_steps)
        progress_bar["value"] = 0

        for i, step in enumerate(activation_steps):
            progress_label.config(text=f"Step {i + 1}: {step}")
            time.sleep(2)
            progress_var.set(i + 1)
            progress_bar["value"] = i + 1

        root.after(2000, update_progress)

        fsr_files = [
            "FSR2FSR3.asi",
            "lfz.sl.dlss.dll",
            "winmm.dll",
            "winmm.ini"
        ]

        for file in fsr_files:
            source_path = os.path.join(os.getcwd(), file)
            destination_path = os.path.join(game_path, file)
            shutil.copy2(source_path, destination_path)

        if inject_gpu_plugin:
            gpu_config_file = "fsr2fsr3.config.toml"
            source_gpu_config_path = os.path.join(os.getcwd(), gpu_config_file)
            destination_gpu_config_path = os.path.join(game_path, gpu_config_file)
            shutil.copy2(source_gpu_config_path, destination_gpu_config_path)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the activation process: {e}")
    finally:
        activation_button.config(state=tk.NORMAL)
        progress_label.config(text="")
        progress_var.set(0)
        progress_bar["value"] = 0

def remove_fsr_mod(game_path):
    fsr_files = [
        "FSR2FSR3.asi",
        "lfz.sl.dlss.dll",
        "winmm.dll",
        "winmm.ini",
        "fsr2fsr3.config.toml",
    ]

    for file in fsr_files:
        file_path = os.path.join(game_path, file)
        if os.path.exists(file_path):
            os.remove(file_path)

def browse_folder():
    initial_path = "C:/Program Files (x86)/Steam/steamapps/common"  # Başlangıç konumu
    folder_selected = filedialog.askdirectory(initialdir=initial_path)
    game_folder_entry.delete(0, tk.END)
    game_folder_entry.insert(0, folder_selected)


def simulate_amd_fsr():
    selected_game_name = games_combobox.get()

    if selected_game_name == "Select a Game":
        messagebox.showwarning("Game Selection", "Please select a game.")
    else:
        selected_game = next((game for game in games if game.name == selected_game_name), None)

        if selected_game:
            game_path = game_folder_entry.get()

            if not os.path.exists(game_path):
                messagebox.showerror("Folder Error", "The specified folder does not exist.")
                return

            if check_game_compatibility(selected_game):
                messagebox.showinfo("Compatibility", f"{selected_game.name} is compatible with AMD FSR.")
                activation_button.config(state=tk.DISABLED)
                inject_gpu_plugin_var.set(True)  # Auto-check the "Inject GPU Plugin" checkbox
                threading.Thread(target=enable_amd_fsr_simulation, args=(progress_var, progress_label, progress_bar, activation_button, game_path, inject_gpu_plugin_var.get())).start()
            else:
                messagebox.showwarning("Compatibility", f"{selected_game.name} is not compatible with AMD FSR.")
        else:
            messagebox.showerror("Game Error", "Invalid game selection.")

def remove_fsr_mod_button():
    selected_game_name = games_combobox.get()

    if selected_game_name == "Select a Game":
        messagebox.showwarning("Game Selection", "Please select a game.")
    else:
        selected_game = next((game for game in games if game.name == selected_game_name), None)

        if selected_game:
            game_path = game_folder_entry.get()

            if not os.path.exists(game_path):
                messagebox.showerror("Folder Error", "The specified folder does not exist.")
                return

            answer = messagebox.askokcancel("Remove FSR Mod", f"Are you sure you want to remove FSR Mod from {selected_game.name}?", icon='warning', parent=root)

            if answer:
                remove_fsr_mod(game_path)

# ThemedTk provides a more modern look for the GUI
root = ThemedTk(theme="arc")  # You can experiment with other available themes
root.title("AMD FSR Enabler Simulator")

# Load FSR logo
fsr_logo_path = "FSR.JPG"  # Replace with the actual path to the FSR logo
fsr_logo = Image.open(fsr_logo_path)
fsr_logo = fsr_logo.resize((200, 100), Image.ANTIALIAS)
fsr_logo = ImageTk.PhotoImage(fsr_logo)

# Simulate a list of games with their compatibility
games = [
    Game("Select a Game", False, ""),
    Game("The Last Of Us Part I", True, "C:\\Program Files (x86)\\Steam\\steamapps\\common\\The Last Of Us Part I"),
    Game("Dead Space", True, ""),
    Game("Hogwarts Legacy", True, ""),
    Game("Cyberpunk 2077", True, "E:\\SteamLibrary\\steamapps\\common\\Cyberpunk 2077\\bin\\x64"),
    Game("The Witcher 3", True, ""),
    Game("Marvel's Spider-Man Remastered", True, ""),
    Game("Dying Light 2", True, ""),
    Game("Alan Wake 2", True, ""),
    Game("Ready or Not", True, ""),
]

# GUI elements
fsr_logo_label = ttk.Label(root, image=fsr_logo)
fsr_logo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# New label for "Developed by" text
developed_by_label = ttk.Label(root, text="Developed by @c4gwn", font=("Helvetica", 8), foreground="gray")
developed_by_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

games_combobox = ttk.Combobox(root, values=[game.name for game in games], state="readonly")
games_combobox.current(0)
games_combobox.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

game_folder_label = ttk.Label(root, text="Game Folder:")
game_folder_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

game_folder_entry = ttk.Entry(root, width=50)
game_folder_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

browse_button = ttk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=2, column=2, padx=10, pady=10)

inject_gpu_plugin_var = tk.BooleanVar()
inject_gpu_plugin_checkbox = ttk.Checkbutton(root, text="Inject GPU Plugin", variable=inject_gpu_plugin_var)
inject_gpu_plugin_checkbox.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

activation_button = ttk.Button(root, text="Activate AMD FSR3", command=simulate_amd_fsr)
activation_button.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

remove_fsr_mod_button = ttk.Button(root, text="Remove FSR Mod", command=remove_fsr_mod_button)
remove_fsr_mod_button.grid(row=5, column=0, padx=10, pady=10, columnspan=3)

progress_var = tk.IntVar()
progress_label = ttk.Label(root, text="")
progress_label.grid(row=6, column=0, padx=10, pady=10, columnspan=3)

progress_bar = ttk.Progressbar(root, mode="determinate", length=300)
progress_bar.grid(row=7, column=0, padx=10, pady=10, columnspan=3)

root.mainloop()
