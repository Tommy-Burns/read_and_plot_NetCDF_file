import geopandas as gpd
import rasterio
from rasterio.mask import mask
import matplotlib.pyplot as plt


def clip_netcdf_with_shapefile(netcdf_path, shapefile_path, output_path, variable_name):
    # Read the shapefile using geopandas
    gdf = gpd.read_file(shapefile_path)

    # Open the NetCDF file using rasterio
    with rasterio.open(netcdf_path) as src:
        # Perform spatial subsetting using rasterio's mask function
        out_image, out_transform = mask(src, shapes=gdf.geometry, crop=True)

        # Get the metadata to create the clipped dataset
        out_meta = src.meta.copy()
        out_meta.update({"height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})

    # Save the subsetted NetCDF data using rasterio
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(out_image)

    print("Clipping complete. Output saved to:", output_path)


# Example usage:
netcdf_file_path = "grace_era.nc"
shapefile_path = "Basins/aoi.shp"
output_file_path = "Clipped/grace_clipped.nc"
variable_to_clip = "grace_era.nc"  # Replace with the actual variable name to clip

clip_netcdf_with_shapefile(netcdf_file_path, shapefile_path, output_file_path, variable_to_clip)

# Now let's plot the clipped NetCDF data using matplotlib
with rasterio.open(output_file_path) as src:
    data = src.read(1)  # Read the first band of the clipped NetCDF data

plt.imshow(data, cmap="jet")
plt.colorbar()
plt.title("Clipped NetCDF Data")
plt.show()
