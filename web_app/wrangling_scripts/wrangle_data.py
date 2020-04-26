import pandas as pd
import csv
import plotly.graph_objs as go

# Clean dataset
def cleandata(dataset):
    """Clean data for a visualizaiton dashboard

    Keeps data for the top 10 economies
    Saves the results to a excel file

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """    
    df = pd.read_csv(dataset)

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']
    df = df[df['Country Name'].isin(top10country)]
    
    df_melt = df.melt(id_vars=['Country Name','Indicator Name'], 
                      value_vars = ['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015'])
    df_melt.columns = ['Country Name','Indicator Name', 'Year','Value']
    df_melt['Year'] = df_melt['Year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots GDP from 2005 to 2015 in top 10 economies 
    # as a line chart
    
    graph_one = []    
    df = cleandata('data/WDIData.csv')
    df_gdp = df[df['Indicator Name'] == 'GDP (current US$)']
    df_gdp['Value'] = df_gdp['Value'].round(2)


    for country in df_gdp['Country Name'].unique().tolist():
        x_val = df_gdp[df_gdp['Country Name'] == country]['Year'].tolist()
        y_val =  df_gdp[df_gdp['Country Name'] == country]['Value'].tolist()
        graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Change of GDP between 2005 and 2015',
                xaxis = dict(title = 'Year',),
                yaxis = dict(title = 'GDP (Current USD$)'),
                )

# second chart plots the exports and imports in 2014 
    graph_two = []
    df_export = df[(df['Indicator Name'] =='Exports of goods and services (current US$)')&
                     (df.Year == 2014)]
    df_import = df[(df['Indicator Name'] =='Imports of goods and services (current US$)')&
                     (df.Year == 2014)]
    graph_two=[
    go.Bar(name='Export', x=df_export['Country Name'].unique().tolist(), y=df_export['Value'].unique().tolist()),
    go.Bar(name='Import', x=df_import['Country Name'].unique().tolist(), y=df_import['Value'].unique().tolist())
    ]

    layout_two = dict(title = 'Exports & Imports of goods and services (current US$) in 2014',
                xaxis = dict(title = 'Country Name',),
                yaxis = dict(title = 'Value in $'),
                barmode='stack'
                )


# third chart plots co2 emission per capita in 2014
    graph_three = []
    df_co2 = df[(df['Indicator Name'] == 'CO2 emissions (metric tons per capita)') &
           (df.Year == 2014)]
    graph_three.append(
      go.Bar(name='CO2 per capita', x=df_co2['Country Name'].unique().tolist(), y=df_co2['Value'].unique().tolist(),
            marker=dict(color='lightslategrey'))
      )

    layout_three = dict(title = 'CO2 Emissions (Metric Tons Per Capita)',
                xaxis = dict(title = 'Country Name'),
                yaxis = dict(title = 'CO2 Emissions',
                )
                       )
    
# fourth chart shows life expectancy from 2005 to 2015
    graph_four = []
    df_life_exp = df[df['Indicator Name'] == 'Life expectancy at birth, total (years)']
    df_life_exp['Value'] = df_life_exp['Value'].astype('int')
    
    for country in df_life_exp['Country Name'].unique().tolist():
        x_val = df_life_exp[df_life_exp['Country Name'] == country]['Year'].tolist()
        y_val =  df_life_exp[df_life_exp['Country Name'] == country]['Value'].tolist()
        graph_four.append(
            go.Scatter(
            x = x_val,
            y = y_val,
            mode = 'lines+markers', name = country
                ) 
    )

    layout_four = dict(title = 'Life Expectancy at Birth from 2005 to 2015',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Life Expectancy'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures