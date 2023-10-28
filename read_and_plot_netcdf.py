import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np


def plot_gwsa_data_with_overlay(netcdf_file, dat_file, time_index=0):
    try:
        # Open the NetCDF file
        dataset = nc.Dataset(netcdf_file)

        # Read the 'GWSA' variable data for the specified time index
        gwsa_data = dataset.variables['GWSA'][time_index, :, :]

        # Get latitude and longitude values
        latitude = dataset.variables['latitude'][:]
        longitude = dataset.variables['longitude'][:]

        # Create a 2D plot for 'GWSA' data
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(longitude, latitude, gwsa_data, shading='auto')
        plt.colorbar(label='Groundwater Storage Anomalies (mm)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Groundwater Storage Anomalies at Time Index {time_index}')
        # plt.grid(True)

        # Close the dataset after reading
        dataset.close()

        # Load data from the .dat file
        with open(dat_file, 'r') as f:
            overlay_data = np.loadtxt(f)

        # Extract x and y values from the overlay data
        overlay_x = overlay_data[:, 0]
        overlay_y = overlay_data[:, 1]

        # Overlay the .dat file data on the plot
        plt.plot(overlay_x, overlay_y, color='red', label='Volta Basin')

        # Add a legend to the plot
        plt.legend()

        # Show the plot
        plt.show()

    except Exception as e:
        print(f"Error while reading NetCDF file or overlay data: {e}")


# Usage example:
if __name__ == "__main__":
    netcdf_file_path = "grace_era.nc"
    overlay_dat_file_path = "Basins/VoltaBasin.dat"
    plot_gwsa_data_with_overlay(netcdf_file_path, overlay_dat_file_path, time_index=0)
