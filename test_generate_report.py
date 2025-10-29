import os
from generate_report import create_sample_csv, read_csv, add_entry_to_csv, summarize_data, sort_departments

# --- Constants ---
TEST_CSV = "data/test_input.csv"

# --- Step 1: Create test CSV ---
create_sample_csv(TEST_CSV)

# --- Step 2: Test reading CSV ---
data = read_csv(TEST_CSV)
assert len(data) >= 5, "Error: Sample CSV does not have enough rows"
print("✅ Test 1 passed: CSV read correctly.")

# --- Step 3: Test adding a new record ---
add_entry_to_csv(TEST_CSV, "TestUser", "Testing", 999)
data = read_csv(TEST_CSV)
assert any(row["name"] == "TestUser" for row in data), "Error: New record was not added"
print("✅ Test 2 passed: Record added successfully.")

# --- Step 4: Test summary generation ---
summary = summarize_data(data)
sorted_summary = sort_departments(summary)
assert "Testing" in summary, "Error: Department 'Testing' not found in summary"
print("✅ Test 3 passed: Summary generated successfully.")

# --- Step 5: Cleanup ---
os.remove(TEST_CSV)
print("🧹 Test completed and test CSV removed.")
