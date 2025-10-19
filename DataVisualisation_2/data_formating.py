import pandas as pd

# --- Step 1: Load your data ---
df = pd.read_csv("DataVisualisation_2/state-visited-by-tourists.csv")

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# --- Step 2: Convert from wide - long format ---
df_long = df.melt(
    id_vars=["Year", "State"],
    var_name="Country",
    value_name="Percentage"
)

# --- Step 3: Split combined states ---
# Define combined states and how to split them
split_map = {
    "KUALA LUMPUR / SELANGOR": ["KUALA LUMPUR", "SELANGOR"],
    "KEDAH / PERLIS": ["KEDAH", "PERLIS"]
}

# Create a list to collect all new rows
new_rows = []

for combined, parts in split_map.items():
    # Filter matching rows (ignore case and spacing)
    mask = df_long["State"].str.upper().str.replace(" ", "") == combined.replace(" ", "").upper()
    subset = df_long[mask].copy()
    
    # Divide percentages equally among new states
    subset["Percentage"] = subset["Percentage"] / len(parts)
    
    # Create duplicates for each new state
    for state_name in parts:
        temp = subset.copy()
        temp["State"] = state_name
        new_rows.append(temp)

# Combine all new rows
if new_rows:
    new_rows_df = pd.concat(new_rows, ignore_index=True)
else:
    new_rows_df = pd.DataFrame(columns=df_long.columns)

# --- Step 4: Remove old combined rows ---
for combined in split_map.keys():
    df_long = df_long[~(df_long["State"].str.upper().str.replace(" ", "") == combined.replace(" ", "").upper())]

# --- Step 5: Add new rows ---
df_long = pd.concat([df_long, new_rows_df], ignore_index=True)

# --- Step 6: Save output ---
df_long["State"] = df_long["State"].str.upper()
df_long.to_csv("tourism_long_split.csv", index=False)

print(" Done! Saved as 'tourism_long_split.csv'")
print(df_long[df_long["State"].isin(["KUALA LUMPUR", "SELANGOR", "KEDAH", "PERLIS"])].head(8))
