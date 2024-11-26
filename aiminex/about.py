import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkFont as ctkfont
from PIL import Image, ImageTk


# Function to create the About win
def show_about():
    about_win = ctk.CTkToplevel()
    about_win.title("About")
    
    # Set the size of the About win
    win_w = 400
    win_h = 350
    about_win.geometry(f"{win_w}x{win_h}")

    # Center the win on the screen
    screen_w = about_win.winfo_screenwidth()
    screen_h = about_win.winfo_screenheight()
    x = (screen_w // 2) - (win_w // 2)
    y = (screen_h // 2) - (win_h // 2)
    about_win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # Make the About window stay on top
    about_win.attributes("-topmost", True)
    
    # Load the image to be displayed at the top
    image_path = 'images/favicons/favicon.png'
    try:
        image = Image.open(image_path)
        image = image.resize((64, 64))  # Resize image to fit (adjust as needed)
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image at the top of the About window
        image_label = tk.Label(about_win, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)  # Add some padding around the image

    except Exception as e:
        print(f"Error loading image for About window: {e}")

    # Define bold and normal text
    bold_font = ("Arial", 14, "bold")
    normal_font = ("Arial", 12)

    title_label = ctk.CTkLabel(about_win, text="AIMinex", font=bold_font)
    title_label.pack(pady=(10, 5))

    version_label = ctk.CTkLabel(about_win, text="Version 1.0", font=normal_font)
    version_label.pack()
    description = "An Open-Source, Cross-Platform GUI for Geochemical and Mineral Exploration Data Analysis and Visualization Using AI."
    description_label = ctk.CTkLabel(about_win, text=description, font=normal_font,wraplength=300)
    description_label.pack(pady=(5, 20))
    underlined_text = ctkfont(family="Arial", size=14, underline=True)
    
    contribution_label = ctk.CTkLabel(about_win, text="Contributors:", font=underlined_text)
    contribution_label.pack(pady=5)
    
    # Developer list
    developers = ["Maintainer & Developer: Hom Nath Gharti", "Developer: Tiger Fan", "Data Consultation: Gema Olivo & Adriana Guatame-Garcia"]
    
    # Combine developers into a single string with one developer per line
    developer_text = "\n".join(developers)
    
    # Create a label to display developers
    developer_label = ctk.CTkLabel(about_win, text=developer_text, font=("Arial", 12), justify="left")
    developer_label.pack(pady=10)
  
    # Copyright
    copyright_label = ctk.CTkLabel(about_win, text="© 2024 Digital Earth Science and Engineering Lab", font=normal_font)
    copyright_label.pack( pady=10)
    
    close_button = ctk.CTkButton(about_win, text="OK", command=about_win.destroy)
    close_button.pack(side="bottom", pady=(10,10))