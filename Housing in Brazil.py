# Import Matplotlib, pandas, and plotly
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
#Import the CSV file data/brasil-real-estate-1.csv into the DataFrame df1.
df1 = pd.read_csv('data/brasil-real-estate-1.csv')
# Identifying issues in the data that needs cleaning
df1.head()
df1.info()
print(df1)
# Drop all rows with NaN values from the DataFrame df1
print('count of null values in DataFrame:')
print(df1.isna().sum())

print('DataFrame after dropping the rows having missing values:')
df1.dropna(inplace=True)
df1.info()
# Use the "lat-lon" column to create two separate columns in df1: "lat" and "lon" 
df1[['lat','lon']] = df1["lat-lon"].str.split(",",expand=True)
print(df1.head(3))
#converting the above new column from object to float data type
df1[['lat','lon']] = df1[['lat','lon']].astype(float)
print(df1.info())
# Extracting "state" column from the "place_with_parent_names" column  
df1["state"]= df1["place_with_parent_names"].str.split( '|', expand=True)[2]
df1.info()
df1["state"]
#Transform the "price_usd" column to from object floating-point numbers
df1["price_usd"] = (df1["price_usd"]
                    .str.replace("$", "", regex = False)
                    .str.replace(",", "")
                    .astype(float)
            )
#Drop the "lat-lon" and "place_with_parent_names" columns from df1
df1.drop(columns = ["place_with_parent_names", "lat-lon"], inplace=True)
df1
#Import the CSV file brasil-real-estate-2.csv into the DataFrame df2.
df2 = pd.read_csv('data/brasil-real-estate-2.csv')
df2
# Identifying issues in the data that needs cleaning
df1.head()
df2.head()
df2.info()
df2.isnull().sum()
# Use the "price_brl" column to create a new column named "price_usd". 
# (Keep in mind that, when this data was collected in 2015 and 2016, a US dollar cost 3.19 Brazilian reals.)
df2["price_usd"] =df2["price_brl"] /3.19
# Drop the "price_brl" column from df2, as well as any rows that have NaN values.
df2.drop("price_brl", axis=1, inplace=True)
df2.drop("column_name", axis=1, inplace=True)
# Concatenate df1 and df2 to create a new DataFrame named df.
df = pd.concat([df1, df2])
print("df shape:", df.shape)

#EXPLORATORY DATA ANALYSIS
# Create a scatter_mapbox showing the location of the properties in df
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

fig.update_layout(mapbox_style="open-street-map")

fig.show()
# Obtain the summary statistics for the "area_m2" and "price_usd" columns.
summary_stats = df[["area_m2", "price_usd"]].describe()
summary_stats
# Build histogram of "price_usd" with x-axis label as "Price [USD]" and y-axis label as "Frequency" 
# and the plot has the title "Distribution of Home Prices". Use Matplotlib (plt)
plt.hist(df["price_usd"])
plt.xlabel("Price [USD]")
plt.xlabel("Frequency")
plt.title("Distribution of Home Prices")

# Build box plot
plt.boxplot(df["area_m2"], vert=False)
plt.xlabel("Area [sq meters]")
plt.title("Distribution of Home Sizes")

# Create a horizontal boxplot of "area_m2"ith x-axis label as "Area [sq meters]" and plot has the title "Distribution of Home Sizes" 
plt.boxplot(df["area_m2"], vert=False)
plt.xlabel("Area [sq meters]")
plt.title("Distribution of Home Sizes")
# Use the groupby method to create a Series named mean_price_by_region that shows the mean home price in each region in Brazil
mean_price_by_region = df.groupby("region")["price_usd"].mean().sort_values()
mean_price_by_region
# Use mean_price_by_region to create a bar chart. Make sure you label the x-axis as "Region" 
# and the y-axis as "Mean Price [USD]", and give the chart the title "Mean Home Price by Region"

mean_price_by_region.plot(
    kind="bar"
);
plt.title("Mean Home Price by Region")

# Create a DataFrame df_south that contains all the homes from df that are in the "South" region.
df_south = df.loc[df["region"] == "South"]

# Use the value_counts method to create a Series homes_by_state that contains the number of properties in each state in df_south
df_south
homes_by_state = df_south.state.value_counts()
homes_by_state

# Subset data
df_south_rgs = df_south.loc[df_south["state"] == "Rio Grande do Sul"]
df_south_rgs

#Create a scatter plot showing price vs. area for the state in df_south that has the largest number of properties. 
# label the x-axis "Area [sq meters]" and the y-axis "Price [USD]"
# use the title "<name of state>: Price vs. Area". Use Matplotlib (plt).
df_south_rgs = df_south.loc[df_south["state"] == "Rio Grande do Sul"]
df_south_rgs
plt.scatter(x=df_south_rgs["area_m2"], y=df_south_rgs["price_usd"])
plt.xlabel("Area [sq meters]")
plt.ylabel("Price [USD]")
plt.title("Rio Grande do Sul: Price vs. Area")