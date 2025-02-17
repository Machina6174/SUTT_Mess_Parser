import pandas as pd
import json
import datetime
import platform

# This function tries to convert an Excel date cell to a string. We use different formats based on Windows or not.
def format_excel_date(dt):
    if not hasattr(dt, "strftime"):
        return str(dt).strip()
    else:
        if platform.system() == "Windows":
            return dt.strftime("%#d-%b-%y")
        else:
            return dt.strftime("%-d-%b-%y")

# Read the Excel file. Replace 'mess_menu.xlsx' with your real file path.
df = pd.read_excel("mess_menu.xlsx", header=None)

# Collect the day labels from the first row.
day_labels = []
first_row = df.iloc[0].tolist()
for item in first_row:
    if pd.notna(item):
        item_str = str(item).strip().upper()
        day_labels.append(item_str)

# Prepare a dictionary for the dates.
dates_data = {}

# Extract the second row (index=1) to figure out dates for each column.
dates_list = []
second_row = df.iloc[1].tolist()
for val in second_row:
    if pd.isna(val):
        dates_list.append(None)
    else:
        date_text = format_excel_date(val)
        dates_list.append(date_text)

# Initialize the dictionary with empty meal lists for each date.
for d in dates_list:
    if d is not None and d != "":
        dates_data[d] = {
            "BREAKFAST": [],
            "LUNCH": [],
            "DINNER": []
        }

# We look for three meal names.
meal_names = {"BREAKFAST", "LUNCH", "DINNER"}
current_meal = None

# Go through rows starting from index=2 to read meal items.
for row_index in range(2, df.shape[0]):
    row_values = df.iloc[row_index].tolist()

    found_meal = None
    for cell in row_values:
        if isinstance(cell, str):
            text_cell = cell.strip().upper()
            if text_cell in meal_names:
                found_meal = text_cell
                break

    # If a meal name is found, update current_meal.
    if found_meal in meal_names:
        current_meal = found_meal
        continue

    # If we have a current meal, assign items to the correct date column.
    if current_meal is not None:
        for col_index, cell_value in enumerate(row_values):
            if col_index >= len(dates_list):
                continue

            date_key = dates_list[col_index]
            if date_key not in dates_data:
                continue

            if pd.isna(cell_value):
                continue

            cell_str = str(cell_value).strip()

            # Skip lines containing asterisks or just a day label.
            if "*" in cell_str:
                continue
            if cell_str.upper() in day_labels:
                continue

            dates_data[date_key][current_meal].append(cell_str)

# Write the data to a JSON file.
with open("mess_menu.json", "w", encoding="utf-8") as file_out:
    json.dump(dates_data, file_out, indent=4, ensure_ascii=False)

print("Mess menu data has been processed and saved to mess_menu.json.")