## Custom CSS decisionApp

![Custom CSS](https://github.com/causalens/dara_app_gallery/blob/DO-1580-add-images-to-app-gallery-readme-md/img/custom_css.png?raw=true) 

This app will:

- show you how to make custom stylized components through component attributes
- show you how to make custom stylized components through CSS dictionaries and strings
- link you to some resources to learn more about CSS


### Local Development

In order to run the application locally, you need to have `dara-core` and `dara-components` installed locally. 

To run the application locally, run the following command in the root directory of the project:

```
poetry run dara start
```


### Project Structure

The structure of the project is as follows:
- dara_custom_css/
    - dara_custom_css/
        - pages/
            - css_units.py
            - raw_css.py
            - resources.py
        - main.py
    - pyproject.toml

The `main.py` file is setting up the configuration of the application with `ConfigurationBuilder`. 
The `ConfigurationBuilder` is adding the pages to the application.

The application has three pages:
- CSS Units Page - explains CSS units
- Raw CSS Page - explains how to modify CSS properties in decisionApp SDK components
- Resources - a list of links to learn more about CSS

The `pyproject.toml` file has the information about the name of the application.
