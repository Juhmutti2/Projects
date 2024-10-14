from scipy.stats import spearmanr, pearsonr, ttest_ind, f_oneway
from tri_data_handling import process_data

def calculate_spearman(data, col1, col2):
    correlation, p_value = spearmanr(data[col1], data[col2])
    print(f"Spearman correlation between {col1} and {col2}: {correlation}, p-value: {p_value}")
    return correlation, p_value

def calculate_pearson(data, col1, col2):
    correlation, p_value = pearsonr(data[col1], data[col2])
    print(f"Pearson correlation between {col1} and {col2}: {correlation}, p-value: {p_value}")
    return correlation, p_value

def perform_ttest(group1, group2):
    t_stat, p_value = ttest_ind(group1, group2)
    print(f"T-test between groups: t-statistic: {t_stat}, p-value: {p_value}")
    return t_stat, p_value

def perform_anova(*groups):
    f_stat, p_value = f_oneway(*groups)
    print(f"ANOVA test across groups: F-statistic: {f_stat}, p-value: {p_value}")
    return f_stat, p_value

def calculate_correlation(data):
    # Esikäsitellään data käyttämällä process_data-funktiota
    data = process_data(data)
    # Lasketaan korrelaatio esikäsitellyllä datalla
    correlation = data[['Swim_sec', 'Bike_sec', 'Run_sec', 'Total_sec']].corr()
    return correlation

