import os
import pandas as pd

# Load Excel file
excel_path = "/home/piyushprasoon/Downloads/Eximietas Masterlist of Documents V1.1.xlsx"
df = pd.read_excel(excel_path)

def find_file_path(base_dir, search_terms):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            for term in search_terms:
                if isinstance(term, str) and term.lower() in file.lower():
                    return os.path.join(root, file)
    return "Not Found"

def extract_paths(main_directory):
    file_paths = []
    for _, row in df.iterrows():
        desc = str(row.get("Document Description", "")).strip()
        doc_no = str(row.get("Document No.", "")).strip()
        search_terms = [desc, doc_no]
        path = find_file_path(main_directory, search_terms)
        file_paths.append(path)
    df["File Path"] = file_paths
    return df

# Set your main directory path (change as needed)
main_directory = "//home/piyushprasoon/Downloads/drive-download/NEW_Docs"  # 👈 Update this path

# Run extraction
result_df = extract_paths(main_directory)

# Save result
output_file = "/home/piyushprasoon/Downloads/Document_Paths_Output.xlsx"
result_df.to_excel(output_file, index=False)

print(f"✅ File paths saved to: {output_file}")
