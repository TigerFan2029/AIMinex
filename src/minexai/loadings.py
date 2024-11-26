
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from customtkinter import CTkImage
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tktooltip import ToolTip
from PIL import Image

class loading_class:
    def __init__(self, loadings, shared_container, box_frame, box_frame_sub, on_button_click, apply_button):
        # Initialize the loading class with necessary parameters
        self.apply_button = apply_button
        self.shared_container = shared_container
        self.on_button_click = on_button_click
        self.loadings = loadings

        self.box_frame = box_frame
        self.box_frame_sub = box_frame_sub
        self.var = IntVar()
        self.group_list = []

        self.Graph_PC()

    def Graph_PC(self):
        # Create button for displaying PC bar graph
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "images", "images_program", "element-svgrepo-com.png")
        pil_image = Image.open(image_path)

        self.icon_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(32, 32))

        # Create and place image button
        self.image_button = ctk.CTkLabel(self.box_frame, image=self.icon_image, text="", width=20)
        self.image_button.grid(row=1, column=0, sticky="w", pady=0, padx=5)

        # Bind button click event to PC graph function
        self.image_button.bind("<Button-1>", lambda event: self.on_button_click(self.image_button, self.Graph_PC_sub))

        # Add tooltip to the button
        ToolTip(self.image_button, msg="PC Bar Graph by Elements")

    def Graph_PC_sub(self):
        # Create elements and groups selection UI
        for widget in self.box_frame_sub.winfo_children():
            widget.destroy()

        # Create and pack checkbox for sorting loadings
        self.checkbox = ctk.CTkCheckBox(self.box_frame_sub, text="Sort Loadings", variable=self.var)
        self.checkbox.pack(side="top", anchor="w", padx=5, pady=3)

        # Create and pack listbox for element selection
        self.elements_listbox = tk.Listbox(self.box_frame_sub, selectmode=tk.MULTIPLE)
        for element in self.loadings.index:
            self.elements_listbox.insert(tk.END, element)
        self.elements_listbox.pack(side="top", padx=5, pady=5)

        # Function to deselect all elements
        def deselect_all():
            self.elements_listbox.selection_clear(0, tk.END)

        # Bind deselect function to the listbox
        self.elements_listbox.bind('<Command-d>', lambda event: deselect_all())
        self.elements_listbox.bind('<Control-d>', lambda event: deselect_all())

        # Create and pack button to add selected elements as a group
        self.add_group_button = ctk.CTkButton(self.box_frame_sub, text="Add Group", command=self.add_group)
        self.add_group_button.pack(side="top", padx=5, pady=5)

        # Create and pack listbox to display added groups
        self.group_listbox = tk.Listbox(self.box_frame_sub, selectmode=tk.MULTIPLE)
        self.group_listbox.pack(side="top", padx=5, pady=5)

        # Create and pack apply button
        self.apply_Graph_PC = ctk.CTkButton(self.box_frame_sub, text="Apply", command=self.update_plots)
        self.apply_Graph_PC.pack(side="top", padx=5, pady=5)

        # Create and pack button to clear all groups
        self.clear_groups_button = ctk.CTkButton(self.box_frame_sub, text="Clear Groups", command=self.clear_groups)
        self.clear_groups_button.pack(side="top", padx=5, pady=5)

        self.box_frame_sub.update_idletasks()
        
    def clear_groups(self):
        # Clear all groups
        self.group_list.clear()
        self.group_listbox.delete(0, tk.END)

    def add_group(self):
        # Add selected elements as a group
        selected_elements = [self.elements_listbox.get(i) for i in self.elements_listbox.curselection()]
        self.group_list.append(selected_elements)
        self.group_listbox.insert(tk.END, f"Group {len(self.group_list)}: {', '.join(selected_elements)}")

    def normalize(self, values, vmin=None, vmax=None):
        # Normalize values for color scaling
        vmin = vmin if vmin is not None else np.min(values)
        vmax = vmax if vmax is not None else np.max(values)
        norm_values = (values - vmin) / (vmax - vmin)
        return norm_values

    def plot_pc_barchart(self, data, pc_name, ax, sort, group_indices):
        # Plot the PC bar chart
        if sort:
            data = data.sort_values(ascending=False)
        norm_values = self.normalize(data, vmin=-max(abs(data)), vmax=max(abs(data)))
        bar_colors = plt.cm.coolwarm(norm_values)
        data.plot(kind='barh', color=bar_colors, ax=ax, fontsize="x-small")
        ax.set_title(pc_name)
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.set_ylabel(' ')

        # Draw horizontal lines to separate groups
        for idx in group_indices:
            ax.axhline(y=idx - 0.5, color='black', linewidth=1)

        # Update y-axis labels
        labels = ax.get_yticklabels()
        new_labels = [label.get_text().replace('_ppm', '')
                                      .replace('_pct', '')
                                      .replace('_Howell', '') for label in labels]
        ax.set_yticklabels(new_labels)

    def update_plots(self):
        # Update plots with selected groups and options
        sort = self.var.get() == 1
        if not self.shared_container.current_tab:
            self.shared_container.create_tab() #("Element BarGraph")

        # Close all existing plots and clear widgets
        plt.close('all')
        content_frame = self.shared_container.current_tab[1]
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Create a new figure and axes for the plots
        fig, axes = plt.subplots(ncols=len(self.loadings.columns), figsize=(15, 8))
        if len(self.loadings.columns) == 1:
            axes = [axes]

        # Iterate over each principal component
        for i in range(len(self.loadings.columns)):
            combined_data = pd.Series(dtype='float64')
            group_indices = []
            current_index = 0
            selected_indices = self.group_listbox.curselection()
            
            # Combine data for selected groups
            for index in selected_indices:
                group = self.group_list[index]
                group_data = self.loadings.loc[group, f'PC{i+1}']
                if sort:
                    group_data = group_data.sort_values(ascending=False)
                combined_data = pd.concat([combined_data, group_data])
                current_index += len(group_data)
                group_indices.append(current_index)

            # Plot the combined data
            if not combined_data.empty:
                self.plot_pc_barchart(combined_data, f'PC{i+1}', axes[i], sort=False, group_indices=group_indices)

        # Adjust layout and add colorbar
        fig.suptitle('PC Bar-Graph by Elements')

        #fig.subplots_adjust(bottom=0.25, top=0.90, hspace=0.3)
        plt.tight_layout(rect=[0, 0.05, 1, 1])

        # norm = plt.Normalize(vmin=self.loadings.min().min(), vmax=self.loadings.max().max())
        # cmap = plt.cm.coolwarm

        # cbar = fig.colorbar(
        #     plt.cm.ScalarMappable(norm=norm, cmap=cmap),
        #     ax=axes,
        #     orientation='horizontal',
        #     fraction=0.03,
        #     pad=0.03
        # )

        #fig.text(0.5, 0.05, "qwetaghbvdhak", ha='center', va='center', fontsize=10)

        # Add the plot to the tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()

        # Add navigation toolbar to the canvas
        toolbar = NavigationToolbar2Tk(canvas, content_frame)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, in_=content_frame)
