import pandas as pd
import os

class FileManager:
    _instance = None
    _file_path = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
        return cls._instance

    def load_file(self, file_path):
        """
        Lataa tiedoston ja tallentaa sen ohjelman käyttöön.
        """
        if file_path and os.path.exists(file_path):
            self._file_path = file_path
            raw_data = pd.read_csv(file_path)
            self._data = process_data(raw_data)
            print(f"Tiedosto {file_path} ladattu onnistuneesti.")
        else:
            raise FileNotFoundError(f"Tiedostoa ei löydy: {file_path}")

    def get_file_path(self):

        if self._file_path:
            return self._file_path
        else:
            raise FileNotFoundError("Tiedostoa ei ole ladattu.")

    def get_data(self):

        if self._data is not None:
            return self._data
        else:
            raise ValueError("Tiedostoa ei ole ladattu tai dataa ei ole saatavilla.")

def load_data_from_file(file_path):

    try:
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            #Esikäsittele data (jos tarpeen)
            data = process_data(data)
            return data
        else:
            print(f"Tiedostoa ei löydy polusta: {file_path}")
            return None
    except Exception as e:
        print(f"Error loading data from file {file_path}: {e}")
        raise

def get_analyze_dir(file_path=None):
    """
    Määrittää analyysikansion ladatun tiedoston perusteella.
    Jos file_path on annettu, käytetään sitä. Muussa tapauksessa
    FileManagerista haetaan ladatun tiedoston polku.
    """
    file_manager = FileManager()

    # Käytetään annettua tiedostopolkua tai haetaan FileManagerista
    if file_path is None:
        file_path = file_manager.get_file_path()

    # Tarkista, onko tiedostopolku käytettävissä
    if not file_path:
        raise ValueError("Analysoitavaa tiedostoa ei ole ladattu tai tiedostopolku on virheellinen.")

    # Määritä analyysikansion polku tiedoston perusteella
    file_directory = os.path.dirname(os.path.abspath(file_path))
    base_name = os.path.basename(file_path).replace('_athlete_analyze_version.csv', '')
    analyze_dir = os.path.join(file_directory, f"{base_name}_analytics")

    # Tarkista, onko analyysikansio olemassa. Jos ei, luo se. 
    if not os.path.exists(analyze_dir):
        os.makedirs(analyze_dir)
        print(f"Analyysikansio luotu: {analyze_dir}")
    else:
        print(f"Käytetään olemassa olevaa analyysikansiota: {analyze_dir}")

    return analyze_dir

def save_data(data, file_name, output_dir=None):

    # haetaan FileManagerista tallennuskansio
    if output_dir is None:
        file_manager = FileManager()
        file_path = file_manager.get_file_path()
        output_dir = get_analyze_dir(file_path)

    # Luo hakemisto, jos sitä ei ole olemassa
    os.makedirs(output_dir, exist_ok=True)

    # Määritä tallennuspolku
    output_path = os.path.join(output_dir, file_name)

    # Tallenna data tiedostoon ylikirjoittaen olemassa olevan tiedoston
    if isinstance(data, pd.DataFrame):
        data.to_csv(output_path, index=False)
    elif isinstance(data, str):
        with open(output_path, 'w') as f:  
            f.write(data + '\n')
    elif hasattr(data, 'savefig'): 
        data.savefig(output_path)
    else:
        raise ValueError("Data should be either a DataFrame, a string, or a matplotlib figure.")

    print(f"Data saved to {output_path}")

    return output_path

def get_analysis_data(directory='.',root_dir='.'):
    """
    Hakee viimeisimmän analysoitavaksi tarkoitetun .csv tiedoston,
    jonka nimessä on 'analyze_version' annetusta hakemistosta ja sen alihakemistoista.
    TÄSSÄ VOI OLLA HEIKKOUS MYÖHEMMIN KUN HALUTAAN LAAJENTAA TOIMINTAA.

    Parameters:
    directory (str): Hakemisto, josta etsitään tiedostoja.

    Returns:dir
    str: Uusimman analysoitavaksi tarkoitetun tiedoston polku tai None, jos tiedostoja ei löydy.
    """
    latest_file = None
    latest_mtime = 0

    for dirpath, _, filenames in os.walk(directory):
        for csv_file in filenames:
            if csv_file.endswith('.csv') and '_athlete_analyze_version' in csv_file:
                file_path = os.path.join(dirpath, csv_file)
                file_mtime = os.path.getmtime(file_path)
                if file_mtime > latest_mtime:
                    latest_mtime = file_mtime
                    latest_file = file_path
    if latest_file:
        relative_file_path = os.path.relpath(latest_file, root_dir)
        return relative_file_path
    else:
        print("No suitable file found for analysis.")
        return None

def get_latest_data_file(directory='.'):
    latest_file = None
    latest_mtime = 0

    for dirpath, _, filenames in os.walk(directory):
        csv_files = [f for f in filenames if f.endswith('.csv')]
        for csv_file in csv_files:
            file_path = os.path.join(dirpath, csv_file)
            file_mtime = os.path.getmtime(file_path)
            if file_mtime > latest_mtime:
                latest_mtime = file_mtime
                latest_file = file_path

    return latest_file

def process_data(data, keep_original=False):
    """
    Esikäsittelee ja puhdistaa datan. 
    Vaihtoehtoisesti säilyttää alkuperäisen datan.

    Parameters:
    - data (pd.DataFrame): Käsiteltävä DataFrame.
    - keep_original (bool): Jos True, palauttaa alkuperäisen datan käsitellyn datan lisäksi.

    Returns:
    - data (pd.DataFrame): Käsitelty data.
    - original_data (pd.DataFrame, optional): Alkuperäinen data, jos keep_original=True.
    """
    def time_to_seconds(time_str):
        if pd.isna(time_str) or time_str == '00:00:00':
            return None
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    data['Swim_sec'] = data['Swim'].apply(time_to_seconds)
    data['Bike_sec'] = data['Bike'].apply(time_to_seconds)
    data['Run_sec'] = data['Run'].apply(time_to_seconds)
    data['Total_sec'] = data['Total'].apply(time_to_seconds)

    if keep_original:
        original_data = data.copy()
        return data, original_data
    return data

def filter_data(data):
    """
    Suodattaa urheilijat pois, joiden aika ylittää tietyn rajan tai aika on puuttuva.
    Palauttaa suodatetun datan ja poistetut rivit.

    Parameters:
    - data (pd.DataFrame): Käsiteltävä DataFrame.

    Returns:
    - Tuple (pd.DataFrame, pd.DataFrame): Suodatettu data ja poistetut rivit.
    """
    max_limits = {
        'Swim_sec': 2 * 3600 + 45 * 60,
        'Bike_sec': 10 * 3600,
        'Run_sec': 9 * 3600,
        'Total_sec': 18.5 * 3600
    }
    original_data = data.copy()
    for col, limit in max_limits.items():
        data = data[(data[col] <= limit) & (data[col].notnull())]

    removed_data = original_data[~original_data.index.isin(data.index)]
    return data, removed_data

def seconds_to_time(seconds):
    """
    Muuntaa sekunnit muotoon HH:MM:SS.
    """
    if pd.isna(seconds) or seconds is None:
        return '00:00:00'
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
