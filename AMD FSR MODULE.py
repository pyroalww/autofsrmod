import os
import shutil
import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import time
from ttkthemes import ThemedTk
import zipfile
app_version = "V3.2 Linux"
class Game:
    def __init__(self, name, is_fsr_compatible, default_path):
        self.name = name
        self.is_fsr_compatible = is_fsr_compatible
        self.default_path = default_path

version_mapping = {
    "0.9.0L*z (220)": "LZ090_220.zip",
    "0.8.0L*z (220)": "0.8.0lz_220.zip",
    "0.7.6 L*z (220)": "0.7.6lz_220.zip",
    "0.7.6 L*z (212)": "0.7.6lz_212.zip",
    "0.8.1 Nukem9": "081nuke.zip",
    "0.9.0 Nukem9": "090nuke.zip"
}
def informationatstartup():
    messagebox.showinfo("@c4gwn", "This version developed for Unix based systems. (like decks.)")
def check_game_compatibility(game):
    print(f"Checking compatibility for {game.name}...")
    time.sleep(1)
    return game.is_fsr_compatible
def is_mod_installed(game_path):
    mod_files = [
        "dlssg_to_fsr3_amd_is_better.dll",
        "nvngx.dll",
        "FSR2FSR3.asi",
        "lfz.sl.dlls.dll",
        "winmm.dll",
        "winmm.ini",
        "fsr2fsr3.config.toml"
    ]

    for file in mod_files:
        if not os.path.exists(os.path.join(game_path, file)):
            return False

    return True
informationatstartup()
def update_info_text():
    selected_game_name = games_combobox.get()
    selected_game = next((game for game in games if game.name == selected_game_name), None)

    if selected_game:
        game_path = game_folder_entry.get()

        if not os.path.exists(game_path):
            info_text.set("The specified folder does not exist.")
            return

        if is_mod_installed(game_path):
            info_text.set(f"{selected_game.name}: Mod is already installed.")
        else:
            info_text.set(f"{selected_game.name}: Mod is not installed.")
    else:
        info_text.set("Select a Game")

def browse_folder():
    initial_path = "C:/Program Files (x86)/Steam/steamapps/common"
    folder_selected = filedialog.askdirectory(initialdir=initial_path)
    game_folder_entry.delete(0, tk.END)
    game_folder_entry.insert(0, folder_selected)
    update_info_text()

def enable_amd_fsr_simulation(progress_var, progress_label, progress_bar, activation_button, game_path, inject_gpu_plugin):
    selected_version = version_combobox.get()

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

            os.system("start https://instagram.com/c4gwn")

    try:
        activation_steps = [
            " Backup original files",
            f" Extracting files for {selected_version}",
            f" Step 3: Copy FSR files to game directory {game_path}",
            " Inject GPU Plugin" if inject_gpu_plugin else " Finish"
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

        cleaned_version = "".join(c if c.isalnum() or c == '.' else '_' for c in selected_version)
        zip_filename = version_mapping.get(selected_version)

        if zip_filename:
            zip_path = os.path.join(os.getcwd(), zip_filename)

            # Yeni çıkartma işlemi
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(game_path)

            files_to_move = [
                "dlssg_to_fsr3_amd_is_better.dll",
                "nvngx.dll",
                "FSR2FSR3.asi",
                "lfz.sl.dlls.dll",
                "winmm.dll",
                "winmm.ini",
                "fsr2fsr3.config.toml"
            ]

            for file in files_to_move:
                source_path = os.path.join(game_path, file)
                destination_path = os.path.join(game_path, file)

                if os.path.exists(destination_path):
                    os.remove(destination_path)  # Eğer varsa, önceki dosyayı sil

                shutil.move(source_path, destination_path)

        if inject_gpu_plugin:
            gpu_config_file = "fsr2fsr3.config.toml"
            destination_gpu_config_path = os.path.join(game_path, gpu_config_file)

            os.remove(destination_gpu_config_path)  # Eğer varsa, önceki dosyayı sil

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the activation process: {e}")

        # Debug çıktısı ekleyelim
        print("Debug Information:")
        print(f"selected_version: {selected_version}")
        print(f"zip_filename: {zip_filename}")
        print(f"zip_path: {zip_path}")
        print(f"game_path: {game_path}")

    finally:
        activation_button.config(state=tk.NORMAL)
        progress_label.config(text="")
        progress_var.set(0)
        progress_bar["value"] = 0

def remove_fsr_mod(game_path):
    fsr_files = [
        "dlssg_to_fsr3_amd_is_better.dll",
        "nvngx.dll",
        "FSR2FSR3.asi",
        "lfz.sl.dlss.dll",
        "winmm.dll",
        "winmm.ini",
        "fsr2fsr3.config.toml"
    ]

    for file in fsr_files:
        file_path = os.path.join(game_path, file)
        if os.path.exists(file_path):
            os.remove(file_path)

    if inject_gpu_plugin_var.get():
        gpu_config_file = "fsr2fsr3.config.toml"
        gpu_config_path = os.path.join(game_path, gpu_config_file)
        if os.path.exists(gpu_config_path):
            os.remove(gpu_config_path)



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
                inject_gpu_plugin_var.set(True)  # GPU inject otomatik işaretleme
                threading.Thread(target=enable_amd_fsr_simulation,
                                 args=(progress_var, progress_label, progress_bar, activation_button, game_path,
                                       inject_gpu_plugin_var.get())).start()

                check_installed_mods(game_path)
            else:
                messagebox.showwarning("Compatibility", f"{selected_game.name} is not compatible with AMD FSR.")
        else:
            messagebox.showerror("Game Error", "Invalid game selection.")

def check_installed_mods(game_path):
    mod_installed_message = ""

    if os.path.exists(os.path.join(game_path, "dlssg_to_fsr3_amd_is_better.dll")):
        mod_installed_message = "Nukem9 Mod installed"
    elif os.path.exists(os.path.join(game_path, "FSR2FSR3.asi")):
        mod_installed_message = "L*z Mod installed"
    else:
        mod_installed_message = "Mods are not yet downloaded."

    messagebox.showinfo("Installed Mods", mod_installed_message)

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

root = ThemedTk(theme="arc")
root.title("Auto FSR3 Mod Installer")
info1 = "Do not worry about WinError2. Its just a bug :)"
# Load FSR logo
fsr_logo_path = "FSR.JPG"
fsr_logo = Image.open(fsr_logo_path)
fsr_logo = fsr_logo.resize((200, 100), Image.ANTIALIAS)
fsr_logo = ImageTk.PhotoImage(fsr_logo)

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
    Game("Other Game [Not guaranteed]", True, "")
]

