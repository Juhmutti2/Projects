import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import pandas as pd
from tri_data_handling import FileManager
from tri_analysis import analyze_data
from tri_visualizations import create_visualizations
from tri_statistical_tests import calculate_correlation
from tri_age_group_analysis import age_group_summary
from tri_merge_files import merge_files



def create_interface():
    root = tk.Tk()
    root.title("Triathlon Analyysityökalu")
    root.geometry("1500x600")

    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    button_frame = tk.Frame(main_frame, width=150, height=600)
    button_frame.pack(side='right', fill='y')
    button_frame.pack_propagate(False)

    output_frame = tk.Frame(main_frame, width=1400, height=600)
    output_frame.pack(side='left', fill='both', expand=True)
    output_frame.pack_propagate(False)

    global output_text
    output_text = scrolledtext.ScrolledText(output_frame, wrap='word', height=600, width=800)
    output_text.pack(fill='both', expand=True)

    tk.Button(button_frame, text="Open file", command=load_data_ui).pack(fill='x', pady=5)
    tk.Button(button_frame, text="Analyze data", command=analyze_data_ui).pack(fill='x', pady=5)
    tk.Button(button_frame, text="Create visuals", command=create_visualizations_ui).pack(fill='x', pady=5)
    tk.Button(button_frame, text="Correlation analysis", command=correlation_analysis_ui).pack(fill='x', pady=5)
    tk.Button(button_frame, text="Age group-analysis", command=age_group_analysis_ui).pack(fill='x', pady=5)
    tk.Button(button_frame, text="Merge files", command=merge_files_ui).pack(fill='x', pady=5)
    tk.Button(button_frame, text="Quit", command=root.quit).pack(fill='x', pady=5)

    root.mainloop()

def load_data_ui():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return None
    output_text.insert(tk.END, f"Loading data from {file_path}...\n")
    
    try:
        # Ladataan tiedosto FileManager-luokkaan
        file_manager = FileManager()
        file_manager.load_file(file_path)

        output_text.insert(tk.END, f"Data loaded successfully")
    except Exception as e:
        output_text.insert(tk.END, f"Error loading data: {e}\n")

def analyze_data_ui():
    file_manager = FileManager()
    data = file_manager.get_data()
    file_path = file_manager.get_file_path() 
    if data is not None and not data.empty:
        output_text.insert(tk.END, "Analyzing data...\n")
        result_text = analyze_data(file_path)
        output_text.insert(tk.END, result_text + "\n")
        output_text.insert(tk.END, "Data analysis completed.\n\n")
    else:
        output_text.insert(tk.END, "No data file found for analysis.\n\n")

def create_visualizations_ui():
    file_manager=FileManager()
    data = file_manager.get_data()
    if data is not None and not data.empty:
        output_text.insert(tk.END, "\nCreating visualizations...\n")
        create_visualizations()
        output_text.insert(tk.END, "Visualizations created.\n\n")
    else:
        output_text.insert(tk.END, "No data file found for visualizations.\n\n")

def correlation_analysis_ui():
    file_manager=FileManager()
    data= file_manager.get_data()
    if data is not None and not data.empty:
        output_text.insert(tk.END, "\n Performing correlation analysis...\n")

        corr_matrix = calculate_correlation(data)
        output_text.insert(tk.END, "Correlation Matrix:\n" + corr_matrix.to_string() + "\n\n")

        output_text.insert(tk.END, "Correlation analysis completed.\n\n")
    else:
        output_text.insert(tk.END, "No data file found for correlation analysis.\n\n")

def age_group_analysis_ui():
    file_manager = FileManager()

    try:
   
        data = file_manager.get_data()
        if data is not None and not data.empty:
            output_text.insert(tk.END, "\nPerforming age group analysis...\n")
            file_path = file_manager.get_file_path()

            #Suorita ikäsarja-analyysi, luo tuloste
            result = age_group_summary(data, file_path)

            if result is not None and len(result) == 3:
                output_dir, output_file, result_text = result
  
                output_text.insert(tk.END, result_text + "\n")
                output_text.insert(tk.END, f"Analysis complete.\nResults saved to directory: {output_dir}\n")
            else:
                output_text.insert(tk.END, "Analysis did not complete successfully.\n")
        else:
            output_text.insert(tk.END, "No data file found.\n")
    except Exception as e:
        output_text.insert(tk.END, f"An error occurred: {str(e)}\n")

def merge_files_ui():
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Yhdistetään tiedostot...\n")
    
    #Valitse päätiedosto
    primary_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Valitse päätiedosto")
    if not primary_file_path:
        messagebox.showerror("Error", "Ei tiedostoa valittuna päätiedostoksi.")
        return
    
    #Valitse liitettävä tiedosto
    secondary_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Valitse liitettävä tiedosto")
    if not secondary_file_path:
        messagebox.showerror("Error", "Ei tiedostoa valittuna liitettäväksi.")
        return
    
    try:
        #yhdistä tiedostot
        merged_file_path = merge_files(primary_file_path, secondary_file_path)
        output_text.insert(tk.END, f"Tiedostot yhdistetty onnistuneesti: {merged_file_path}\n")
    except Exception as e:
        output_text.insert(tk.END, f"Virhe tiedostojen yhdistämisessä: {str(e)}\n")

if __name__ == "__main__":
    create_interface()
