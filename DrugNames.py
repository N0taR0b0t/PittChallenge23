#!/opt/homebrew/bin/python3

import csv

def extract_drug_info(search_term):
    # Ensure the search term is case-insensitive by converting it to lowercase
    search_term = search_term.lower()

    # Set to ensure unique combinations of the desired fields
    unique_results = set()

    # Open the CSV file
    with open('drugnames.csv', mode='r') as file:
        reader = csv.reader(file)

        # For each row in the CSV...
        for row in reader:
            # Extract the desired fields
            full_name = row[3]
            full_generic_name = row[5]
            brand_name = row[6]
            display_name = row[7]
            psn = row[16]

            # Convert brand name to lowercase and check if it contains the search term
            if search_term in brand_name.lower():
                unique_results.add((full_name, full_generic_name, brand_name, display_name, psn))

    return list(unique_results)


def print_results(results):
    for result in results:
        print(f"{result[0]},{result[1]},{result[2]},{result[3]},{result[4]}")

# Test the function
results = extract_drug_info("ZOFRAN")
print_results(results)
