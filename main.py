import subprocess

print("=" * 50)
print("AI YOUTUBE COMMENT ANALYZER")
print("=" * 50)

print("\nStep 1: Fetching Comments...")
subprocess.run(["python", "src/fetch_comments.py"])

print("\nStep 2: Cleaning Data...")
subprocess.run(["python", "src/data_cleaning.py"])

print("\nStep 3: Performing EDA...")
subprocess.run(["python", "src/eda.py"])

print("\nProject Completed Successfully!")