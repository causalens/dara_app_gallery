from dara.core.configuration import ConfigurationBuilder

from dara_plot_interactivity.plot_interactivity import PlotInteractivityPage

# Create a configuration builder
config = ConfigurationBuilder()

# Register pages
config.add_page('Plot Interactivity', PlotInteractivityPage())
