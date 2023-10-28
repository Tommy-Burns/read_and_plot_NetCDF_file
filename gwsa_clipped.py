import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import rasterio
import geopandas as gpd


def plot_gwsa_data_with_overlay(netcdf_file, dat_file):
    try:
        # Open the NetCDF file
        # Open the netCDF file
        ds = xr.open_dataset(netcdf_file)

        # Read the shapefile into a GeoDataFrame
        gdf = gpd.read_file('Basins/aoi.shp')

        # Create a mask based on the shapefile's geometries
        mask = rasterio.features.geometry_mask(gdf.geometry, out_shape=ds['var'].shape,
                                               transform=ds['var'].geo_transform(), invert=True)

        # Apply the mask to the data in the netCDF file
        dataset = ds['var'].where(mask)

        # Read the 'GWSA' variable data for the specified time index
        gwsa_data = dataset.variables['GWSA'][:]
        median_gwsa_data = np.median(gwsa_data, axis=0)

        # Load data from the .dat file
        with open(dat_file, 'r') as f:
            overlay_data = np.loadtxt(f)

        # Extract x and y values from the overlay data
        overlay_x = overlay_data[:, 0]
        overlay_y = overlay_data[:, 1]

        # Get the latitude and longitude corresponding to the overlay_data
        latitude = dataset.variables['latitude'][:]
        longitude = dataset.variables['longitude'][:]

        # Create a mask to filter out data points outside the boundary
        mask = (longitude >= np.min(overlay_x)) & (longitude <= np.max(overlay_x)) & \
               (latitude >= np.min(overlay_y)) & (latitude <= np.max(overlay_y))

        # Apply the mask to the median_gwsa_data
        median_gwsa_data[~mask] = np.nan

        # Create a 2D plot for 'GWSA' data
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(overlay_x, overlay_y, median_gwsa_data, shading='auto')
        plt.colorbar(label='Groundwater Storage Anomalies (mm)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Groundwater Storage Anomalies at Median')
        # plt.grid(True)

        # Overlay the .dat file data on the plot
        plt.plot(overlay_x, overlay_y, color='red', label='Volta Basin')

        # Add a legend to the plot
        plt.legend()

        # Show the plot
        plt.show()

        # Close the dataset after reading
        dataset.close()

    except Exception as e:
        print(f"Error while reading NetCDF file or overlay data: {e}")


# Usage example:
if __name__ == "__main__":
    netcdf_file_path = "grace_era.nc"
    dat_file_path = "Basins/VoltaBasin.dat"
    plot_gwsa_data_with_overlay(netcdf_file_path, dat_file_path)
