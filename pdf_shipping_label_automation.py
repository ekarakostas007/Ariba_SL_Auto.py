import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import re

# Developed by Eva Karakostas using Python.

# -----------------------------
# CONFIGURATION
# -----------------------------

BASE_FOLDER = r"S:\Sales\Customer\TOYOTA\SHIPPING\Ariba Shipping Labels"

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def get_most_recent_folder(base_folder):
    """
    Finds the folder with the most recent year in the name.
    Assumes folder names are like: 'Ariba Shipping Labels (YYYY)'
    """
    folders = [f for f in Path(base_folder).iterdir() if f.is_dir()]
    latest_year = None
    latest_folder = None

    year_pattern = r"\((\d{4})\)"

    for folder in folders:
        match = re.search(year_pattern, folder.name)
        if match:
            year = int(match.group(1))
            if (latest_year is None) or (year > latest_year):
                latest_year = year
                latest_folder = folder

    return latest_folder

# -----------------------------
# MAIN SCRIPT
# -----------------------------

def main():
    most_recent_folder = get_most_recent_folder(BASE_FOLDER)

    if not most_recent_folder:
        print("No valid year folder found.")
        return

    print(f"Processing PDFs inside: {most_recent_folder}")

    # Search ALL subfolders recursively
    pdf_files = list(most_recent_folder.rglob("*.pdf")) + \
                list(most_recent_folder.rglob("*.PDF"))

    if not pdf_files:
        print("No PDF files found in this folder or its subfolders.")
        return

    for pdf_file in pdf_files:
        try:
            reader = PdfReader(str(pdf_file), strict=False)

            # Skip files that already have 1 page
            if len(reader.pages) <= 1:
                continue

            writer = PdfWriter()
            writer.add_page(reader.pages[0])  # Keep ONLY first page

            # Overwrite original file safely
            temp_path = pdf_file.with_suffix(".tmp")

            with open(temp_path, "wb") as temp_file:
                writer.write(temp_file)

            os.replace(temp_path, pdf_file)

            print(f"Trimmed {pdf_file.name} → 1 page")

        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")

    print("\nAll PDFs processed successfully.")

if __name__ == "__main__":
    main()

