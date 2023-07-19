## Root Cause Analysis decisionApp


This app will:
- demonstrate how to get inputs from the user through Dara Variables
- demonstrate how to make calculations based on these inputs through Dara DerivedVariables
- demonstrate how to make dynamic layouts based on these inputs through Dara py_components
- outline when to use DerivedVariables vs when to use py_components
- demonstrate how to run DerivedVariables in a separate process

### Local Development

In order to run the application locally, you need to have `dara-core` and `dara-components` installed locally. 

To run the application locally, run the following command in the root directory of the project:

```
poetry run dara start
```


### Project Structure

The structure of the project is as follows:
- dara_interactivity/
    - dara_interactivity/
        - pages/
            - derived_variables.py
            - expensive_calculations.py
            - py_components.py
            - py_components_vs_derived_variables.py
            - variables.py
        - custom_components.py
        - definitions.py
        - main.py
        - tasks.py
    - pyproject.toml

The `main.py` file is setting up the configuration of the application with `ConfigurationBuilder`. 
The `ConfigurationBuilder` is adding the pages to the application.

This application has five pages:
- Variables - explains the concept of a `Variable`
- Derived Variables - explains the concept of a `DerivedVariable`
- py_components - explains the concept of a `py_component`
- Comparison - compares and explains when to use `DerivedVariable` vs `py_components`
- Expensive Calculations - explains how to handle expensive calculations

To keep the code tidy, all definitions and concept explanations are located in the `definitions.py` file, while the `custom_components.py` file holds the styled components reused throughout the application (such as to represent code).
All definitions used throughout the application are located in `definitions.py` and all accompanying utility functions in `definitions_utils.py`. The `tasks.py` contains the function that is ran in a separate process as an expensive calculation. 

The `pyproject.toml` file has the information about the name of the application.
