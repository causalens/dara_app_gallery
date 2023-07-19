from dara.core.configuration import ConfigurationBuilder

from dara_interactivity.pages.pycomponents_vs_derived_variables import comparison_page
from dara_interactivity.pages.variables import variables_page
from dara_interactivity.pages.derived_variables import derived_variables_page
from dara_interactivity.pages.py_components import pycomponents_page
from dara_interactivity.pages.expensive_calculations import expensive_calculations_page

# Create a configuration builder
config = ConfigurationBuilder()

# Register pages
config.add_page('Variables', variables_page())
config.add_page('Derived Variables', derived_variables_page())
config.add_page('py_components', pycomponents_page())
config.add_page('Comparison', comparison_page())
config.add_page('Expensive Calculations', expensive_calculations_page())

config.task_module = 'dara_interactivity.tasks'
