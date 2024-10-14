import pandas as pd
import os
from tri_data_handling import process_data, get_analysis_data, seconds_to_time, save_data, get_analyze_dir
from tri_statistical_tests import calculate_spearman, calculate_pearson

class TriathlonAnalyzer:
    def __init__(self, file_path=None):
        self.file_path = os.path.abspath(file_path)

        if file_path is None:
            file_path = get_analysis_data()
            if file_path is None:
                raise FileNotFoundError("No data file found.")
        print({file_path})

        print(f"File path being used: {self.file_path}")

        raw_data = pd.read_csv(self.file_path)
        self.data, self.original_data = process_data(raw_data, keep_original=True)  # Palauta alkuperäinen data

        # Puhdista data: korvaa inf ja poista NaN
        self.data.replace([pd.NA, float('inf'), float('-inf')], pd.NA, inplace=True)
        self.data.dropna(subset=['Swim_sec', 'Bike_sec', 'Run_sec', 'Total_sec'], inplace=True)

        # Määritä analyysikansio
        self.output_dir = get_analyze_dir(self.file_path)

    def get_original_data(self):
        return self.original_data


    def analyze_data(self):
 
        self.data['Swim_time'] = self.data['Swim_sec'].apply(seconds_to_time)
        self.data['Bike_time'] = self.data['Bike_sec'].apply(seconds_to_time)
        self.data['Run_time'] = self.data['Run_sec'].apply(seconds_to_time)
        self.data['Total_time'] = self.data['Total_sec'].apply(seconds_to_time)

        statistics = self.data[['Swim_sec', 'Bike_sec', 'Run_sec', 'Total_sec']].describe()
        statistics.columns = ['Swim', 'Bike', 'Run', 'Total']
        statistics = statistics.loc[:, (statistics.loc['min'] != 0)]

        result_text = "\nBasic statistics:\n"
        num_athletes = len(self.data)
        result_text += f"Total number of athletes: {num_athletes}\n"

        # Lasketaan naisten lukumäärä ja prosenttiosuus
        num_females = self.data[self.data['AG'].str.startswith('F')].shape[0]
        female_percentage = (num_females / num_athletes) * 100 if num_athletes > 0 else 0
        result_text += f"Number of female athletes: {num_females} ({female_percentage:.2f}%)\n"

        def convert_stats_to_time(stats):
            time_stats = stats.copy()
            for column in stats.columns:
                time_stats[column] = stats[column].apply(seconds_to_time)
            return time_stats

        time_statistics = convert_stats_to_time(statistics.drop('count'))
        result_text += time_statistics.to_string() + "\n"

        #print(result_text)  # Tulosta perusstatistiikka konsoliin

        # Korrelaatioanalyysi käyttämällä Pearsonin ja Spearmanin korrelaatiota, peet erittäin pienille arvoille.
        def format_p_value(p_value):
            if p_value == 0:
                return "p-value < 1e-300"  # Jos p-arvo on erittäin pieni, merkataan näin
            return f"{p_value:.3g}"  # Muotoillaan pienet arvot 3 merkittävällä numerolla
        
        pearson_corr_swim, pearson_p_swim = calculate_pearson(self.data, 'Swim_sec', 'Total_sec')
        spearman_corr_swim, spearman_p_swim = calculate_spearman(self.data, 'Swim_sec', 'Total_sec')

        pearson_corr_bike, pearson_p_bike = calculate_pearson(self.data, 'Bike_sec', 'Total_sec')
        spearman_corr_bike, spearman_p_bike = calculate_spearman(self.data, 'Bike_sec', 'Total_sec')

        pearson_corr_run, pearson_p_run = calculate_pearson(self.data, 'Run_sec', 'Total_sec')
        spearman_corr_run, spearman_p_run = calculate_spearman(self.data, 'Run_sec', 'Total_sec')

        # Päivitetään tulostuksen korrelaatiot
        result_text += f"\nPearson's correlation (Swim vs Total): correlation = {pearson_corr_swim:.4f}, {format_p_value(pearson_p_swim)}\n"
        result_text += f"Pearson's correlation (Bike vs Total): correlation = {pearson_corr_bike:.4f}, {format_p_value(pearson_p_bike)}\n"
        result_text += f"Pearson's correlation (Run vs Total): correlation = {pearson_corr_run:.4f}, {format_p_value(pearson_p_run)}\n"

        result_text += f"\nSpearman's correlation (Swim vs Total): correlation = {spearman_corr_swim:.4f}, {format_p_value(spearman_p_swim)}\n"
        result_text += f"Spearman's correlation (Bike vs Total): correlation = {spearman_corr_bike:.4f}, {format_p_value(spearman_p_bike)}\n"
        result_text += f"Spearman's correlation (Run vs Total): correlation = {spearman_corr_run:.4f}, {format_p_value(spearman_p_run)}\n"

        # Tulostetaan myös konsoliin siistitysti
        print("\nKorrelaatioanalyysi (Pearson):")
        print(f"Swim vs Total: correlation = {pearson_corr_swim:.4f}, {format_p_value(pearson_p_swim)}")
        print(f"Bike vs Total: correlation = {pearson_corr_bike:.4f}, {format_p_value(pearson_p_bike)}")
        print(f"Run vs Total: correlation = {pearson_corr_run:.4f}, {format_p_value(pearson_p_run)}")

        print("\nKorrelaatioanalyysi (Spearman):")
        print(f"Swim vs Total: correlation = {spearman_corr_swim:.4f}, {format_p_value(spearman_p_swim)}")
        print(f"Bike vs Total: correlation = {spearman_corr_bike:.4f}, {format_p_value(spearman_p_bike)}")
        print(f"Run vs Total: correlation = {spearman_corr_run:.4f}, {format_p_value(spearman_p_run)}")

        #Total, mediaani ja keskiarvo
        total_median = self.data['Total_sec'].median()
        total_mean = self.data['Total_sec'].mean()

        result_text += f"\nTotal median: {seconds_to_time(total_median)}\n"
        result_text += f"Total mean: {seconds_to_time(total_mean)}\n"

        print(f"\nKokonaisajan mediaani: {seconds_to_time(total_median)}")
        print(f"Kokonaisajan keskiarvo: {seconds_to_time(total_mean)}")

        # Min/Max-arvot ja urheilijarivien tulostus
        min_text, min_rows = self.get_extreme_athletes('min')
        max_text, max_rows = self.get_extreme_athletes('max')

        result_text += "\n" + min_text + "\n" + max_text
        print(min_text)
        print(max_text)

        # Tallenna analyysin tulokset YLIKIRJOITTAMALLA
        save_data(result_text, 'analysis_results.txt', output_dir=self.output_dir)

        # Tallenna min/max urheilijarivit .csv-tiedostoon
        min_max_df = pd.concat(min_rows + max_rows).drop(columns=['Swim_sec', 'Bike_sec', 'Run_sec', 'Total_sec', 'Swim_time', 'Bike_time', 'Run_time', 'Total_time'], errors='ignore')
        save_data(min_max_df, 'min_max_athletes.csv', output_dir=self.output_dir)

        return result_text

    def get_extreme_athletes(self, max_or_min='max'):
        if max_or_min not in ['max', 'min']:
            raise ValueError("Invalid value for max_or_min. Choose 'max' or 'min'.")

        # Valitse oikea funktio max tai min arvon saamiseksi
        func = max if max_or_min == 'max' else min

        swim_extreme = self.data.loc[self.data['Swim_sec'] == func(self.data['Swim_sec'])]
        bike_extreme = self.data.loc[self.data['Bike_sec'] == func(self.data['Bike_sec'])]
        run_extreme = self.data.loc[self.data['Run_sec'] == func(self.data['Run_sec'])]
        total_extreme = self.data.loc[self.data['Total_sec'] == func(self.data['Total_sec'])]

        #Tarpeettomat sarakkeet veks
        columns_to_remove = ['Swim_sec', 'Bike_sec', 'Run_sec', 'Total_sec', 'Swim_time', 'Bike_time', 'Run_time', 'Total_time']
        swim_extreme = swim_extreme.drop(columns=columns_to_remove, errors='ignore')
        bike_extreme = bike_extreme.drop(columns=columns_to_remove, errors='ignore')
        run_extreme = run_extreme.drop(columns=columns_to_remove, errors='ignore')
        total_extreme = total_extreme.drop(columns=columns_to_remove, errors='ignore')

        #Sarakeleveys
        column_widths = {
            "Index": 6, "Ovr": 5, "Gen": 5, "Div": 5, "Name": 20, "#": 4,
            "AG": 7, "Country": 7, "Swim": 9, "Bike": 9, "Run": 9,
            "Total": 9, "Competition": 25, "Year": 25
        }

        #Tulostus
        def format_row(row):
            return " ".join(f"{str(value):<{column_widths[col]}}" for col, value in row.items())

        def format_headers(columns):
            return " ".join(f"{col:<{column_widths[col]}}" for col in columns)

        headers = list(swim_extreme.columns)
        headers_text = format_headers(headers)

        extreme_text = f"{max_or_min.capitalize()} Athletes:\n"
        extreme_text += f"Swim:\n{headers_text}\n" + "\n".join(swim_extreme.apply(format_row, axis=1)) + "\n\n"
        extreme_text += f"Bike:\n{headers_text}\n" + "\n".join(bike_extreme.apply(format_row, axis=1)) + "\n\n"
        extreme_text += f"Run:\n{headers_text}\n" + "\n".join(run_extreme.apply(format_row, axis=1)) + "\n\n"
        extreme_text += f"Total:\n{headers_text}\n" + "\n".join(total_extreme.apply(format_row, axis=1)) + "\n"

        return extreme_text, [swim_extreme, bike_extreme, run_extreme, total_extreme]


def analyze_data(file_path):
    analyzer = TriathlonAnalyzer(file_path)
    return analyzer.analyze_data()

def save_extremes_to_file(file_path, extreme_type, swim, bike, run, total):
    output_text = (
        f"{extreme_type.capitalize()} Extremes:\n"
        f"Swim: {swim}\n"
        f"Bike: {bike}\n"
        f"Run: {run}\n"
        f"Total: {total}\n"
    )
    save_data(output_text, f'{extreme_type}_extremes.txt', output_dir=os.path.dirname(file_path), mode='w')
