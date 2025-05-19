import os
import requests
import csv

# Function to call the API and extract relevant data for the run
def get_run_data(filename):
    url = f"https://www.speedrun.com/api/v1/runs/{filename}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching data for {filename}: {response.status_code}")
        return None

    data = response.json().get("data", {})

    # Extract relevant fields
    run_time = data.get("times", {}).get("primary", "N/A")
    run_date = data.get("date", "N/A")
    user_uri = data.get("players", [{}])[0].get("uri", "N/A")

    # Get the user information from their API URL
    user_data = get_user_data(user_uri)
    user_name = user_data.get("names", {}).get("international", "N/A") if user_data else "N/A"

    return {
        'filename': filename + ".mp4",
        'time': run_time,
        'run_date': run_date,
        'user': user_name
    }

# Function to fetch user data from the user API
def get_user_data(user_uri):
    response = requests.get(user_uri)

    if response.status_code != 200:
        print(f"Error fetching user data: {response.status_code}")
        return None

    return response.json().get("data", {})

# Directory where your MP4 files are located
directory = "src-runs"

# CSV output file
csv_file = "speedrun_data.csv"

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["filename", "time", "run_date", "user"])
    writer.writeheader()

    # Loop through the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            # Remove ".mp4" to get the run ID
            run_id = filename[:-4]

            # Get run data from the API
            run_data = get_run_data(run_id)

            if run_data:
                # Write to CSV
                writer.writerow(run_data)

print(f"Data has been written to {csv_file}")

