from tri_data_handling import save_data, get_analyze_dir, seconds_to_time

def age_group_summary(data, file_path):
    # Tarkista, että file_path on merkkijono
    if not isinstance(file_path, str):
        raise TypeError(f"Expected file_path to be a string, but got {type(file_path)}")

    # Ryhmittele data ikäryhmittäin
    grouped = data.groupby('AG')

    # Määritä analyysikansio analysoitavan tiedoston perusteella
    output_dir = get_analyze_dir(file_path)
    output_file = 'age_group_analysis.txt'
    result_text = ""

    for name, group in grouped:
        group_desc = group.describe()
        fastest_athlete = group.loc[group['Total_sec'].idxmin()]

        time_stats = ['mean', 'std', '25%', '50%', '75%', 'max']
        time_cols = ['Swim_sec', 'Bike_sec', 'Run_sec', 'Total_sec']

        time_data = {col: {stat: seconds_to_time(group_desc[col][stat]) for stat in time_stats} for col in time_cols}

        num_athletes = group.shape[0]
        age_group_info = f"Age group {name}:\nTotal number of athletes: {num_athletes}\n"
        age_group_info += "           Swim      Bike       Run     Total\n"
        for stat in time_stats:
            swim = time_data['Swim_sec'][stat]
            bike = time_data['Bike_sec'][stat]
            run = time_data['Run_sec'][stat]
            total = time_data['Total_sec'][stat]
            age_group_info += f"{stat:4}  {swim}  {bike}  {run}  {total}\n"

        fastest_swimmer = group.loc[group['Swim_sec'].idxmin()]
        fastest_biker = group.loc[group['Bike_sec'].idxmin()]
        fastest_runner = group.loc[group['Run_sec'].idxmin()]

        greatest_gladiators = f"Greatest gladiators of {name}:\n"
        greatest_gladiators += (f"Fastest athlete: {fastest_athlete['Name']}, "
                                f"Swim: {seconds_to_time(fastest_athlete['Swim_sec'])}, "
                                f"Bike: {seconds_to_time(fastest_athlete['Bike_sec'])}, "
                                f"Run: {seconds_to_time(fastest_athlete['Run_sec'])}, "
                                f"Total: {seconds_to_time(fastest_athlete['Total_sec'])}\n")

        if fastest_swimmer['Name'] == fastest_athlete['Name']:
            greatest_gladiators += "Fastest swimmer: see fastest athlete\n"
        else:
            greatest_gladiators += (f"Fastest swimmer: {fastest_swimmer['Name']}, "
                                    f"Swim: {seconds_to_time(fastest_swimmer['Swim_sec'])}, "
                                    f"Bike: {seconds_to_time(fastest_swimmer['Bike_sec'])}, "
                                    f"Run: {seconds_to_time(fastest_swimmer['Run_sec'])}, "
                                    f"Total: {seconds_to_time(fastest_swimmer['Total_sec'])}\n")

        if fastest_biker['Name'] == fastest_athlete['Name']:
            greatest_gladiators += "Fastest cyclist: see fastest athlete\n"
        elif fastest_biker['Name'] == fastest_swimmer['Name']:
            greatest_gladiators += f"Fastest cyclist: {fastest_biker['Name']}, see fastest swimmer\n"
        else:
            greatest_gladiators += (f"Fastest cyclist: {fastest_biker['Name']}, "
                                    f"Swim: {seconds_to_time(fastest_biker['Swim_sec'])}, "
                                    f"Bike: {seconds_to_time(fastest_biker['Bike_sec'])}, "
                                    f"Run: {seconds_to_time(fastest_biker['Run_sec'])}, "
                                    f"Total: {seconds_to_time(fastest_biker['Total_sec'])}\n")

        if fastest_runner['Name'] == fastest_athlete['Name']:
            greatest_gladiators += "Fastest runner: see fastest athlete\n"
        elif fastest_runner['Name'] == fastest_swimmer['Name']:
            greatest_gladiators += f"Fastest runner: {fastest_runner['Name']}, see fastest swimmer\n"
        elif fastest_runner['Name'] == fastest_biker['Name']:
            greatest_gladiators += f"Fastest runner: {fastest_runner['Name']}, see fastest cyclist\n"
        else:
            greatest_gladiators += (f"Fastest runner: {fastest_runner['Name']}, "
                                    f"Swim: {seconds_to_time(fastest_runner['Swim_sec'])}, "
                                    f"Bike: {seconds_to_time(fastest_runner['Bike_sec'])}, "
                                    f"Run: {seconds_to_time(fastest_runner['Run_sec'])}, "
                                    f"Total: {seconds_to_time(fastest_runner['Total_sec'])}\n")
        if (fastest_athlete['Name'] == fastest_swimmer['Name'] and
            fastest_athlete['Name'] == fastest_biker['Name'] and
            fastest_athlete['Name'] == fastest_runner['Name']):
                greatest_gladiators += f"{fastest_athlete['Name']} YOU ARE AN IRONMAN\n"

        result_text += age_group_info + greatest_gladiators + "\n"

    save_data(result_text, output_file, output_dir=output_dir)

    return output_dir, output_file, result_text

