import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tri_data_handling import FileManager, process_data, filter_data, save_data, get_analyze_dir

def create_visualizations():
    file_manager=FileManager()
    data = file_manager.get_data()
    file_path = file_manager.get_file_path()
    if data is None:
        print("No analysis file found.")
        return

    data = process_data(data)
    print(data.head())

    #Poista ääriarvot ja virheelliset arvot. TÄTÄ EI TARVITA KUN LOAD DATA TOIMINNALLISUUS ON SUUNNITELTU LOPPUUN. 
    filtered_data, _ = filter_data(data)  # Tallentaa tiedoston tupleksi. Filtered data eli tuplen eka arvo on, mitä halutaan.

    output_dir = get_analyze_dir(file_path)
    #print(f"Output directory: {output_dir}")

    # Varmista tulostushakemisto on olemassa
    #if not os.path.exists(output_dir):
        #os.makedirs(output_dir)
        #print(f"Created directory: {output_dir}")

    def format_time(x, pos):
        h = int(x // 3600)
        m = int((x % 3600) // 60)
        return f"{h:02d}:{m:02d}"

    # Kokonaisajan jakauma
    min_total_time = filtered_data['Total_sec'].min()
    plt.figure(figsize=(15, 6))
    sns.histplot(filtered_data['Total_sec'], bins=50, kde=True)
    plt.title('Kokonaisajan jakauma')
    plt.xlabel('Kokonaisaika')
    plt.ylabel('Frekvenssi')
    plt.xlim(min_total_time, 18 * 3600)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_time))
    plt.xticks(rotation=45)
    save_data(plt, 'total_time_distribution.png', output_dir)
    plt.close()

    #Viiksikaavio
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='AG', y='Total_sec', data=filtered_data)
    plt.title('Total time by age group')
    plt.xlabel('Age group')
    plt.ylabel('Total time')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_time))
    save_data(plt, 'age_group_boxplot.png', output_dir)
    plt.close()

    # Korrelaatiomatriisi
    correlation = filtered_data[['Swim_sec', 'Bike_sec', 'Run_sec', 'Total_sec']].corr()
    correlation.index = ['Swim', 'Bike', 'Run', 'Total']
    correlation.columns = ['Swim', 'Bike', 'Run', 'Total']
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix')
    save_data(plt, 'correlation_matrix.png', output_dir)
    plt.close()

    # Hajontakaavio osa-aikojen ja kokonaisajan välillä
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Bike_sec', y='Total_sec', data=filtered_data)
    plt.title('Bike vs Total')
    plt.xlabel('Bike leg')
    plt.ylabel('Total time')
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_time))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_time))
    save_data(plt, 'bike_vs_total_scatter.png', output_dir)
    plt.close()

    # Hajontakaavio uinti vs total
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Swim_sec', y='Total_sec', data=filtered_data)
    plt.title('Swim vs total')
    plt.xlabel('Swim time')
    plt.ylabel('Total time')
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_time))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_time))
    save_data(plt, 'swim_vs_total_scatter.png', output_dir)
    plt.close()

    # Hajontakaavio juoksu vs Total
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Run_sec', y='Total_sec', data=filtered_data)
    plt.title('Run vs Total time')
    plt.xlabel('Run time')
    plt.ylabel('Total time')
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_time))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_time))
    save_data(plt, 'run_vs_total_scatter.png', output_dir)
    plt.close()

    # Kokonaisaikojen keskiarvo ikäryhmittäin ja kaikille urheilijoille
    age_group_means = filtered_data.groupby('AG')['Total_sec'].mean()
    
    # Erotetaan mies- ja naisikäryhmät
    male_groups = age_group_means[age_group_means.index.str.startswith('M')]
    female_groups = age_group_means[age_group_means.index.str.startswith('F')]
    
    male_mean = male_groups.mean()
    female_mean = female_groups.mean()
    overall_mean = filtered_data['Total_sec'].mean()
    
    # Lisää keskiarvot vertailua varten
    male_mean_series = pd.Series(male_mean, index=['Male Overall'])
    female_mean_series = pd.Series(female_mean, index=['Female Overall'])
    overall_mean_series = pd.Series(overall_mean, index=['Overall'])
    comparison_data = pd.concat([female_groups, female_mean_series, male_groups, male_mean_series, overall_mean_series])

    # Laske y-akselin minimi (nopein keskiarvo - 15 minuuttia. Luettavuuden kannalta vaikuttaisi optimilta)
    min_mean = comparison_data.min()
    y_min = max(0, min_mean - 900)  # Varmistetaan, ettei y_min ole negatiivinen
    max_y = comparison_data.max() + 3600

    plt.figure(figsize=(12, 6))
    comparison_data.plot(kind='bar', color='skyblue')
    plt.title('Total time mean by age groups and all athletes')
    plt.xlabel('Age group')
    plt.ylabel('Total time (hh:mm)')
    plt.ylim(y_min, max_y) 
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_time))
    plt.xticks(rotation=45)

    # Lisää keskiarvon lukemat palkkien yläpuolelle
    for index, value in enumerate(comparison_data):
        plt.text(index, value + 300, format_time(value, None), ha='center')

    plt.tight_layout()
    save_data(plt, 'age_group_vs_overall_mean.png', output_dir)
    plt.close()

    # Kokonaisaikojen minimit ikäryhmittäin ja kaikille urheilijoille
    age_group_min = filtered_data.groupby('AG')['Total_sec'].min()
    
    male_min = age_group_min[age_group_min.index.str.startswith('M')]
    female_min = age_group_min[age_group_min.index.str.startswith('F')]
    
    male_min_value = male_min.min()
    female_min_value = female_min.min()
    overall_min_value = filtered_data['Total_sec'].min()
    
    #minimiarvot vertailuun
    male_min_series = pd.Series(male_min_value, index=['Male Fastest'])
    female_min_series = pd.Series(female_min_value, index=['Female Fastest'])
    overall_min_series = pd.Series(overall_min_value, index=['Overall Fastest'])
    min_comparison_data = pd.concat([female_min, female_min_series, male_min, male_min_series, overall_min_series])

    # Laske y-akselin minimi (nopein aika - 15 minuuttia, kts yllä)
    min_time = min_comparison_data.min()
    y_min = max(0, min_time - 900)  # Varmistetaan, ettei y_min ole negatiivinen

    plt.figure(figsize=(12, 6))
    min_comparison_data.plot(kind='bar', color='coral')
    plt.title('Fastest times by age group and all athletes')
    plt.xlabel('Age group')
    plt.ylabel('Total time (hh:mm)')
    plt.ylim(y_min, max_y) 
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_time))
    plt.xticks(rotation=45)

    #Minimiarvot palkkien yläpuolelle
    for index, value in enumerate(min_comparison_data):
        plt.text(index, value + 300, format_time(value, None), ha='center')

    plt.tight_layout()
    save_data(plt, 'age_group_vs_overall_min.png', output_dir)
    plt.close()
