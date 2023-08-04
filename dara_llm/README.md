## Large Language Model decisionApp

![LLMs](https://github.com/causalens/dara_app_gallery/blob/DO-1580-add-images-to-app-gallery-readme-md/img/llm.png?raw=true) 

This app will:
- Demonstrate how you can incorporate a LLM chat box into your decision app to understand model insights.


### Local Development

In order to run the application, you need to have `dara-core` and `dara-components` installed locally. To install them, run:

```
poetry install
```

To run the application locally, run the following command in the root directory of the project:

```
poetry run dara start
```

This app uses OpenAI's ChatGPT model as its LLM of choice. To use this functionality you must set the `OPENAI_API_KEY` in your environment. You can so by setting the following in your .env file:

``` .env
OPENAI_API_KEY=<API_KEY>
```

If you do not have an OpenAI account you can sign up for one [here](https://platform.openai.com/signup). Once you have an account you can generate new API keys in your [user settings](https://platform.openai.com/account/api-keys).

### Project Structure

The structure of the project is as follows:
- dara_llm/
    - dara_llm/
        - chatbox.py
        - definitions.py
        - main.py
        - sales_predictions.py
        - tasks.py
    - pyproject.toml

The `main.py` file is setting up the configuration of the application with `ConfigurationBuilder`. 
The `ConfigurationBuilder` is adding the pages to the application.

This application has one page called "Sales Predictions". This page uses a dataset of marketing spend in various channels and the resulting sales. A simple OLS model is used to predict Sales using linear regression with the marketing spend as independent variables. At the top right corner you can find a "Ask ChatGPT" button. Clicking this button will present a form that allows the user to query ChatGPT with questions about the model. A list of predefined questions is provided along with the ability to ask a custom question. The code for this form is kept in `chatbox.py`.

To keep the code tidy, all definition variables are located in the `definitions.py` file.  The `tasks.py` contains the function that queries ChatGPT and it is ran in a separate process as it is a time-expensive calculation. 

The `pyproject.toml` file has the information about the name of the application.
