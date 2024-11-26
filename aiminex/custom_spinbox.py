
import customtkinter as ctk
import tkinter as tk

from typing import Union, Callable


class CTkSpinbox(ctk.CTkFrame):
         
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1.0,
                 min_value: int = 0.0,
                 max_value: int = 1000.0,
                 button_color: str = None,
                 button_hover_color: str = None,
                 entry_color: str = None,
                 text_color: str = None,
                 border_color: str = None,
                 entry_border: str = 2,
                 command: Callable = None,
                 **kwargs):
        
        super().__init__(*args, width=width, height=height, **kwargs)
        

        self.step_size = step_size
        self.max_value = max_value
        self.min_value = min_value
        self.command = command
        self.validation = self.register(self.only_numbers)
        
        self.grid_columnconfigure((0, 2), weight=0) 
        self.grid_columnconfigure(1, weight=1)
        
        self.button_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"] if button_color is None else button_color
        self.button_hover = ctk.ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else button_hover_color
        self.entry_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"] if entry_color is None else entry_color
        self.border_color = ctk.ThemeManager.theme["CTkEntry"]["border_color"] if border_color is None else border_color
        self.text_color = ctk.ThemeManager.theme["CTkEntry"]["text_color"] if text_color is None else text_color
        super().configure(border_color=self.border_color)
        
        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6, border_color=self.border_color, text_color=self.text_color,
                                                       command=self.subtract_button_callback, fg_color=self.button_color, hover_color=self.button_hover)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
    
        self.text = tk.DoubleVar()
        self.text.set(self.min_value)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, textvariable=self.text, fg_color=self.entry_color, border_width=entry_border,
                                            placeholder_text=str(self.min_value), justify="right", validate='key', border_color=self.border_color,
                                            validatecommand=(self.validation, '%P'), text_color=self.text_color)       
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6, border_color=self.border_color, text_color=self.text_color,
                                                  command=self.add_button_callback, fg_color=self.button_color, hover_color=self.button_hover)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.entry.bind("<MouseWheel>", self.on_mouse_wheel)
        
    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.add_button_callback()
        else:
            self.subtract_button_callback()
            
    def add_button_callback(self):
        if self.entry.get() == "":
            self.text.set(0.0)
        try:
            current_value = float(self.entry.get())
            if current_value < self.max_value:
                self.text.set(round(current_value + self.step_size, 2))
        except ValueError:
            return
        if self.command is not None:
            self.command()
            
    def configure(self, state="enabled", **kwargs):
        if state == "disabled":
            self.entry.configure(state="disabled")
            self.add_button.configure(state="disabled", **kwargs)
            self.subtract_button.configure(state="disabled", **kwargs)
            self.entry.unbind("<MouseWheel>")
        else:
            self.entry.configure(state="normal")
            self.add_button.configure(state="normal", **kwargs)
            self.subtract_button.configure(state="normal", **kwargs)
            self.entry.bind("<MouseWheel>", self.on_mouse_wheel)
            
    def subtract_button_callback(self):
        if self.entry.get() == "":
            self.text.set(0.0)
        try:
            current_value = float(self.entry.get())
            if self.min_value < current_value <= self.max_value:
                self.text.set(round(current_value - self.step_size, 2))
        except ValueError:
            return
        if self.command is not None:
            self.command()
        
    def only_numbers(self, char):
        if char == "" or (char.replace('.', '', 1).isdigit() and char.count('.') < 2):
            try:
                float(char)  # Ensure it's a valid float
                return True
            except ValueError:
                return False
        else:
            return False
        
    def get(self) -> Union[float, None]:
        if self.entry.get() == "":
            return 0.0
        try:
            return round(float(self.text.get()), 2)
        except ValueError:
            return None

    def set(self, value: float):
        try:
            float(value)
            self.text.set(round(float(value), 2))
        except ValueError:
            pass
