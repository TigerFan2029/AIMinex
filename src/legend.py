import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import color_change
from custom_toolbar import CustomToolbar
from matplotlib.lines import Line2D

def legend(self):
    # Create and display legends for lithology and rock type
    Legend = self.var1.get() == 1
    if Legend:
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        if not color_change.dc.empty and not color_change.ds.empty:
            unique_lithologies = self.cleaned_df[self.selected_column.strip().lower()].unique()
            
            from color_change import column_to_use
            unique_shapes = self.cleaned_df[column_to_use.strip().lower()].unique()
    
            # For lithologies
            handle1 = []
            label1 = []
            print (f"color_map{color_change.color_map}")
            for lithology in unique_lithologies:
                color = color_change.color_map[lithology.title()]
                l1 = Line2D([], [], color=color, marker='o', linestyle='None', label=lithology)
                handle1.append(l1)
                label1.append(lithology)
    
            # For shapes
            handle2 = []
            label2 = []
            print (f"color_map1{color_change.color_map1}")
            for shape in unique_shapes:
                str(shape).strip().lower()
                marker = color_change.color_map1[shape]
                l2 = Line2D([], [], color='black', marker=marker, linestyle='None', label=shape)
                handle2.append(l2)
                label2.append(shape)
    
            total_entries = len(label1) + len(label2)
            height_per_entry = 0.225
            fig_height = total_entries * height_per_entry
            
            hei = fig_height-(len(label1)*0.3)-0.05
            print(hei)
            print(f"fig_height{fig_height}")
    
            figx = plt.figure(figsize=(2.5, fig_height))
            axx = figx.add_subplot(111)
            axx.axis('off')
    
            self.legend1 = plt.legend(handle1, label1, bbox_to_anchor=(0, 1.2), loc='upper left', title=self.selected_column, fontsize=10, labelspacing=0.3, bbox_transform=axx.transAxes)
            self.legend2 = plt.legend(handle2, label2, bbox_to_anchor=(0, hei), loc='upper left', title=column_to_use, fontsize=10, labelspacing=0.3, bbox_transform=axx.transAxes)
            axx.add_artist(self.legend1)
            axx.add_artist(self.legend2)
            self.canvas1 = FigureCanvasTkAgg(figx, master=self.legend_frame)
            toolbar = CustomToolbar(self.canvas1, self.legend_frame)
            toolbar.update()
            toolbar.pack(side=tk.TOP, fill=tk.X)
    
            self.canvas1.get_tk_widget().pack(fill="both", expand=True)
    
            self.legend1.set_visible(self.var1.get() == 1)
            self.legend2.set_visible(self.var1.get() == 1)
        else:
            pass
    else:
        pass


