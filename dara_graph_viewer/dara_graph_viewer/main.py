from dara.core.configuration import ConfigurationBuilder

from dara_graph_viewer.pages import IntroductionPage, InfluentialIndividualsPage, ConnectionsPage, StrongestPathsPage
# Create a configuration builder
config = ConfigurationBuilder()

# Register pages
config.add_page('Social Networks', IntroductionPage())
config.add_page('Influential Individuals', InfluentialIndividualsPage())
config.add_page('Connections', ConnectionsPage())
config.add_page('Strongest Path', StrongestPathsPage())

