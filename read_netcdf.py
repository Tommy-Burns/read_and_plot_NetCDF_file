import netCDF4 as nc


def read_netcdf_file(file_path):
    try:
        # Open the NetCDF file
        dataset = nc.Dataset(file_path)

        # Read data and metadata
        variables = dataset.variables
        dimensions = dataset.dimensions
        global_attributes = dataset.__dict__

        # You can access specific variables using their names
        # For example, if there's a variable called 'temperature':
        # temperature_data = dataset.variables['temperature'][:]

        # Print some basic information
        print("NetCDF file information:")
        print(f"Longitude: {dimensions}")
        print(f"Variables: {variables}")
        # print(f"Global Attributes: {global_attributes}")

        # Close the dataset after reading
        dataset.close()

    except Exception as e:
        print(f"Error while reading NetCDF file: {e}")


# Usage example:
if __name__ == "__main__":
    file_path = "grace_era.nc"
    read_netcdf_file(file_path)
