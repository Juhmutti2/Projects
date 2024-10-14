import pandas as pd
import os

def detect_age_group_column(df):

    for col in df.columns:
        if df[col].dtype == object and all(df[col].str.match(r'^[MF]\d{2}-\d{2}$', na=False)):
            return col
    return None

def normalize_age_group(age_group):

    if pd.isna(age_group):
        return age_group
    return age_group.upper().replace('N', 'F')

def get_unique_filename(directory, filename):

    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    return unique_filename

def merge_files(primary_file, secondary_file, output_dir='.'):

    #debug printit 
    #print(f"Primary file: {primary_file}")
    #print(f"Secondary file: {secondary_file}")
    
    primary_df = pd.read_csv(primary_file)
    secondary_df = pd.read_csv(secondary_file)
    

    primary_age_group_col = detect_age_group_column(primary_df)
    secondary_age_group_col = detect_age_group_column(secondary_df)
    
    if primary_age_group_col and secondary_age_group_col:
        secondary_df[secondary_age_group_col] = secondary_df[secondary_age_group_col].apply(normalize_age_group)
    
    if not all(col in secondary_df.columns for col in primary_df.columns):
        raise ValueError("Secondary file does not have the same columns as the primary file.")
    
    # Yhdistä tiedostot
    combined_df = pd.concat([primary_df, secondary_df], ignore_index=True)
    
    #Määritä tallennustiedoston nimi
    primary_filename = os.path.splitext(os.path.basename(primary_file))[0]
    output_filename = f"{primary_filename}_merged.csv"
    
    # Luo uusi hakemisto
    output_folder = f"{primary_filename}_merged_folder"
    full_output_dir = os.path.join(output_dir, output_folder)
    os.makedirs(full_output_dir, exist_ok=True)
    
    output_filename = get_unique_filename(full_output_dir, output_filename)
    output_path = os.path.join(full_output_dir, output_filename)
    
    # Debug printit output-poluille
    #print(f"Output folder: {full_output_dir}")
    #print(f"Output file: {output_path}")
    
    # Tallenna yhdistetty tiedosto
    combined_df.to_csv(output_path, index=False)
    
    print(f"Merged file saved to: {output_path}")
    return output_path
