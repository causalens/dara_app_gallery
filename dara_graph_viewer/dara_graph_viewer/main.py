from dara.core.configuration import ConfigurationBuilder

from dara_graph_viewer.pages import (
    InfluentialIndividualsPage,
    IntroductionPage,
    StrongestPathsPage,
)

# Create a configuration builder
config = ConfigurationBuilder()

# Register pages
config.add_page('Social Networks', IntroductionPage())
config.add_page('Influential Individuals', InfluentialIndividualsPage())
config.add_page('Strongest Path', StrongestPathsPage())
