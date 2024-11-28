import customtkinter as ctk
import tkinter as tk
from tkinter import IntVar
from customtkinter import CTkImage
#import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from PIL import Image
from tktooltip import ToolTip


class sample_class:
    def __init__(self, shared_container, pca_df_scaled, df, cleaned_df, box_frame, box_frame_sub, on_button_click, apply_button):
        # Initialize the sample class with necessary parameters
        self.apply_button = apply_button
        self.shared_container = shared_container
        self.on_button_click = on_button_click
        self.pca_df_scaled = pca_df_scaled
        self.df = df
        self.cleaned_df = cleaned_df
        self.box_frame = box_frame
        self.box_frame_sub = box_frame_sub
        self.var = IntVar()
        self.Graph_PCA()

    def Graph_PCA(self):
        # Create button for displaying PC bar graph by samples
        #script_dir = os.path.dirname(os.path.abspath(__file__))
        #image_path = os.path.join(script_dir, "images", "images_program", "sample-screen-svgrepo-com.png")
        image_path = 'images/icons/sample-screen-svgrepo-com.png'
        pil_image = Image.open(image_path)

        self.icon_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(32, 32))

        # Create and place image button
        self.image_button = ctk.CTkLabel(self.box_frame, image=self.icon_image, text="", width=20)
        self.image_button.grid(row=1, column=1, sticky="w", pady=0, padx=5)

        # Bind button click event to PCA graph function
        self.image_button.bind("<Button-1>", lambda event: self.on_button_click(self.image_button, self.Graph_PCA_sub))

        ToolTip(self.image_button, msg="PC Bar Graph by Samples")

    def Graph_PCA_sub(self):
        # Create UI for PCA graph options and actions
        for widget in self.box_frame_sub.winfo_children():
            widget.destroy()

        # Create and pack checkbox for sorting loadings
        self.checkbox = ctk.CTkCheckBox(self.box_frame_sub, text="Sort Loadings", variable=self.var)
        self.checkbox.pack(side="top", anchor="w", padx=5, pady=3)

        # Create and pack apply button
        self.apply_Graph_PCA = ctk.CTkButton(self.box_frame_sub, text="apply", command=self.update_plots)
        self.apply_Graph_PCA.pack(side="top", padx=5, pady=5)

        self.box_frame_sub.update_idletasks()
        
    def normalize(self, values, vmin=None, vmax=None):
        # Normalize values for color scaling
        vmin = vmin if vmin is not None else np.min(values)
        vmax = vmax if vmin is not None else np.max(values)
        norm_values = (values - vmin) / (vmax - vmin)
        return norm_values

    def plot_pca_barchart(self, data, entry_name, ax, sort):
        # Plot the PCA bar chart
        if sort:
            data = data.sort_values(ascending=False)
        norm_values = self.normalize(data, vmin=-max(abs(data)), vmax=max(abs(data)))
        bar_colors = plt.cm.coolwarm(norm_values)
        data.plot(kind='barh', color=bar_colors, ax=ax, fontsize="xx-small")
        ax.set_title(entry_name)
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.set_ylabel('')

    def update_plots(self):
        # Update plots with selected options
        sort = self.var.get() == 1 
        if not self.shared_container.current_tab:
            self.shared_container.create_tab() #("Sample BarGraph")

        # Close all existing plots and clear widgets
        plt.close('all')
        content_frame = self.shared_container.current_tab[1]
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Determine the number of samples and PCs
        num_samples = len(self.pca_df_scaled)
        num_pcs = len(self.pca_df_scaled.columns)
        
        # Create subplots for each PC
        fig, axes = plt.subplots(ncols=num_pcs, figsize=(9, 10))

        for i in range(num_pcs):
            pc_name = f'PC{i+1}'
            data = self.pca_df_scaled.iloc[:, i]
            if sort:
                sorted_indices = data.sort_values(ascending=False).index
                data = data.loc[sorted_indices]
                y_tick_labels = self.cleaned_df.loc[sorted_indices, 'sample id']
            else:
                y_tick_labels = self.cleaned_df['sample id']

            # Plot PCA bar chart for each PC
            self.plot_pca_barchart(data, pc_name, axes[i], sort)
            axes[i].set_yticks(range(num_samples))
            axes[i].set_yticklabels(y_tick_labels, fontsize="xx-small")
            axes[i].set_ylabel('')

        # Adjust layout and add colorbar
        fig.suptitle('PC Bar-Graphs by Sample IDs')

        plt.tight_layout(rect=[0, 0.05, 1, 1])

        # Add the plot to the tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()

        # Add navigation toolbar to the canvas
        toolbar = NavigationToolbar2Tk(canvas, content_frame)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, in_=content_frame)

