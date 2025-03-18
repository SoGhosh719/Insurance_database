import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file (update the filename if needed)
file_path = "Licensed-Or-Approved-Companies.csv"
df = pd.read_csv(file_path)

# Drop unnecessary columns
df = df[['Company Name', 'Type of Insurance']]

# Function to categorize companies based on the "Type of Insurance" column
def categorize_company(type_info):
    categories = {
        "Auto Insurance": "Auto",
        "Health Insurance": "Health",
        "Life Insurance": "Life",
        "Home Insurance": "Home",
        "Commercial Insurance": "Business, Commercial, Liability"
    }
    
    for category, keywords in categories.items():
        if any(keyword in str(type_info) for keyword in keywords.split(", ")):
            return category
    return "Other"

# Apply categorization
df["Category"] = df["Type of Insurance"].apply(categorize_company)

# Count companies per category
category_counts = df["Category"].value_counts()
print("\n🏢 Categorized Companies:\n")
print(category_counts)

# Save the categorized data to a new CSV file
output_file = "categorized_companies.csv"
df.to_csv(output_file, index=False)
print(f"\n✅ Categorized data saved to {output_file}")

# Generate and display a bar chart
plt.figure(figsize=(10,5))
category_counts.plot(kind='bar', color='skyblue')
plt.xlabel("Insurance Category")
plt.ylabel("Number of Companies")
plt.title("Number of Companies per Insurance Category")
plt.xticks(rotation=45)
plt.show()