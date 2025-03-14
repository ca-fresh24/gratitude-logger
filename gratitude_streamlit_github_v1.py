import streamlit as st
import csv
import os
from datetime import datetime

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_FILE = os.path.join(SCRIPT_DIR, "Category.txt")
SUBCATEGORY_FILE = os.path.join(SCRIPT_DIR, "sub-category.txt")
FILENAME = os.path.join(SCRIPT_DIR, "gratitude_list_streamlit_v6.csv")

def get_next_number(filename):
    """ Get the next entry number from the CSV file """
    if not os.path.exists(filename):
        return 1
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            rows = list(reader)
            if not rows:
                return 1
            return int(rows[-1][0]) + 1  # Get last number and increment
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return 1

def load_list_from_file(filename):
    """ Load categories or subcategories from a text file """
    if not os.path.exists(filename):
        st.error(f"File not found: {filename}")
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return []

def append_to_csv(filename, number, date, gratitude, category, sub_category):
    """ Save the gratitude entry to CSV """
    file_exists = os.path.exists(filename)
    try:
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Number", "Date", "Gratitude", "Category", "Sub-category"])  # Write header
            writer.writerow([number, date, gratitude, "; ".join(category), "; ".join(sub_category)])
    except Exception as e:
        st.error(f"Error writing to file: {e}")

# Load categories and subcategories
categories = load_list_from_file(CATEGORY_FILE)
subcategories = load_list_from_file(SUBCATEGORY_FILE)

# Streamlit UI
st.title("Gratitude Journal")

# Gratitude Input
gratitude_text = st.text_area("Enter today's gratitude:")

# Category Selection
st.subheader("Select Category")
selected_categories = st.multiselect("Choose categories:", categories)

# Sub-category Selection
st.subheader("Select Sub-category")
selected_subcategories = st.multiselect("Choose sub-categories:", subcategories)

# Add New Sub-category
new_subcategory = st.text_input("Add new sub-category")
if st.button("Add Sub-category"):
    if new_subcategory and new_subcategory not in subcategories:
        subcategories.append(new_subcategory)
        with open(SUBCATEGORY_FILE, "a", encoding="utf-8") as file:
            file.write(f"{new_subcategory}\n")
        st.success(f"New sub-category '{new_subcategory}' added!")

# Save Gratitude Entry
if st.button("Save Entry"):
    if gratitude_text and selected_categories and selected_subcategories:
        entry_number = get_next_number(FILENAME)
        current_date = datetime.now().strftime("%Y-%m-%d")
        append_to_csv(FILENAME, entry_number, current_date, gratitude_text, selected_categories, selected_subcategories)
        st.success(f"Gratitude #{entry_number} saved successfully!")
    else:
        st.error("Please enter gratitude and select at least one category and sub-category before saving.")
