# Created by Muhammad Suleiman Qureshi
#Possible Parameter to change
#Whether or not to show EDI in the Schedule
drop_EDI = True





import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
import os
from datetime import datetime, timedelta

def parse_time(time_str):
    """Convert 12-hour time format (e.g., '9:40a' or '11:30p') to 24-hour time."""
    time_str = time_str.strip().lower().replace("a", "AM").replace("p", "PM")
    return datetime.strptime(time_str, "%I:%M%p").time()

def expand_days(days_str):
    """Expand multi-day entries (e.g., 'TTh') into a list of individual days."""
    day_mapping = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4, "S": 5, "Su": 6}
    days = []
    i = 0
    while i < len(days_str):
        if i + 1 < len(days_str) and days_str[i:i+2] in day_mapping:
            days.append(day_mapping[days_str[i:i+2]])
            i += 2
        else:
            days.append(day_mapping[days_str[i]])
            i += 1
    return days

def plot_schedule(file_path):
    # Load CSV file
    df = pd.read_csv(file_path)
    
    # Convert time columns to datetime.time
    df["Published Start"] = df["Published Start"].astype(str).apply(parse_time)
    df["Published End"] = df["Published End"].astype(str).apply(parse_time)
    
    # Plot settings
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_yticks(range(7))
    ax.set_yticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))  # Set major locator for 15-minute intervals
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%I:%M %p"))
    plt.xticks(rotation=90)
    # Define the start time at 8:15 AM
    start_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=8, minutes=15)
    
    # Define the end time at 6:45 PM
    end_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=18, minutes=45)
    
    # Set the xlim (starting point at 8:15 AM and ending at 6:45 PM)
    ax.set_xlim(start_time, end_time)
    # Plot each course at its specific time on multiple days
    ax.grid(True, which='both', axis='x', linestyle='--', color='gray', linewidth=0.5)

    for _, row in df.iterrows():
        start_time = datetime.combine(datetime.today(), row["Published Start"])
        end_time = datetime.combine(datetime.today(), row["Published End"])
        days = expand_days(row["Day Of Week"])
        for day in days:
            ax.plot([start_time, end_time], [day]*2, marker='o', label=row["Title"])
    
    ax.set_xlabel("Time")
    ax.set_ylabel("Day of Week")
    ax.set_title("Schedule of " + subfolder_name+ (" No EDI" if (drop_EDI) else " With EDI"))
    # plt.legend()
    plt.savefig("Schedule of " + subfolder_name + ".png", dpi=300)
    # plt.show()
    plt.clf()

def clean_schedule(file_path):
    # Load CSV file
    df = pd.read_csv(file_path)
    df = df.drop_duplicates(subset=["Type","Title"], keep="first")
    # Keep only the relevant columns
    if (drop_EDI):
        df = df[df["Title"] != "Engineering, Design, & Innov."]
    df = df[["Title", "Day Of Week", "Published Start", "Published End"]]
    
    # Remove duplicate course entries, keeping only the first occurrence
    
    return df
    # # Save the cleaned file
    # df.to_csv(output_file, index=False)
    # print(f"Cleaned schedule saved to {output_file}")


def process_csv_files(folder_path):
    # List all files in the given folder
    files = os.listdir(folder_path)
    all_cleaned_data = pd.DataFrame()
    # Iterate through each file in the folder
    for file in files:
        # Check if the file is a CSV file
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            try:
                # Read the CSV file
                # df = pd.read_csv(file_path)
                cleaned_data = clean_schedule(file_path)
                
                # Append the cleaned data to the final DataFrame
                all_cleaned_data = pd.concat([all_cleaned_data, cleaned_data], ignore_index=True)
                print(f"Processed and cleaned {file}")
                # Perform any processing here. For now, let's just print the first few rows.
                # print(f"Processing file: {file}")
                # print(df.head())  # You can replace this with any processing you need.
            except Exception as e:
                print(f"Error reading {file}: {e}")
    all_cleaned_data.to_csv(final_output_file, index=False)
    plot_schedule(final_output_file)
# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the subfolder name inside the script directory
# Combine the script directory with the subfolder name
# folder_path = os.path.join(script_directory, subfolder_name)

def get_folders_in_current_directory():
    # Get the path of the current directory where the script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # List all items in the directory
    items = os.listdir(current_directory)
    
    # Filter out the folders (directories) from the list
    folders = [item for item in items if os.path.isdir(os.path.join(current_directory, item))]
    
    return folders

# Call the function and print the folder names
folders = get_folders_in_current_directory()

# print("Folders:", folders)

for subfolder_name in folders:
    final_output_file = subfolder_name+"/final_cleaned_schedule.csv"
    process_csv_files(subfolder_name)
