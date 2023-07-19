from dara.core.configuration import ConfigurationBuilder

from dara_dataset_wrangler.dataset_wrangler import dataset_wrangler_page

# Create a configuration builder
config = ConfigurationBuilder()

# Register pages
config.add_page('Dataset Wrangler', dataset_wrangler_page())
