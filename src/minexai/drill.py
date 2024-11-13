import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, IntVar
from tkinter import *
from customtkinter import CTkImage

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from PIL import Image
from tktooltip import ToolTip
import re


class drill_class:
    def __init__(self, shared_container, pca_df_scaled, cleaned_df, df, box_frame, box_frame_sub, on_button_click, apply_button):
        self.shared_container = shared_container
        self.apply_button = apply_button
        self.on_button_click = on_button_click
        self.pca_df_scaled = pca_df_scaled
        self.cleaned_df = cleaned_df
        self.df = df
        self.box_frame = box_frame
        self.box_frame_sub = box_frame_sub
        self.var = IntVar()

        # Initialize the drill hole graph
        self.Graph_PCA()

    def Graph_PCA(self):
        # Load and resize the image for the button icon
        pil_image = Image.open("src/minexai/images/images_program/drill-svgrepo-com.png")
        self.icon_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(32, 32))

        # Create a label with the icon and bind a click event to it
        self.image_button = ctk.CTkLabel(self.box_frame, image=self.icon_image, text="", width=20)
        self.image_button.grid(row=1, column=4, sticky="w", pady=0, padx=5)
        self.image_button.bind("<Button-1>", lambda event: self.on_button_click(self.image_button, self.Graph_PCA_sub))

        # Add a tooltip to the label
        ToolTip(self.image_button, msg="Drill Hole Chart")

    def Graph_PCA_sub(self):
        # Clean and process sample IDs
        self.cleaned_df['Drill_Hole'] = self.cleaned_df['drillhole']
        
        # Extract depth unit from column name
        column_name = self.cleaned_df.filter(like='depth').columns[0]
        match = re.search(r'\((.*?)\)', column_name)
        self.unit = match.group(1) if match else None
        
        self.cleaned_df['Depth'] = self.cleaned_df[column_name]
        self.drill_holes = sorted(self.cleaned_df['Drill_Hole'].unique().tolist())

        # Clear previous widgets
        for widget in self.box_frame_sub.winfo_children():
            widget.destroy()

        # Create a dropdown for selecting drill hole
        ctk.CTkLabel(self.box_frame_sub, text="Select Drill Hole:").pack(side="top", padx=5, pady=(5, 0))
        self.drill_hole_combo = ttk.Combobox(self.box_frame_sub, values=self.drill_holes, state="readonly")
        self.drill_hole_combo.current(0)
        self.drill_hole_combo.pack(side="top", padx=5, pady=(5, 0))

        # Add an apply button
        self.apply_Graph_PCA = ctk.CTkButton(self.box_frame_sub, text="apply", command=self.update_plots)
        self.apply_Graph_PCA.pack(side="top", padx=5, pady=10)

        self.box_frame_sub.update_idletasks()

    def normalize(self, values, vmin=None, vmax=None):
        # Normalize values to range [0, 1]
        vmin = vmin if vmin is not None else np.min(values)
        vmax = vmax if vmin is not None else np.max(values)
        norm_values = (values - vmin) / (vmax - vmin)
        return norm_values

    def plot_pca_scatter(self, data, y_positions, ax):
        # Normalize data and create scatter plot with color mapping
        norm_values = self.normalize(data, vmin=-max(abs(data)), vmax=max(abs(data)))
        scatter_colors = plt.cm.coolwarm(norm_values)
        ax.scatter(data, y_positions, color=scatter_colors, s=30)
        ax.set_yticks(y_positions)
        ax.set_yticklabels([])
        ax.invert_yaxis()
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.axvline(x=0, color='black', linewidth=0.5)
        max_val = max(abs(data.min()), data.max())
        ax.set_xlim(-max_val, max_val)
        ax.tick_params(rotation=-35, labelsize="medium")

        # Customize plot spines
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(1)

    def plot_depth_chart(self, depths, y_positions, ax):
        # Plot depth chart with horizontal lines representing depths
        ax.hlines(y=y_positions, xmin=0, xmax=0.2, linestyles='-', linewidth=0.8)
        ax.set_yticks(y_positions)
        ax.set_yticklabels(depths)
        ax.invert_yaxis()
        ax.set_xticklabels([])
        ax.set_title(f'Depth ({self.unit})')
        ax.axis('on')
        ax.set_ylabel(self.drill_hole)
        ax.tick_params(labelsize="small")

    def update_plots(self):
        # Create a new tab if not already present
        if not self.shared_container.current_tab:
            self.shared_container.create_tab() #("Drill Hole")

        content_frame = self.shared_container.current_tab[1]
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        # Filter and sort data for the selected drill hole
        self.drill_hole = self.drill_hole_combo.get()
        filtered_cleaned_df = self.cleaned_df[self.cleaned_df['Drill_Hole'] == self.drill_hole]
        if filtered_cleaned_df.empty:
            self.output_text.insert("end", "No samples found for the selected drill hole.")
            return

        filtered_cleaned_df = filtered_cleaned_df.sort_values(by='Depth')
        sample_indices = filtered_cleaned_df.index
        depths = filtered_cleaned_df['Depth'].tolist()
        if len(sample_indices) == 0:
            self.output_text.insert("end", "No samples found for the selected drill hole.")
            return

        # Calculate y positions for depth markers
        print(depths)
        max_depth = max(depths)
        min_depth = min(depths)
        if max_depth == min_depth:
            y_positions = [0.5 for _ in depths]
        else:
            y_positions = [((depth - min_depth) / (max_depth - min_depth)) * len(depths) for depth in depths]

        plt.close('all')

        # Create subplots for depth chart and PCA scatter plots
        fig, axes = plt.subplots(nrows=1, ncols=len(self.pca_df_scaled.columns) + 1, figsize=(15, 10))
        pos1 = axes[0].get_position()
        axes[0].set_position([pos1.x0, pos1.y0, pos1.width * 0.5, pos1.height])
        self.plot_depth_chart(depths, y_positions, axes[0])

        # Plot PCA scatter plots for each principal component
        for col, pc in enumerate(self.pca_df_scaled.columns):
            data = self.pca_df_scaled.loc[sample_indices, pc]
            ax = axes[col + 1]
            self.plot_pca_scatter(data, y_positions, ax)
            ax.set_title(f'PC{col + 1}')

        # Embed the plot in the Tkinter GUI
        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, content_frame)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, in_=content_frame)