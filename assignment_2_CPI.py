# Q1 and 2: Lines 4-34
import pandas as pd

# Initialize list with jurisdictions and empty list to collect dataframes
jurisdiction_list = ['AB', 'BC', 'Canada', 'MB', 'NB', 'NL', 'NS', 'ON', 'PEI', 'QC', 'SK']
# df_list = []

data = []

# Initialize loop to open the 11 different csv files and add them to the list
for jurisdiction in jurisdiction_list:
    file = jurisdiction + '.CPI.1810000401.csv'    
    df = pd.read_csv(file)

    # Merge the dataframe to have a single column for the month and CPI
    id_vars = ['Item']
    months = [col for col in df.columns if col not in id_vars]

    for index, row in df.iterrows():
        for month in months:
            data.append({'Item': row['Item'], 'Month': month, 'Jurisdiction': jurisdiction, 'CPI': row[month]})

cpi_data = pd.DataFrame(data)

# Define the correct order for the months
month_order = ['24-Jan', '24-Feb', '24-Mar', '24-Apr', '24-May', '24-Jun', '24-Jul', '24-Aug', '24-Sep', '24-Oct', '24-Nov', '24-Dec']
cpi_data['Month'] = pd.Categorical(cpi_data['Month'], categories=month_order, ordered=True)

# Sort the dataframe by Month first and then by Jurisdiction
cpi_data = cpi_data.sort_values(by=['Month', 'Jurisdiction'])

# Print the first 12 rows of data
print(cpi_data.head(13).to_string(index=False))
print("\n")

# Q3: Lines 38-51

# Calculate the month-to-month percentage change
cpi_data['pct_change'] = cpi_data.groupby(['Jurisdiction', 'Item'])['CPI'].pct_change() * 100

# Filter for the required items
items_of_interest = ['Food', 'Shelter', 'All-items excluding food and energy']
df_filtered = cpi_data[cpi_data['Item'].isin(items_of_interest)]

# Calculate the average month-to-month change for each jurisdiction and item
avg_monthly_change = df_filtered.groupby(['Jurisdiction', 'Item'])['pct_change'].mean().reset_index()

# Report the numbers as a percent up to one decimal place
avg_monthly_change['pct_change'] = avg_monthly_change['pct_change'].round(1)
print(avg_monthly_change)
print("\n")

# Q4: Lines 49-64

# Find the province with the highest average change for each item
highest_avg_change = avg_monthly_change.loc[avg_monthly_change.groupby('Item')['pct_change'].idxmax()]

# Print the results with text
for item in items_of_interest:
    highest_change = highest_avg_change[highest_avg_change['Item'] == item]

    jurisdiction = highest_change['Jurisdiction'].values[0]
    pct_change = highest_change['pct_change'].values[0]
    print(f"The province with the highest average change in {item} is {jurisdiction} with an average change of {pct_change}%.")

# Q5 68-82 

# Filter for the 'Services' item
df_services = cpi_data[cpi_data['Item'] == 'Services']

# Pivot the data so that each (Jurisdiction) pair is a row and months are columns
df_services_pivot = df_services.pivot_table(index='Jurisdiction', columns='Month', values='CPI')

# Compute the annual change using the January and December values
df_services_pivot['YOY Change'] = (df_services_pivot['24-Dec'] - df_services_pivot['24-Jan']) / df_services_pivot['24-Jan'] * 100

# Report the numbers as a percent up to one decimal place
df_services_pivot['YOY Change'] = df_services_pivot['YOY Change'].round(1)

# Print the annual change for services
print(df_services_pivot[['YOY Change']])
print("\n")

# Q6 86-90

# Print the jurisdiction with the highest YOY change
highest_yoy_change_jurisdiction = df_services_pivot['YOY Change'].idxmax()
highest_yoy_change_value = df_services_pivot['YOY Change'].max()
print(f"The jurisdiction with the highest YOY change is {highest_yoy_change_jurisdiction} with a change of {highest_yoy_change_value}%.")
print("\n")

