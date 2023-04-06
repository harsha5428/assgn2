#Import necessary modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def file_modify(filename):
    """
    Reads a csv file, removes unnecessary columns, transposes the dataframe,
    saves the transposed dataframe as a new csv file, and returns both the original
    and transposed dataframes.

    Args:
    filename (str): Name of the csv file to be read.

    Returns:
    tuple: A tuple containing the original dataframe and the transposed dataframe.
    """
    # Read the csv file, skipping the first 3 rows
    data_read = pd.read_csv(filename, skiprows=3)

    # Create a copy of the original dataframe
    dataframe = data_read

    # Drop unnecessary columns from the copy of the dataframe
    dataframe1 = dataframe.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], axis=1)

    # Set the index of the copy of the dataframe to "Country Name"
    dataframe1 = dataframe1.set_index('Country Name')

    # Transpose the copy of the dataframe
    dataframe1 = dataframe1.transpose()

    # Save the transposed dataframe to a new csv file
    dataframe1.to_csv('df1transpose.csv')

    # Return the original and transposed dataframes as a tuple
    return data_read, dataframe1

# Example usage
filename = "API_19_DS2_en_csv_v2_4902199.csv"
dataframe_years, dataframe_countries = file_modify(filename)

print(dataframe_countries.describe())

print(dataframe_years.info())

print(dataframe_years.isnull().sum())

data_read = dataframe_years.fillna(0)
print(data_read)

def line_plot(dataframe, indicator):
    """
    Plots a line chart of the given indicator for a select list of countries over time.

    Args:
    dataframe (pandas dataframe): Dataframe containing data for all countries and indicators.
    indicator (str): The name of the indicator to be plotted.

    Returns:
    None
    """
    # Save the dataframe to a csv file
    dataframe.to_csv('data_read122.csv')
    
    # Drop unnecessary columns
    dataframe = dataframe.drop(["Country Code","Indicator Code"],axis =1)
    
    # Set the index to the indicator name
    dataframe.set_index("Indicator Name",inplace = True)
    
    # Select the rows corresponding to the given indicator
    dataframe = dataframe.loc[indicator]
    
    # Reset the index to move the indicator name to a column
    dataframe = dataframe.reset_index(level = "Indicator Name")
    
    # Select a subset of countries
    countries = ["India", "Australia", "United States", "Bangladesh", "Pakistan"]
    dataframe = dataframe.query('`Country Name` in @countries')
    
    # Plot the data
    dataframe.plot(x= "Country Name" ,y = ['1970', '1980', '1990','2000','2010','2020'],figsize = (15,5))
    
    # Add a title to the plot
    plt.title(indicator, fontsize=20)
    
    # Display the plot
    plt.show()

#Calling the line_plot function to plot a line chart
line_plot(data_read, "Population growth (annual %)")
line_plot(data_read, "CO2 emissions from liquid fuel consumption (% of total)")


def bar_plot(dataframe, indicator):
    """
    Plots a bar chart of the given indicator for a select list of countries.

    Args:
    dataframe (pandas dataframe): Dataframe containing data for all countries and indicators.
    indicator (str): The name of the indicator to be plotted.

    Returns:
    None
    """
    # Drop the columns "Country Code" and "Indicator Code" from the dataframe
    dataframe = dataframe.drop(["Country Code","Indicator Code"],axis =1)
    # Set the index of the dataframe to "Indicator Name"
    dataframe.set_index("Indicator Name",inplace = True)
    # Select the rows corresponding to the given indicator
    dataframe = dataframe.loc[indicator]
    # Reset the index of the dataframe to "Indicator Name"
    dataframe = dataframe.reset_index(level = "Indicator Name")
    # Select a list of countries to be plotted
    countries = ["India", "Australia", "United States", "Bangladesh", "Pakistan"]
    # Filter the dataframe to select only the rows corresponding to the selected countries
    dataframe = dataframe.query('`Country Name` in @countries')
    # Plot a bar chart of the selected data
    dataframe.plot(x= "Country Name" ,y = ['1970', '1980', '1990','2000','2010','2020'],figsize = (15,5), kind = "bar")
    # Set the title of the plot to the indicator name
    skewness = dataframe.loc[:, '1970':'2020'].skew()
    kurtosis = dataframe.loc[:, '1970':'2020'].kurtosis()
    print(skewness)
    print(kurtosis)
    
    plt.title(indicator, fontsize=20)
    # Display the plot
    plt.show()

#Calling the bar_plot function to plot a bar graph
bar_plot(data_read, "Agricultural land (% of land area)")
bar_plot(data_read, "Cereal yield (kg per hectare)")



def heat_map():
     """
    
    Generates a heatmap of the correlation between select indicators for India.
    Returns:
    None
    
    """
    # Group the data by country name
    grouped = data_read.groupby("Country Name")
    
    # Filter rows related to India
    bd_group = grouped.get_group("India")
    
    # Set the indicator name as the index
    grp_1=bd_group.set_index("Indicator Name")
    
    # Select data from 2000 to 2021
    grp_1 = grp_1.loc[:, '2000':'2021']
    
    # Transpose the dataframe
    grp_1=grp_1.transpose()
    
    # Select a subset of indicators to be used in the heatmap
    indicators = [ "CO2 emissions from liquid fuel consumption (% of total)",
                  "Electric power consumption (kWh per capita)",
                  "Urban population growth (annual %)",
                  "Rural population living in areas where elevation is below 5 meters (% of total population)",
                  "Total greenhouse gas emissions (kt of CO2 equivalent)"]
    
    # Extract the data for the selected indicators
    bd_indicators = grp_1[indicators]
    
    # Compute the correlation matrix for the selected indicators
    corr_matrix = bd_indicators.corr()
    
    # Set the labels for the heatmap
    labels = ["CO2 emissions from liquid fuel consumption (% of total)",
              "Electric power consumption (kWh per capita)",
              "Urban population (% of total population)",
              "Rural population living in areas where elevation is below 5 meters (% of total population)",
              "Total greenhouse gas emissions (kt of CO2 equivalent)"]
    
    # Visualize the correlation matrix as a heatmap
    sns.heatmap(corr_matrix, cmap="RdBu", annot=True, xticklabels=labels, yticklabels=labels)
    
    # Set the title for the heatmap
    plt.title("India Indicators correlation", fontsize=25)
    
    # Show the heatmap
    plt.show()
#Calling the heat_map function to plot a heat_map
heat_map()
