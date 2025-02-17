# README

### Author: Daksh Gargi

This code reads an Excel file containing a mess menu and converts it into a JSON file. It may look a bit long, but it’s actually broken down into manageable steps. Below is an overview of what each part does.

---

## 1) Reading the Excel File  
• The code uses the pandas library to load an Excel file named "mess_menu.xlsx."  
• It does not assume any fancy rows or formatting in the file, so it’s important that your Excel file is laid out neatly (the first row has day labels, the second row has dates, and the rest contains meal information).

Example:
```python
df = pd.read_excel("mess_menu.xlsx", header=None)
```
This reads the entire spreadsheet into a structure called a DataFrame.

---

## 2) Getting Day Labels  
• The first row (in the code, "df.iloc[0]") is picked out.  
• Each value in it is turned into uppercase and added to a list called "day_labels."  
• We do this so later on we know what "words" we should not treat as part of the food items (like "SATURDAY" or "SUNDAY").

Example:
```python
first_row = df.iloc[0].tolist()
for item in first_row:
    if pd.notna(item):
        item_str = str(item).strip().upper()
        day_labels.append(item_str)
```
This way, any time we see these labels later, we know they’re not actual menu items.

---

## 3) Converting Dates  
• The second row (which is "df.iloc[1]") is where the actual dates are expected.  
• We loop through these potential dates, change them into a nice string format (like "1-Feb-25"), and store them in "dates_list."  
• A small helper function called "format_excel_date" detects whether the given value is a date or something else. If it’s recognized as a date, it formats it differently for Windows vs. other systems.

Example:
```python
second_row = df.iloc[1].tolist()
for val in second_row:
    if pd.isna(val):
        dates_list.append(None)
    else:
        date_text = format_excel_date(val)
        dates_list.append(date_text)
```
This means each column in the sheet is tied to one of these dates.

---

## 4) Setting Up a Dictionary to Store Meals  
• After we have a list of all the dates, we create a dictionary called "dates_data."  
• Each date in "dates_list" becomes a key in this dictionary. For each date, we also create three empty lists: "BREAKFAST," "LUNCH," and "DINNER."

Example:
```python
dates_data[d] = {
    "BREAKFAST": [],
    "LUNCH": [],
    "DINNER": []
}
```
So later, if we find out "Pasta" is a "DINNER" item for "4-Feb-25," we can just append "Pasta" to "dates_data["4-Feb-25"]["DINNER"]."

---

## 5) Identifying Which Meal We’re In  
• The code loops from the third row onward (because row zero is day labels, row one is dates).  
• Inside each row, we look for the words "BREAKFAST," "LUNCH," or "DINNER." If we find one, that means from this point on, we’re listing items for that meal until we see the next meal name.

Example:
```python
meal_names = {"BREAKFAST", "LUNCH", "DINNER"}
current_meal = None  # This holds which meal we’re currently reading.

# For each row, see if there's a cell that matches one of our meal names
for cell in row_values:
    if isinstance(cell, str):
        text_cell = cell.strip().upper()
        if text_cell in meal_names:
            found_meal = text_cell
            break
```
If found, "current_meal" is updated accordingly.

---

## 6) Assigning Menu Items to the Right Meal and Date  
• Once we know the current meal ("current_meal"), other cells in the row belong to the columns (which are dates).  
• We figure out which date each column belongs to by using "dates_list."  
• Then we skip anything that might be a day label (like "SATURDAY") or contains asterisks.  
• Anything left is considered a valid menu item, which gets appended to the correct part of the dictionary, such as "dates_data[some_date][current_meal]."

Example:
```python
for col_index, cell_value in enumerate(row_values):
    date_key = dates_list[col_index]
    # If the cell is not empty or an asterisk or a day label, we store it
    dates_data[date_key][current_meal].append(cell_str)
```
This approach ensures each meal has the correct list of items for each date.

---

## 7) Saving Everything as JSON  
• At the end, "dates_data" is written to a file named "mess_menu.json" in a human-readable format (JSON).  
• The code uses "json.dump(..., indent=4)" to make the JSON file pretty.

Example:
```python
with open("mess_menu.json", "w", encoding="utf-8") as file_out:
    json.dump(dates_data, file_out, indent=4, ensure_ascii=False)
```
This creates the final output in a standard JSON structure that can be easily read or used by other scripts.

---

That’s the entire process. If you ever need to tweak or troubleshoot (like changing how you skip certain rows or adjusting the date format), you can modify the relevant part of the code, but the approach stays the same.
