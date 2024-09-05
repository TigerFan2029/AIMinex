import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from customtkinter import CTkImage
import pandas as pd
from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from PIL import Image
from tktooltip import ToolTip


class supervised_learning():
    def __init__(self, df, cleaned_df, on_button_click, apply_button, box_frame):
        self.df = df  # The dataframe without 'lithology'
        self.cleaned_df = cleaned_df  # DataFrame with 'lithology' column
        self.on_button_click = on_button_click
        self.apply_button = apply_button
        self.box_frame = box_frame
        self.rows = []  
        self.prediction_df = None  # For the imported Excel prediction data

        self.y_column = None

        self.graph_icon() 

    def graph_icon(self):
        # Create button for displaying PC bar graph
        pil_image = Image.open("mineralAI_images/images_program/ml.png")

        self.icon_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(32, 32))

        # Create and place image button
        self.image_button = ctk.CTkLabel(self.box_frame, image=self.icon_image, text="", width=20)
        self.image_button.grid(row=5, column=0, sticky="w", pady=0, padx=5)

        # Bind button click event to PC graph function
        self.image_button.bind("<Button-1>", lambda event: self.on_button_click(self.image_button, self.create_window))

        # Add tooltip to the button
        ToolTip(self.image_button, msg="Supervised Learning-Prediction with data")


    def create_window(self):
        # Create a new window for dynamic rows and predictions
        self.window = ctk.CTkToplevel()
        self.window.title("Dynamic Rows Example")
        self.window.geometry("800x600")
        
        # Use CTkScrollableFrame instead of canvas and scrollbar
        self.scrollable_frame = ctk.CTkScrollableFrame(self.window, width=780, height=580)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize UI elements in the new window
        self.initialize_ui()

    def initialize_ui(self):
        # Import Excel button for quick predictions
        self.import_button = ctk.CTkButton(self.scrollable_frame, text="Import Excel for Prediction", command=self.import_excel)
        self.import_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # ComboBox for selecting the model
        self.combo1 = ctk.CTkComboBox(self.scrollable_frame, values=["SVM", "Random Forest"], command=self.update_model_parameters)
        self.combo1.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.combo1.set("Select Model")
        
        # Call the method to create ComboBox for selecting y column
        self.create_y_column_combobox()

        # Plus button for adding rows manually
        self.plus_button = ctk.CTkButton(self.scrollable_frame, text="+", command=self.add_manual_row)
        self.plus_button.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")

        # Predict button (initially hidden, will be repositioned after rows are added)
        self.predict_button = ctk.CTkButton(self.scrollable_frame, text="Predict", command=self.predict_model)
        self.predict_button.grid(row=7, column=0, columnspan=3, pady=10, sticky="ew")


    def create_y_column_combobox(self):
        filtered_columns = [col for col in self.cleaned_df.columns if '_ppm' not in col and '_pct' not in col]

        ctk.CTkLabel(self.scrollable_frame, text="Select y-data").grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        # Create ComboBox to select which column to use for prediction (y data)
        self.y_column_combo = ctk.CTkComboBox(self.scrollable_frame, values=filtered_columns, command = self.set_y_column)
        self.y_column_combo.set("Select Y Column")
        self.y_column_combo.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

    def set_y_column(self, event):
        # Store the selected y column
        self.y_column = self.y_column_combo.get()
        

    def update_model_parameters(self, selected_model):
        # Place the parameter widgets above the manual rows
        param_row_start = 1  # Starting row for parameter widgets

        try:
            self.kernel_combo.grid_forget()
            self.c_spinbox.grid_forget()
            self.coef0_spinbox.grid_forget()
            self.degree_spinbox.grid_forget()
            self.kernel_text.grid_forget()
            self.c_text.grid_forget()
            self.coef0_text.grid_forget()
            self.degree_text.grid_forget()
        except:
            pass

        try:
            self.n_estimators_spinbox.grid_forget()
            self.max_depth_spinbox.grid_forget()
            self.min_samples_split_spinbox.grid_forget()
            self.n_estimators_text.grid_forget()
            self.max_depth_text.grid_forget()
            self.min_samples_split_text.grid_forget()
        except:
            pass

    
        
        if selected_model == "SVM":
            # Add SVM parameter widgets starting at row 2
            self.kernel_text = ctk.CTkLabel(self.scrollable_frame, text = "Select Kernel").grid(row=param_row_start, column=1, padx=10, pady=5, sticky="ew")
            self.kernel_combo = ctk.CTkComboBox(self.scrollable_frame, values=["linear", "poly", "rbf", "sigmoid"])
            self.kernel_combo.grid(row=param_row_start, column=2, padx=10, pady=5, sticky="ew")
            self.kernel_combo.set("linear")
            
            self.c_text = ctk.CTkLabel(self.scrollable_frame, text = "Select C").grid(row=param_row_start+1, column=1, padx=10, pady=5, sticky="ew")
            self.c_spinbox = ttk.Spinbox(self.scrollable_frame, from_=0.1, to=1000, increment=0.1)
            self.c_spinbox.grid(row=param_row_start+1, column=2, padx=10, pady=5, sticky="ew")
            self.c_spinbox.set("1.0")

            self.coef0_text = ctk.CTkLabel(self.scrollable_frame, text = "Select Coef0").grid(row=param_row_start+2, column=1, padx=10, pady=5, sticky="ew")
            self.coef0_spinbox = ttk.Spinbox(self.scrollable_frame, from_=0.0, to=100, increment=0.1)
            self.coef0_spinbox.grid(row=param_row_start+2, column=2, padx=10, pady=5, sticky="ew")
            self.coef0_spinbox.set("0.0")
            
            self.degree_text = ctk.CTkLabel(self.scrollable_frame, text = "Select Degree").grid(row=param_row_start+3, column=1, padx=10, pady=5, sticky="ew")
            self.degree_spinbox = ttk.Spinbox(self.scrollable_frame, from_=1.0, to=10)
            self.degree_spinbox.grid(row=param_row_start + 3, column=2, padx=10, pady=5, sticky="ew")
            self.degree_spinbox.set("3")

        elif selected_model == "Random Forest":
            # Add Random Forest parameter widgets starting at row 2
            self.n_estimators_text = ctk.CTkLabel(self.scrollable_frame, text = "Select n_estimators").grid(row=param_row_start, column=1, padx=10, pady=5, sticky="ew")
            self.n_estimators_spinbox = ttk.Spinbox(self.scrollable_frame, from_=10.0, to=1000)
            self.n_estimators_spinbox.grid(row=param_row_start, column=2, padx=10, pady=5, sticky="ew")
            self.n_estimators_spinbox.set("100")

            self.max_depth_text = ctk.CTkLabel(self.scrollable_frame, text = "Select max_depth").grid(row=param_row_start+1, column=1, padx=10, pady=5, sticky="ew")
            self.max_depth_spinbox = ttk.Spinbox(self.scrollable_frame, from_=1.0, to=100)
            self.max_depth_spinbox.grid(row=param_row_start+1, column=2, padx=10, pady=5, sticky="ew")
            self.max_depth_spinbox.set("None")

            self.min_samples_split_text = ctk.CTkLabel(self.scrollable_frame, text = "Select min_samples_split").grid(row=param_row_start+2, column=1, padx=10, pady=5, sticky="ew")
            self.min_samples_split_spinbox = ttk.Spinbox(self.scrollable_frame, from_=2.0, to=10)
            self.min_samples_split_spinbox.grid(row=param_row_start+2, column=2, padx=10, pady=5, sticky="ew")
            self.min_samples_split_spinbox.set("2")

    def add_manual_row(self, column_name=None, values=None):
        # Continue placing manual rows below parameter widgets
        param_row_end = 8  # End row of the parameter widgets
        current_row = len(self.rows) + param_row_end + 1  # Start adding rows below parameters

        # Your existing code for adding manual rows remains the same, except for updating the row number
        if len(self.rows) < len(self.df.columns):
            combobox = ctk.CTkComboBox(self.scrollable_frame, values=self.df.columns.tolist())
            if column_name:
                combobox.set(column_name)
            combobox.grid(row=current_row, column=0, padx=10, pady=5, sticky="ew")

            spinbox = ttk.Spinbox(self.scrollable_frame, from_=0.0, to=100)
            spinbox.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            if values:
                spinbox.set(values[0])  # Set the spinbox value to the first row of the column

            delete_button = ctk.CTkButton(self.scrollable_frame, text="🗑️", width=20, command=lambda: self.delete_row(combobox))
            delete_button.grid(row=current_row, column=2, padx=10, pady=5, sticky="ew")

            self.rows.append([combobox, spinbox, delete_button])

            self.predict_button.grid(row=current_row + 1, column=0, columnspan=3, pady=10, sticky="ew")

            if len(self.rows) >= len(self.df.columns):
                self.plus_button.configure(state="disabled")
        else:
            self.plus_button.configure(state="disabled")

    def import_excel(self):
        # Open a file dialog to select the Excel file for prediction
        file_path = fd.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            # Load the dataset for prediction
            self.prediction_df = pd.read_excel(file_path)

            # Clear existing rows before adding new ones
            self.clear_existing_rows()

            # Add rows based on the new Excel data
            self.add_prediction_rows()

    def clear_existing_rows(self):
        # Clear all existing rows (comboboxes, spinboxes, and buttons)
        for row in self.rows:
            for widget in row:
                widget.destroy()

        # Clear the rows list and reset the count
        self.rows.clear()

    def add_prediction_rows(self):
        # Populate comboboxes and spinboxes with values from the uploaded Excel sheet
        if self.prediction_df is not None:
            # Iterate over the columns of the Excel file
            for column in self.prediction_df.columns:
                # Create combobox and spinbox for each feature (column in Excel)
                self.add_manual_row(column_name=column, values=self.prediction_df[column].tolist())

    def delete_row(self, combobox):
        # Find the row index dynamically based on the combobox
        row_index = next((i for i, row in enumerate(self.rows) if row[0] == combobox), None)

        if row_index is not None:
            # Remove the widgets for the specified row index
            for widget in self.rows[row_index]:
                widget.destroy()

            # Remove the row from the list
            self.rows.pop(row_index)

            # Re-enable the plus button if rows are deleted and below the maximum
            if len(self.rows) < len(self.df.columns):
                self.plus_button.configure(state="normal")

            # Reposition the remaining rows
            for idx, row in enumerate(self.rows):
                for col_idx, widget in enumerate(row):
                    widget.grid(row=idx + 3, column=col_idx, padx=10, pady=5, sticky="ew")

    def predict_model(self):
        # Ensure that the model is trained on the cleaned_df
        selected_model = self.combo1.get()
                
        if not self.y_column:
            self.display_warning_message("Please select a Y column for prediction.")
            return
            
        input_data = {}
        missing_columns = []  # To store columns not found in df
    
        # Clear previous messages
        self.clear_warning_labels()
    
        # Collect data from the dynamically created ComboBoxes and Spinboxes for prediction
        for idx, row in enumerate(self.rows):
            feature_name = row[0].get().lower()
            feature_value = float(row[1].get())  # Spinbox for feature value
            
            # Check if the feature_name is present in the cleaned_df
            if feature_name in self.cleaned_df.columns.str.lower():
                input_data[feature_name] = feature_value
            else:
                missing_columns.append(feature_name)  # Add missing column name to the list
        
        # Display the warning message in the app frame
        if missing_columns:
            missing_columns_message = f"Warning: The following columns were not found in the dataset and were skipped: {', '.join(missing_columns)}"
            self.display_warning_message1(missing_columns_message)
    
        # Create a DataFrame for the input data for prediction
        if input_data:
            input_df = pd.DataFrame([input_data])
    
            # Access columns in cleaned_df using the stripped and lowercased feature names
            X_train_filtered = self.cleaned_df[input_df.columns.str.lower()]
            y_train_filtered = self.cleaned_df[self.y_column]
    
            # SVM model setup with selected parameters
            if selected_model == "SVM":
                kernel = self.kernel_combo.get()
                C = float(self.c_spinbox.get())
                coef0 = float(self.coef0_spinbox.get())
                degree = int(self.degree_spinbox.get())
    
                model = make_pipeline(StandardScaler(), SVC(kernel=kernel, C=C, coef0=coef0, degree=degree, random_state=42))
    
            # Random Forest model setup with selected parameters
            elif selected_model == "Random Forest":
                n_estimators = int(self.n_estimators_spinbox.get())
                max_depth = None if self.max_depth_spinbox.get() == "None" else int(self.max_depth_spinbox.get())
                min_samples_split = int(self.min_samples_split_spinbox.get())
    
                model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, random_state=42)
    
            else:
                self.display_warning_message("Please select a model.")
                return
            
            # Fit the model and make predictions based on the values entered in the spinboxes
            model.fit(X_train_filtered, y_train_filtered)
            predictions = model.predict(input_df)
            
            # Display the prediction result
            result_text = f"Prediction: {predictions[0]}"
            self.display_warning_message(result_text)
        else:
            self.display_warning_message("No valid columns found for prediction.")
    
    def display_warning_message(self, message):
        # Create a label to display the warning message in the UI
        self.warning_label = ctk.CTkLabel(self.scrollable_frame, text=message, text_color="red", wraplength=600)
        self.warning_label.grid(row=len(self.rows) + 10, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def display_warning_message1(self, message):
        # Create a label to display the warning message in the UI
        self.warning_label = ctk.CTkLabel(self.scrollable_frame, text=message, text_color="red", wraplength=600)
        self.warning_label.grid(row=len(self.rows) + 11, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    
    def clear_warning_labels(self):
        # Clear the previous warning label if it exists
        try:
            self.warning_label.destroy()
        except AttributeError:
            pass