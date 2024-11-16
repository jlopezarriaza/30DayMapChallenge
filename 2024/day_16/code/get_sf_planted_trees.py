# Local imports
from utils import (
    get_sf_trees,
    add_zipcodes_to_df,
    create_choropleth_map,
)

# Third-party imports
import geopandas as gpd


if __name__ == "__main__":
    # Get the data
    trees_df = get_sf_trees()

    # Basic info about the dataset
    print(f"Number of trees: {len(trees_df)}")
    print("\nColumns in dataset:")
    print(trees_df.columns.tolist())

    # Save raw data to CSV
    trees_df.to_csv("sf_trees.csv", index=False)

    # Add zipcode data if needed
    if "zipcode" not in trees_df.columns:
        trees_df = add_zipcodes_to_df(trees_df)
        
    unique_zipcode_geometries = (
        trees_df[["zipcode", "zipcode_geom"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    
    trees_per_zipcode = (
        trees_df.groupby("zipcode")
        .size()
        .reset_index(name="count")
    )
    
    zipcode_tree_counts = trees_per_zipcode.merge(
        unique_zipcode_geometries, 
        on="zipcode", 
        how="left"
    )
    
    zipcode_tree_geodf = gpd.GeoDataFrame(
        zipcode_tree_counts, 
        geometry="zipcode_geom", 
        crs="EPSG:4326"
    )

    # Create and save the map
    choropleth_map = create_choropleth_map(zipcode_tree_geodf)
    choropleth_map.save("sf_trees_choropleth.html")
    print("\nMap saved as 'sf_trees_choropleth.html'")
