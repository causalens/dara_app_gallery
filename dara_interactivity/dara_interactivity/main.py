from dara.core.configuration import ConfigurationBuilder, Configuration
from dara.core.visual.components import Menu, RouterContent
from dara.core.visual.components.sidebar_frame import SideBarFrame
from dara.core.visual.template import TemplateBuilder

from dara_interactivity.pages.pycomponents_vs_derived_variables import comparison_page
from dara_interactivity.pages.variables import variables_page
from dara_interactivity.pages.derived_variables import derived_variables_page
from dara_interactivity.pages.py_components import pycomponents_page
from dara_interactivity.pages.expensive_calculations import expensive_calculations_page

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

# Register pages
config.add_page('Variables', variables_page())
config.add_page('Derived Variables', derived_variables_page())
config.add_page('py_components', pycomponents_page())
config.add_page('Comparison', comparison_page())
config.add_page('Expensive Calculations', expensive_calculations_page())

config.task_module = 'dara_interactivity.tasks'
