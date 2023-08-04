## Data Interactivity decisionApp

![Data Interactivity](https://github.com/causalens/dara_app_gallery/blob/master/img/data_interactivity.png?raw=true) 

This app will:
- demonstrate how to enable you to interact with bokeh plots through Variables and py_components
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
- dara_data_interactivity/
    - dara_data_interactivity/
        - data_interactivity.py
        - definitions.py
        - main.py
        - plotting_utils.py
    - data/
        - 401k.csv
    - pyproject.toml

The `main.py` file is setting up the configuration of the application with `ConfigurationBuilder`. 
The `ConfigurationBuilder` is adding the pages to the application.

The application page is located in `data_interactivity.py` and it displays a table of the data with customized formatting along with distribution plots and descriptive statistics of the selected table rows.

To keep the code for the application tidy, the utility functions can be found in:
- `definitions.py` - definitions of global variables used throughout the application
- `plotting_utils.py` - plotting utility functions 

The `pyproject.toml` file has the information about the name of the application.
