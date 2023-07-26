from dara.core.configuration import ConfigurationBuilder, Configuration
from dara.core.visual.components import Menu, RouterContent
from dara.core.visual.components.sidebar_frame import SideBarFrame
from dara.core.visual.template import TemplateBuilder

from dara_llm.sales_predictions import SalesPredictionsPage

# Create a configuration builder
config = ConfigurationBuilder()

def template_renderer(config: Configuration):
    builder = TemplateBuilder(name='side-bar')

    # Using the TemplateBuilder's helper method - add_router_from_pages
    # to construct a router of page definitions
    router = builder.add_router_from_pages(list(config.pages.values()))

    builder.layout = SideBarFrame(
        content=RouterContent(routes=router.content),
        side_bar=Menu(routes=router.links),
        logo_path='/static/dara_light.svg',
    )

    return builder.to_template()

config.add_template_renderer('side-bar', template_renderer)
config.template = 'side-bar'

# Register the task module where your task definitions are defined
config.task_module = 'dara_llm.tasks'

# Register pages
config.add_page('Sales Predictions', SalesPredictionsPage())
