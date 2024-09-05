import tkinter as tk
import threading
import code
import sys

class MATerminal:
    def __init__(self, text_widget, main_app):

        # Use the passed text widget for terminal I/O
        self.terminal_text = text_widget
        self.main_app = main_app  # Reference to the main app

        # Enable copy functionality
        self.enable_copy()
        
        # Create a variable to store command history
        self.command_history = []
        self.history_index = -1

        # Create an interactive interpreter
        self.interpreter = code.InteractiveInterpreter(locals=self.get_scope())

        # Redirect stdout and stderr after interpreter is set
        sys.stdout = self
        sys.stderr = self

        # Insert initial prompt
        self.prompt()

        # Bind Enter and KeyPress events
        self.terminal_text.bind("<Return>", self.enter_command)
        self.terminal_text.bind("<KeyPress>", self.on_key_press)

    def enable_copy(self):
        self.terminal_text.bind("<Control-c>", self.copy_text)
        self.terminal_text.bind("<Command-c>", self.copy_text)
    
    def copy_text(self, event):
        try:
            # Get the selected text
            selected_text = self.terminal_text.selection_get()
            
            # Copy it to the clipboard
            self.terminal_text.clipboard_clear()
            self.terminal_text.clipboard_append(selected_text)
        except tk.TclError:
            pass

    def get_scope(self):
        # Combine globals, instance attributes, and main app attributes
        scope = globals().copy()
        scope.update(self.__dict__)
        scope.update(self.main_app.__dict__)  # Include main app's attributes
        scope['self'] = self
        scope['main_app'] = self.main_app  # Explicitly add main_app to scope
        return scope

    def update_scope(self):
        # Ensure interpreter has the latest local variables
        self.interpreter.locals.update(self.get_scope())

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name not in ('interpreter', 'terminal_text', 'command_history', 'history_index', 'main_app') and 'interpreter' in self.__dict__:
            self.interpreter.locals[name] = value

    def __getattr__(self, name):
        if 'interpreter' in self.__dict__ and name in self.interpreter.locals:
            return self.interpreter.locals[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def write(self, message):
        # Use after to ensure this runs on the main thread
        self.terminal_text.after(0, self.terminal_text.insert, tk.END, message)
        self.terminal_text.after(0, self.terminal_text.see, tk.END)
    
        # Ensure that the terminal widget scrolls to the end
        self.terminal_text.after(0, self.terminal_text.see, tk.END)

    def prompt(self):
        self.write(">> ")
        self.terminal_text.mark_set("insert", tk.END)
        self.terminal_text.see(tk.END)

    def enter_command(self, event):
        command = self.get_command()
        if command.strip():
            self.terminal_text.insert(tk.END, "\n")
            self.command_history.append(command)
            self.history_index = -1
            self.execute_command(command)
        return "break"

    def get_command(self):
        # Get the line where the command was entered
        line_start_index = self.terminal_text.index("insert linestart")
        line_end_index = self.terminal_text.index("insert lineend")
        command = self.terminal_text.get(line_start_index, line_end_index).strip()
    
        # Remove the prompt ('>> ') from the command
        if command.startswith(">> "):
            command = command[3:].strip()
    
        print(f"Command extracted: {command}")
        return command


    def execute_command(self, command):
        threading.Thread(target=self.run_command, args=(command,)).start()

        
    def run_command(self, command):
        try:
            self.update_scope()  # Ensure interpreter has the latest local variables
    
            # Compile the command into a code object
            code_obj = compile(command, '<input>', 'exec')
    
            try:
                # Execute the compiled code object
                exec(code_obj, self.interpreter.locals)
            except Exception as e:
                # Catch exceptions during the execution and print them
                error_message = traceback.format_exc()
                self.write(error_message)
    
            # If the command is an expression, evaluate and print its result
            if not command.startswith("print") and command.strip():  # Avoid printing prints and empty commands
                try:
                    # Evaluate the expression and print it
                    result = eval(command, self.interpreter.locals)
                    if result is not None:
                        self.write(f"{result}\n")
                except Exception as e:
                    pass
                    
        except Exception as e:
            # Catch any compilation exceptions and print them
            self.write(f"Error: {str(e)}\n")
        
        # Always show the prompt after execution or printing
        self.prompt()

    def on_key_press(self, event):
        # Disallow editing previous text
        if self.terminal_text.compare("insert", "<", self.terminal_text.index(tk.END + "-1c linestart")):
            return "break"
        
        # Handle command history navigation
        if event.keysym == "Up":
            if self.command_history:
                self.history_index = max(0, self.history_index - 1)
                self.replace_command(self.command_history[self.history_index])
            return "break"
        elif event.keysym == "Down":
            if self.command_history:
                self.history_index = min(len(self.command_history) - 1, self.history_index + 1)
                self.replace_command(self.command_history[self.history_index])
            return "break"

    def replace_command(self, command):
        line_start_index = self.terminal_text.index("insert linestart")
        line_end_index = self.terminal_text.index("insert lineend")
        self.terminal_text.delete(line_start_index, line_end_index)
        self.terminal_text.insert(line_start_index, f" {command}")
