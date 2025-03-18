import pandas as pd

# Load the CSV file (update the filename if needed)
file_path = "Licensed-Or-Approved-Companies.csv"
df = pd.read_csv(file_path)

# Display basic info about the dataset
print("\n🔍 Dataset Overview:\n")
print(df.info())

# Display first few rows
print("\n📊 First 5 Rows:\n")
print(df.head())

# Function to categorize companies based on keywords
def categorize_company(name):
    categories = {
        "Auto Insurance": ["Auto", "Vehicle", "Car", "Motor"],
        "Health Insurance": ["Health", "Medical", "Care"],
        "Life Insurance": ["Life", "Annuity"],
        "Home Insurance": ["Home", "Property", "Casualty"],
        "Commercial Insurance": ["Business", "Commercial", "Liability"],
    }
    
    for category, keywords in categories.items():
        if any(keyword in name for keyword in keywords):
            return category
    return "Other"

# Apply categorization
df["Category"] = df["Company Name"].astype(str).apply(categorize_company)

# Display categorized data
print("\n🏢 Categorized Companies:\n")
print(df["Category"].value_counts())

# Save the categorized data to a new CSV file
output_file = "categorized_companies.csv"
df.to_csv(output_file, index=False)
print(f"\n✅ Categorized data saved to {output_file}")
