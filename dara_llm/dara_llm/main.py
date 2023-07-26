from dara.core.configuration import ConfigurationBuilder

from dara_llm.sales_predictions import SalesPredictionsPage

# Create a configuration builder
config = ConfigurationBuilder()

# Register the task module where your task definitions are defined
config.task_module = 'dara_llm.tasks'

# Register pages
config.add_page('Sales Predictions', SalesPredictionsPage())
