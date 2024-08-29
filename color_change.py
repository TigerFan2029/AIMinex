import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd


def open_color_window(self):
    global dc, ds, color_map, color_map1

    # Open a new window for manual color editing
    color_window = tk.Toplevel(self)
    color_window.title("Edit Colors")

    # Lithologies Section
    lithology_label = ctk.CTkLabel(color_window, text="Lithology")
    lithology_label.grid(row=0, column=0, padx=10, pady=10)

    color_label = ctk.CTkLabel(color_window, text="Color")
    color_label.grid(row=0, column=1, padx=10, pady=10)

    visual_label = ctk.CTkLabel(color_window, text="Selected Color")
    visual_label.grid(row=0, column=2, padx=10, pady=10)

    # Generate the list of comboboxes for lithology color selection
    for idx, lithology in enumerate(self.lithologies):
        # Label for lithology
        litho_label = ctk.CTkLabel(color_window, text=lithology)
        litho_label.grid(row=idx + 1, column=0, padx=10, pady=5)

        # Small rectangle to visualize the selected color
        color_visual = ttk.Label(color_window, text="   ", background=color_map.get(lithology, "black"))
        color_visual.grid(row=idx + 1, column=2, padx=10, pady=5)

        # Combobox for selecting color
        color_combo = ctk.CTkComboBox(
            color_window, 
            values=["lime", "blue", "cyan", "deeppink", "pink", "black", "grey", "sienna", "dimgrey", "lightgrey"], 
            state="readonly", 
            command=lambda selected_value, lithology=lithology, color_visual=color_visual: update_color_visual(selected_value, lithology, color_visual)
        )
        color_combo.set(color_map.get(lithology, "black"))
        color_combo.grid(row=idx + 1, column=1, padx=10, pady=5)
            
    # Rock Units Section
    rock_label = ctk.CTkLabel(color_window, text="Rock Unit")
    rock_label.grid(row=0, column=4, padx=10, pady=10)
    
    shape_label = ctk.CTkLabel(color_window, text="Shape")
    shape_label.grid(row=0, column=5, padx=10, pady=10)
    
    shape_visual_label = ctk.CTkLabel(color_window, text="Selected Shape")
    shape_visual_label.grid(row=0, column=6, padx=10, pady=10)
    
    # Define a mapping between user-friendly names and symbols
    shape_name_to_symbol = {
        "triangle": "^",
        "star": "*",
        "circle": "o",
        "square": "s",
        "diamond": "D"
    }
    
    # Define the reverse mapping (symbols to names) for setting the default value
    symbol_to_shape_name = {v: k for k, v in shape_name_to_symbol.items()}
    
    # Rock Units Section
    for idx, rock_unit in enumerate(ds['Shape'].unique()):
        # Label for rock unit
        rock_label = ctk.CTkLabel(color_window, text=rock_unit)
        rock_label.grid(row=idx + 1, column=4, padx=10, pady=5)
    
        # Get the default shape symbol
        default_shape_symbol = color_map1.get(rock_unit, ds.loc[ds['Shape'] == rock_unit, 'Shapes'].values[0])
        
        # Convert the symbol to a user-friendly name for display in the combobox
        default_shape_name = symbol_to_shape_name.get(default_shape_symbol, "triangle")  # Default to "triangle" if not found
                
        # Text to visualize the selected shape symbol
        rock_shape_visual = ttk.Label(color_window, text=default_shape_symbol)
        rock_shape_visual.grid(row=idx + 1, column=6, padx=10, pady=5)
    
        # Combobox for selecting shape (display names instead of symbols)
        rock_shape_combo = ctk.CTkComboBox(
            color_window, 
            values=list(shape_name_to_symbol.keys()),
            state="readonly", 
            command=lambda selected_value, rock_unit=rock_unit, rock_shape_visual=rock_shape_visual: update_rock_shape_visual(selected_value, rock_unit, rock_shape_visual, shape_name_to_symbol)
        )
        rock_shape_combo.set(default_shape_name)
        rock_shape_combo.grid(row=idx + 1, column=5, padx=10, pady=5)


    # Apply Button to save the changes
    apply_button = ctk.CTkButton(color_window, text="Apply Colors", command=lambda: apply_color_change(self))
    apply_button.grid(row=max(len(self.lithologies), len(ds['Shape'].unique())) + 2, column=0, columnspan=7, stick = "ew", padx=10, pady=(10,0))

    label = ctk.CTkLabel(color_window, text="Redraw graphs to apply change")
    label.grid(row=max(len(self.lithologies), len(ds['Shape'].unique())) + 3, column=0, columnspan=7, stick = "ew", padx=10, pady=(0,10))
    
