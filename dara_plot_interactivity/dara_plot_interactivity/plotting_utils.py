"""
Copyright 2023 Impulse Innovations Limited


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
import math
import numpy
import pandas as pd
from typing import List
from pandas import json_normalize

from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models import ColorBar, GeoJSONDataSource, HoverTool, LinearColorMapper
from bokeh.palettes import RdBu
from bokeh.plotting import figure

from dara_plot_interactivity.definitions import COUNTRIES, AREA_FEATURE, YEAR_FEATURE

def df_to_geojson(df, sep="."):
    """
    The opposite of json_normalize
    """
    df = df.replace(to_replace=numpy.nan, value='').replace(to_replace=numpy.NaN, value='')
    result = []
    for idx, row in df.iterrows():
        parsed_row = {}
        for col_label, v in row.items():
            keys = col_label.split(sep)

            current = parsed_row
            for i, k in enumerate(keys):
                if i==len(keys)-1:
                    current[k] = v
                else:
                    if k not in current.keys():
                        current[k] = {}
                    current = current[k]
        # save
        result.append(parsed_row)

    geojson = {
        "type": "FeatureCollection",
        "features": result
    }
    return geojson

def world_map(data: pd.DataFrame, feature: str, year: int):
    """
    Constructs a world map using Geopandas and Bokeh.

    Constructs a GeoJSONDataSource out of the data and a dictionary of countries and their coordinates.
    Passes the GeoJSONDataSource into a Bokeh Patches model and uses a color mapper to color the countries
    based on their values of the feature.

    :param data: the data in question
    :param feature: the variable from the data to inspect
    :param year: filter for the data by year
    :return the Bokeh figure to be plotted by the Bokeh extension
    """
    # select data according to feature and year
    plot_data = data[data[YEAR_FEATURE] == year].copy()

    countries = json_normalize(COUNTRIES["features"])

    # merge with the selected data
    plot_data = plot_data.add_prefix('properties.')
    plot_data_with_geometry = pd.merge(countries, plot_data, on=['properties.' + AREA_FEATURE], how='left')
    
    # convert this data into a GeoJSONDataSource to be used by the Bokeh patch (heat map)
    geo_source = GeoJSONDataSource(geojson=json.dumps(df_to_geojson(plot_data_with_geometry)))

    p = figure(
        sizing_mode='stretch_both',
        height=450,
        match_aspect=True,
        tooltips=[('Country', '@area'), ('value', '@{' + feature + '}{,}')],
        toolbar_location='above',
        tools='reset',
        title=f"Countries by {' '.join(feature.split('_'))}",
    )

    # create color mapper for the heat map
    min_val = plot_data_with_geometry['properties.' + feature].min() 
    max_val = plot_data_with_geometry['properties.' + feature].max()
    color_mapper = LinearColorMapper(palette=RdBu[11], low=min_val, high=max_val)

    # create a sidebar that depicts the color mapper
    color_bar = ColorBar(
        color_mapper=color_mapper,
        label_standoff=5 if max_val < 1e3 else 15,
        width=20,
        location=(1, 0),
        formatter=NumeralTickFormatter(format='0.0a')
    )
    p.add_layout(color_bar, 'right')

    # create the heat map
    fill_color = {'field': feature, 'transform': color_mapper}
    p.patches('xs', 'ys', fill_color=fill_color, line_color='black', line_width=0.2, source=geo_source)

    p.axis.visible = False
    p.grid.grid_line_color = None
    p.toolbar.logo = None

    return p


def top_ten_countries_barplot(data: pd.DataFrame, feature: str, year: int):
    """
    Constructs a Bokeh bar chart of the top ten countries according to the feature and year selected.

    :param data: the data in question
    :param feature: the variable from the data to inspect
    :param year: filter for the data by year
    :return the Bokeh figure to be plotted by the Bokeh extension
    """

    plot_data = data[data[YEAR_FEATURE] == year][[feature, AREA_FEATURE]].copy()
    plot_data = plot_data.sort_values(feature, ascending=False)[[feature, AREA_FEATURE]].iloc[:10]
    plot_data = plot_data.set_index(AREA_FEATURE)[feature]
    plot_data = plot_data.reset_index(name='value').rename(columns={AREA_FEATURE: 'country'})
    plot_data['color'] = RdBu[11][:len(plot_data)]

    p = figure(
        title=f"Top 10 countries: {' '.join(feature.split('_'))}",
        x_range=plot_data['country'].tolist(),
        sizing_mode='stretch_both',
        toolbar_location=None,
        tooltips='@country: @value{,}',
    )

    p.vbar(x='country', top='value', color='white', fill_color='color', width=0.9, source=plot_data)
    p.xaxis.major_label_orientation = math.pi / 8
    p.xgrid.grid_line_color = None
    p.yaxis.formatter = NumeralTickFormatter(format='0.0a')
    p.yaxis.axis_label = f"{feature.replace('_', ' ')}"
    p.yaxis.axis_label_text_font_size = '8pt'
    p.xaxis.major_label_text_font_size = '6pt'

    return p


def timeseries_plot(data: pd.DataFrame, countries: List[str], feature: str):
    """
    Constructs a Bokeh timeseries line plot of the selected feature filtered by selected countries.

    :param data: the data in question
    :param countries: filter for the data by country
    :param feature: the variable from the data to inspect
    :return the Bokeh figure to be plotted by the Bokeh extension
    """
    plot_data = data[data[AREA_FEATURE].isin(countries)][[AREA_FEATURE, YEAR_FEATURE, feature]].copy()
    plot_data = plot_data.pivot(index=[YEAR_FEATURE], columns=[AREA_FEATURE]).reset_index()
    plot_data.columns = [col if col else YEAR_FEATURE for col in plot_data.columns.get_level_values(1).rename(None)]

    p = figure(sizing_mode='stretch_both', title=f"{' '.join(feature.split('_'))}", toolbar_location=None)
    lrends = []
    for i, col in enumerate(plot_data.columns):
        if col == YEAR_FEATURE:
            continue
        lrend = p.line(YEAR_FEATURE, col, legend_label=col, line_width=3, source=plot_data, color=RdBu[11][i])
        lrends.append(lrend)

    hover = HoverTool(
        renderers=[lrend for lrend in lrends],
        tooltips=[(f'{country}', '@{%s}{0.00}' % country) for country in countries] + [('Year', f'@{YEAR_FEATURE}')],
        formatters={f'@{country}': 'printf' for country in countries},
        toggleable=False,
    )
    p.add_tools(hover)

    p.yaxis.formatter = NumeralTickFormatter(format='0.0a')
    p.yaxis.axis_label = f"{feature.replace('_', ' ')}"
    p.yaxis.axis_label_text_font_size = '8pt'
    p.legend.orientation = 'horizontal'
    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'

    return p
