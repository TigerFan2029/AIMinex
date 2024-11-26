import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class CustomToolbar(NavigationToolbar2Tk):
    #Toolbar with only the save button
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)

        for widget in self.winfo_children():
            try:
                if isinstance(widget, ttk.Separator):
                    widget.pack_forget()
                elif str(widget['text']) != 'Save':
                    widget.pack_forget()
            except (tk.TclError, KeyError):
                pass
