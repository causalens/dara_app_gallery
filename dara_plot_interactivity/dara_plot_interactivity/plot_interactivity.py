from typing import List
from bokeh.models import TapTool

from dara.core import Variable, py_component, UpdateVariable
from dara.core.definitions import ComponentInstance
from dara.components import Heading, Stack, Grid, Select, Text, Button, Label, Bokeh
from dara.components.plotting import figure_events

from dara_plot_interactivity.definitions import DATA, PLOT_FEATURES, YEAR_FEATURE
from dara_plot_interactivity.plotting_utils import top_ten_countries_barplot, world_map, timeseries_plot


class PlotInteractivityPage:
    def __init__(self) -> None:
        self.countries = Variable([])
        self.feature = Variable('crops_production_tonnes')
        self.year = Variable(2019)

    def __call__(self) -> ComponentInstance:
        """
        Constructs the layout of the page.

        The page displays a a world heat map and bar chart based on a year and feature selected.
        It also displays a time series plot of the feature based on the countries tapped on the world heat map.

        :return: ComponentInstance
        """
        return Stack(
            Heading('Explore Your Dataset'),            
            Text('Explore the map to inspect features for each country', italic=True),
            Grid(
                Grid.Row(
                    Grid.Column(Label(Select(value=self.feature, items=PLOT_FEATURES), value='Column:', direction='horizontal'), span=5),
                    Grid.Column(Label(Select(value=self.year, items=[*DATA[YEAR_FEATURE].unique()]), value='Year:', direction='horizontal'), span=5),
                    Grid.Column(
                        Button(
                            'Reset Selection',
                            icon='refresh',
                            onclick=UpdateVariable(lambda ctx: [], self.countries),                            
                        ),
                    ),
                    height='8%',
                    column_gap=1
                ),
                Grid.Row(
                    Grid.Column(self.display_interactive_world_map(self.feature, self.year)),
                    Grid.Column(self.display_bar_plot(self.feature, self.year)),
                    height='45%'
                ),
                Grid.Row(
                    Grid.Column(self.display_timeseries_plot(self.countries, self.feature)),
                    height='45%'
                ),
            )
        )

    @staticmethod
    def update_countries(ctx):
        """
        Adds the country clicked on in the world map to the list of the page's selected countries.

        To keep the graph clean, it limits to ten selected countries. When it goes over ten, it will
        pop the first country and replace it with the new one.

        :param x: the newly selected country from the world map
        :param y: the current list of selected countries
        :return the updated list of selected countries (at a maximum of ten countries)
        """
        x = ctx.inputs.new
        y = ctx.inputs.old
        if len(y) == 10:
            _ = y.pop(0)
        if x not in y:
            y.append(x)
        else:
            y.remove(x)
        return y

    @py_component
    def display_interactive_world_map(self, feature: str, year: int) -> ComponentInstance:
        """
        Displays a world heat map according to the feature and year selected.

        Adds an interactive component where the user can tap on a country in the map and have it be reflected
        in the page's time series plot. This feature utilizes Bokeh's ability to add CustomJS callbacks.

        If there's no data available for the parameters selected, a warning message is returned instead.

        :param feature: the variable from the data to inspect
        :param year: filter for the data by year
        :return: ComponentInstance
        """
        if DATA[DATA[YEAR_FEATURE] == year][feature].isna().all():
            return Stack(
                Text('No data available for this selection.'),
                align='center'
            )

        p = world_map(DATA, feature, year)

        # create event generator for the figure world_map
        figure_event_generator = figure_events(p)

        """
        Specify what should happen when the user clicks on the world map with the figure_event_generator.

        This must be specified through a snippet of JavaScript code to execute in the browser.
        Within the code there is a cb_obj parameter that contains the object that tiggered the callback
        and there is a cb_data parameter that contains any tool-specific data. The cb_data will have access
        to the source of the graph which is the the GeoJSONDataSource that is defined in the world_map function.

        The following line will grab the index for the glyph (country) that is tapped:
        const index = cb_data.source.selected.indices[0];

        You can then retrieve the name of the country by using this index in the source's data:
        return cb_data.source.data['area'][index];

        This is the data that was passed into the geo_source: gpd.GeoDataFrame(plot_data_with_geometry)

        In the code snippet, there is a log statement of cb_data so that you can get a glimpse of what is happening
        by inspecting the page with developer tools and going into the console.
        You will see the object ({geometries: {…}, source: GeoJSONDataSource}) in  the console logs
        and can inspect the object yourself.

        More information on Bokeh JavaScript callbacks can be found here:
        https://docs.bokeh.org/en/latest/docs/reference/models/callbacks.html#bokeh.models.CustomJS
        """
        click_event = figure_event_generator(
            event_name='CLICK',
            code="""
                console.log(cb_data)
                const index = cb_data.source.selected.indices[0];
                return cb_data.source.data['area'][index];
            """
        )

        # register the CustonJs event in a TapTool
        taptool = TapTool(callback=click_event())
        p.add_tools(taptool)

        # tell Dara what to do with the value returned in the code snippet when the map is clicked on
        # the Variable self.countries is updated with the value returned from the callback via self.update_countries
        events = [('CLICK', [UpdateVariable(self.update_countries, self.countries)])]

        return Bokeh(p, events=events)

    @py_component
    def display_bar_plot(self, feature: str, year: int) -> ComponentInstance:
        """
        Displays a Bokeh bar chart of the top ten countries according to the feature and year selected.

        If there's no data available for the parameters selected, a warning message is returned instead.

        :param feature: the variable from the data to inspect
        :param year: filter for the data by year
        :return: ComponentInstance
        """
        if DATA[DATA[YEAR_FEATURE] == year][feature].isna().all():
            return Stack(
                Text('No data available for this selection.'),
                align='center'
            )

        return Bokeh(top_ten_countries_barplot(DATA, feature, year))

    @py_component
    def display_timeseries_plot(self, countries: List[str], feature: str) -> ComponentInstance:
        """
        Displays a Bokeh time series line plot of the selected feature filtered by selected countries.

        If no countries have been selected, a warning message is returned instead.

        :param countries: filter for the data by country
        :param feature: the variable from the data to inspect
        :return ComponentInstance
        """
        if countries == []:
            return Stack(
                Text(f"Please select countries on the map or in the selctor \
                        to view their {' '.join(feature.split('_'))} through time."),
                align='center'
            )
        return Bokeh(timeseries_plot(DATA, countries, feature), width='100%')