def update_color_visual(selected_value, lithology, color_visual):
    # Declare dc as global to access the global dataframe
    global dc, color_map
    
    # Update the rectangle color preview with the selected color
    color_visual.configure(background=selected_value)
    
    # Update the color map and global dc dataframe immediately
    color_map[lithology] = selected_value
    dc.loc[dc['Lithology'] == lithology, 'Color'] = selected_value

def update_rock_shape_visual(selected_shape_name, rock_unit, rock_shape_visual, shape_name_to_symbol):
    global ds, color_map1
    # Convert the selected name back to the corresponding symbol
    selected_symbol = shape_name_to_symbol.get(selected_shape_name)
    
    # Update the shape visualization (display the selected symbol)
    rock_shape_visual.configure(text=selected_symbol)
    
    # Update the shape map and global ds dataframe with the symbol, not the name
    color_map1[rock_unit] = selected_symbol
    ds.loc[ds['Shape'] == rock_unit, 'Shapes'] = selected_symbol

def apply_color_change(self):
    global dc, ds, color_map, color_map1
    
    # Get selected lithology or rock unit from the listbox and the chosen color
    selected_lithology = self.lithology_listbox_color.get(tk.ACTIVE)
    selected_color = self.color_combo.get()
    dc.reset_index(drop=True, inplace=True)
    ds.reset_index(drop=True, inplace=True)
    
    if selected_lithology and selected_color:
        # Update the color map for lithologies (color_map) and global `dc`
        if selected_lithology in self.lithologies:
            dc.loc[dc['Lithology'] == selected_lithology, 'Color'] = selected_color
            color_map[selected_lithology] = selected_color
        
        # Update the color map for rock units (color_map1) and global `ds`
        if selected_lithology in ds['Shape'].values:
            ds.loc[ds['Shape'] == selected_lithology, 'Shapes'] = selected_color
            color_map1[selected_lithology] = selected_color

        # Update visuals globally to reflect the changes
        self.update_visuals_globally()

def color_function(self):
    global dc, color_map
    # Generate color mapping for lithologies
    try:
        dc = self.cleaned_df['lithology']
        dc = dc.to_frame()
        dc = dc.rename(columns={dc.columns[0]: 'Lithology'})
        
        # color_list = dc['Lithology'].unique()
        # default_colors = ["lime", "blue", "cyan", "deeppink", "pink", "black", "black", "black", "grey", "lightgrey"]
        # color_map = {}
        # # Populate the dictionary with symbols for each shape
        # for i, color in enumerate(color_list):
        #     if i < len(default_colors):
        #         color_map[color] = default_colors[i]
        color_map = {
            'Calcitic Marble': 'lime',
            'Dolomitic Marble': 'blue',
            'Di-Tr Dolomitic Marble': 'cyan',
            'Apatite Marble': 'deeppink',
            'Siliceous Calcitic Marble': 'steelblue',
            #'Carbonatite': 'deeppink',
            #'Carbonatite-Like': 'pink',
        
            'Syenite': 'black',
            'Altered Syenite': 'black',
            'Intrusion': 'black',
            'Skarn': 'sienna',
            'Syenite-Like': 'black',
            'Impure Siliciclastic': 'dimgrey',
            'Pure Siliciclastic': 'lightgrey',
            'Siliciclastic': 'grey'
            
        }
        dc['Color'] = dc['Lithology'].map(color_map)
        dc.reset_index(drop=True, inplace=True)

    except Exception as e:
        color_map = {}
        dc = pd.DataFrame()
        self.output_text.insert("end", f"Error generating lithology-color map: {e}\n")     
    
def shape_map(self):
    global ds, color_map1
    # Generate shape mapping for rock units
    try:
        self.cleaned_df['rock unit'] = self.cleaned_df['rock unit'].apply(lambda x: x.strip().lower().title() if isinstance(x, str) and pd.notnull(x) else x)
        
        ds = self.cleaned_df['rock unit']
        ds = ds.str.strip().to_frame()
        ds = ds.rename(columns={ds.columns[0]: 'Shape'})
        
        #shape_list = ds['Shape'].unique()
        # default_symbols = ["^", "*", "o", "s", "D"]
        # color_map1 = {}
        # # Populate the dictionary with symbols for each shape
        # for i, shape in enumerate(shape_list):
        #     if i < len(default_symbols):
        #         color_map1[shape] = default_symbols[i]
        
        color_map1 = {
            'Marble Units': "^",
            'Altered Intrusion': "*",
            'Siliciclastic': "o",
            'Intrusion': "s",
            'Anomalous Rock': "D",
        }

        ds["Shapes"] = ds["Shape"].map(color_map1)
        ds.reset_index(drop=True, inplace=True)

    except Exception as e:
        color_map1 = {}
        ds = pd.DataFrame()
        self.output_text.insert("end", f"Error generating rock unit-shape map: {e}\n") 
        self.output_text.insert("end", f"Column Rock Unit does not exist, or check error in name?\n") 
