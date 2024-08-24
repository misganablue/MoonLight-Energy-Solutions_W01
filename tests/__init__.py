def check_missing_values(data, location):
    # Get the count of missing values for each column
    missing_values = data.isnull().sum()
    missing_summary = missing_values[missing_values > 0]  # Show only columns with missing values
    return missing_summary