fsr_logo_label = ttk.Label(root, image=fsr_logo)
fsr_logo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

developed_by_label = ttk.Label(root, text="Developed by @c4gwn", font=("Helvetica", 8), foreground="gray")
developed_by_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

games_combobox = ttk.Combobox(root, values=[game.name for game in games], state="readonly", postcommand=update_info_text)
games_combobox.current(0)
games_combobox.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

game_folder_label = ttk.Label(root, text="Game Folder:")
game_folder_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

game_folder_entry = ttk.Entry(root, width=50)
game_folder_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

browse_button = ttk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=2, column=2, padx=10, pady=10)

version_label = ttk.Label(root, text="Select Version:")
version_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

version_combobox = ttk.Combobox(root, values=[version for version in version_mapping.keys()], state="readonly")
version_combobox.current(0)
version_combobox.grid(row=3, column=1, padx=10, pady=10, sticky="w", columnspan=2)

inject_gpu_plugin_var = tk.BooleanVar()
inject_gpu_plugin_checkbox = ttk.Checkbutton(root, text="Inject GPU Plugin", variable=inject_gpu_plugin_var)
inject_gpu_plugin_checkbox.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

activation_button = ttk.Button(root, text="Install AMD FSR3", command=simulate_amd_fsr)
activation_button.grid(row=5, column=0, padx=10, pady=10, columnspan=3)

remove_fsr_mod_button = ttk.Button(root, text="Remove FSR Mod", command=remove_fsr_mod_button)
remove_fsr_mod_button.grid(row=6, column=0, padx=10, pady=10, columnspan=3)

progress_var = tk.IntVar()
progress_label = ttk.Label(root, text="")
progress_label.grid(row=7, column=0, padx=10, pady=10, columnspan=3)

progress_bar = ttk.Progressbar(root, mode="determinate", length=300)
progress_bar.grid(row=8, column=0, padx=10, pady=10, columnspan=3)

info_text = tk.StringVar()
info_label = ttk.Label(root, textvariable=info_text, font=("Helvetica", 10), foreground="blue")
info_label.grid(row=9, column=0, padx=10, pady=10, columnspan=3)
version_label = ttk.Label(root, text=f"Version: {app_version}", font=("Helvetica", 12), foreground="green")
version_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
info1 = tk.StringVar()
info_label1 = ttk.Label(root, textvariable=info1, font=("Helvetica", 10), foreground="blue")
info_label1.grid(row=11, column=0, padx=12, pady=11, columnspan=4)

root.mainloop()
