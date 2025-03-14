# foerderdatenbank.de

## Instructions
Run every script with `python3 <script_name>` in the console:

- `0_topic_search.py`: Is meant to scrape all search terms from the API. Still incomplete.
- `1_save_search_results_to_html_by_keyword.py`: Use any search term to save the search results from Foerderdatenbank to html files in the html_files folder.
- `2_extract_and_save_program_links_from_html.py`: Scrapes all urls from the result pages of the html_files folder in the main directory and saves to "program_links.json" in main folder.
- `3_scrape_funding_offer_links.py`: Scrapes all data and saves the "scraped_data.json" in main folder as a final step.

## Install
### Basic Requirements
#### Python Version
I recommend using _pyenv_ to install a fitting python version. To install pyenv, please follow allong [this documentation](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) 

After installing pyenv, please remember to set up the suggested [python build environment](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) 

After installing pyenv, you can install a fitting python version:
```bash
pyenv install 3.12
```
#### Poetry
We use Python-Poetry for python virtual environment management. Please follow [this guide](https://python-poetry.org/docs/#installation) to install Poetry.

### Setting Up Working Environment
Using pyenv, we can set the used python version in the working directory and install all required python packages.
```bash
pyenv local 3.12
poetry install
```
Poetry is set up for this repository to create a local virtual environment (see `poetry.toml`). Virtual Studio Code will automatically detect the local virtual environment and will use it for the jupyter notebook or python scripts.

Afterwards we can open a Poetry shell `poetry shell` or run the jupyter notebook in Visual Studio Code.

