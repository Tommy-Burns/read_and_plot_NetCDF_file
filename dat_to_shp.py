import pandas as pd
import geopandas as gpd

# Step 1: Read the .dat file using Pandas with appropriate column names
input_dat_file = 'Basins/VoltaBasin.dat'
column_names = ['Longitude', 'Latitude', 'Value']  # Replace these with actual column names
df = pd.read_csv(input_dat_file, delimiter=' ', names=column_names)

# Step 2: Convert the DataFrame to a GeoDataFrame
# Since the data has no headers, you'll need to specify the column names directly while creating the GeoDataFrame.
geometry = gpd.points_from_xy(df['Longitude'], df['Latitude'])
crs = 'EPSG:4326'
gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

# Step 3: Save the GeoDataFrame as a shapefile
output_shapefile = './Basins/aoi.shp'
gdf.to_file(output_shapefile, driver='ESRI Shapefile')
