import csv
import html

def search_substance(query, resultCount=0):
    """
    Search for a substance within the "FoodSubstances.csv" file.

    Parameters:
    - query: str - Substance to search for
    - resultCount: int - Number of results to display. If 0, show all.

    Returns:
    - None, but will print the matching substances
    """
    filename = "FoodSubstances.csv"
    results = []

    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header
        for row in reader:
            # Check if the row has at least 2 elements
            if len(row) > 1:
                substance = html.unescape(row[1].strip())
                if query.lower() in substance.lower():
                    results.append(substance)
            else:
                print(f"Skipping incomplete row: {row}")
    
    if resultCount > 0:
        results = results[:resultCount]
    
    for r in results:
        print(r)

search_substance("propan", 1) #Query STR and lines INT
