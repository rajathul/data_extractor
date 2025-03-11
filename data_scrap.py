import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.barchart.com/futures/quotes/IMG25/historical-prices?orderBy=contractExpirationDate&orderDir=asc&page=4"

# Send a GET request to the website
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing historical prices
table = soup.find('table', {'class': 'bc-table'})

# Extract table headers and rows
headers = [header.text.strip() for header in table.find_all('th')]
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    cells = row.find_all('td')
    rows.append([cell.text.strip() for cell in cells])

# Create a DataFrame
df = pd.DataFrame(rows, columns=headers)

# Extract the first 4 columns
first_four_columns = df.iloc[:, :4]

# Save to CSV or print
first_four_columns.to_csv('first_four_columns.csv', index=False)
print(first_four_columns)