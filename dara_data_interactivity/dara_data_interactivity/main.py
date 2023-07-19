from dara.core.configuration import ConfigurationBuilder

from dara_data_interactivity.data_interactivity import DataInteractivityPage

# Create a configuration builder
config = ConfigurationBuilder()

# Register pages
config.add_page('Data Interactivity', DataInteractivityPage())
