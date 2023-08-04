## Graph Viewer decisionApp

![Graph Viewer](https://github.com/causalens/dara_app_gallery/blob/DO-1580-add-images-to-app-gallery-readme-md/img/graph_viewer.png?raw=true) 

This app will:
- Demonstrate how to use the `CausalGraphViewer` to display your graphs or networks.
- Demonstrate how to update the metadata of your `CausalGraph` so that the `CausalGraphViewer` can display relevant information through colors and tooltips.
- Demonstrate how to make your `CausalGraphViewer` interactive so the page can update based on the user selecting nodes or edges.


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
- dara_graph_viewer/
    - dara_graph_viewer/
        - pages/
            - __init__.py
            - influential_individuals.py
            - introduction.py
            - strongest_paths.py
        - definitions.py
        - main.py
        - utils.py
    - pyproject.toml

The `main.py` file is setting up the configuration of the application with `ConfigurationBuilder`. 
The `ConfigurationBuilder` is adding the pages to the application.

This application has three pages:
- Introduction - articulates the purpose of the app and allows the user to explore the datasets that the app utilizes. This page highlights how the `on_click_edge` argument of the `CausalGraphViewer` allows you to update your page based on what edge the user selects in their graph.
- Influential Individuals - allows the user to explore the influential individuals in their network through various centrality measures. This page highlights how to update the aesthetic properties of your graph to display important information to the user.
- Strongest Paths - allows the user to explore the strongest path between two individuals in their network using Dijkstra's algorithm. This page highlights how the `on_click_node` argument of the `CausalGraphViewer` allows you to update your page based on what nodes the user selects in their graph.

To keep the code tidy, all definition variables are located in the `definitions.py` file and all accompanying utility functions are kept in `utils.py`.

The `pyproject.toml` file has the information about the name of the application.
