import os
import pandas as pd


def match_value_with_time_sequence_mean(original_data, matched_monthly_data, field):

    for line_original_data in range(0, len(original_data)):
        for line_matched_data in range(0, len(matched_monthly_data)):
            if matched_monthly_data.loc[line_matched_data, 'Site'] == original_data.loc[line_original_data, 'Site']:
                Year_start = original_data.loc[line_original_data, 'Year_start']
                Month_start = original_data.loc[line_original_data, 'Month_start']
                Year_end = original_data.loc[line_original_data, 'Year_end']
                Month_end = original_data.loc[line_original_data, 'Month_end']
                if pd.isna(Year_start):
                    continue
                if pd.isna(Month_start):
                    continue
                if pd.isna(Year_end):
                    continue
                if pd.isna(Month_end):
                    continue

                Year_start = str(int(Year_start)).zfill(4)
                Month_start = str(int(Month_start)).zfill(2)
                Year_end = str(int(Year_end)).zfill(4)
                Month_end = str(int(Month_end)).zfill(2)

                time_start = Year_start+'-'+Month_start
                time_end = Year_end+'-'+Month_end

                time_start = pd.to_datetime(time_start)
                time_end = pd.to_datetime(time_end)
                sum_value = 0
                for time_sequence in pd.date_range(time_start, time_end, freq='M'):
                    for column in matched_monthly_data.columns.to_list()[7:]:
                        if str(time_sequence)[: 4] == column[3: 7] and str(time_sequence)[5: 7] == column[-2:]:
                            sum_value = sum_value + (matched_monthly_data.loc[line_matched_data, column])
                            months_passed = (time_end - time_start).days // 30
                            mean_value = sum_value / months_passed
                            original_data.loc[line_original_data, field] = mean_value
    return original_data


path = r"C:\Users\DELL\Desktop"
original_excel = 'Data_Weathering_HWSD_pre_water.xlsx'
original_data = pd.read_excel(os.path.join(path, original_excel), sheet_name=0)

precipitation_excel = 'swc1980-2020.xlsx'
precipitation_data = pd.read_excel(os.path.join(path, precipitation_excel), sheet_name=0)
original_data = match_value_with_time_sequence_mean(original_data, precipitation_data, 'Water content')
original_data.to_excel(os.path.join(path, original_excel), index=False)
print('done')
