
# Define the directory where the CSV files are located
csv_directory = 'D:\data\Solar Radiation Measurement Data'

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

# Load each CSV file into a DataFrame
dataframes = {}
for file in csv_files:
    file_path = os.path.join(csv_directory, file)
    dataframes[file] = pd.read_csv(file_path)
    print(f"Loaded {file} with shape {dataframes[file].shape}")

# Display the first few rows of one DataFrame
df = dataframes[csv_files[0]]
df.head()

