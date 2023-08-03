## Plot Interactivity decisionApp


This app will:
- demonstrate how to enable the user to interact with their bokeh plots through Variables and py_components
- demonstrate how to trigger actions based on clicks, mouse movements or other interactions with Bokeh objects using CustomJS callbacks

### Local Development

In order to run the application, you need to have `dara-core` and `dara-components` installed locally. To install them, run:

```
poetry install
```

To run the application locally, run the following command in the root directory of the project:

```
poetry run dara start
```


### Project Structure

The structure of the project is as follows:
- dara_plot_interactivity/
    - dara_plot_interactivity/
        - definitions.py
        - main.py
        - plot_interactivity.py
        - plotting_utils.py
    - data/
        - countries.json
        - sanctions.csv
    - pyproject.toml

The `main.py` file is setting up the configuration of the application with `ConfigurationBuilder`. 
The `ConfigurationBuilder` is adding the pages to the application.

The application has one page that demonstrates how to enable the user to interact and trigger actions with their bokeh 
plots. The code for the page is located in `plot_interactivity.py` file.

To keep the code for the application tidy, the utility functions are distributed throughout the following files:
- `definitions.py` - global variables 
- `plotting_utils.py` - plotting functions

The `pyproject.toml` file has the information about the name of the application.
