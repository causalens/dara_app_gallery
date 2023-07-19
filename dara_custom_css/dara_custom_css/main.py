from dara.core.configuration import ConfigurationBuilder
from dara.core.css import get_icon

from dara_custom_css.pages.resources import ResourcePage
from dara_custom_css.pages.css_units import CSSUnitsPage
from dara_custom_css.pages.raw_css import RawCSSPage

# Create a configuration builder
config = ConfigurationBuilder()


# Register pages
config.add_page(name='Customizing Components', content=RawCSSPage(), icon=get_icon('palette'))
config.add_page(name='CSS Units', content=CSSUnitsPage(), icon=get_icon('ruler'))
config.add_page(name='Learning Resources', content=ResourcePage(), icon=get_icon('book'))
