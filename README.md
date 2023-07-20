# Hunty Datasets EDA
> Early exploration on data and implementation of OpenAI ada-02

## Directory

```
.
├── .env
├── EDA.ipynb
├── README.md
├── dataset
│   ├── .gitkeep
│   ├── postings.csv
│   └── users.csv
├── model
│   ├── .gitkeep
│   ├── embeddings
│   │   ├── job<id>.npy
│   │   └── id_user<id>.npy
│   └── model.py
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── config.py
│   ├── data_utils.py
│   ├── plots.py
│   └── preprocessing.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_data_utils.py
    └── test_preprocessing.py

7 directories, 10033 files
```
## The Business problem

To vevelop a job recommendation system based on the similarity between the
characteristics of vacancies and user profiles.

## Technical aspects

This notebook will guide you through all the steps made to explore data, evaluate model implementation and test/define key functions for further deployment.

The technologies involved are:
- Python as the main programming language
- Pandas for consuming data from CSVs files
- **Numpy to store binary representations of vectors**
- OpenAI Ada 02, nltk for building features and training ML models
- Matplotlib and Seaborn for the visualizations
- Jupyter notebooks to make the experimentation in an interactive way

## Installation

A `requirements.txt` file is provided with all the needed Python libraries for running this project. For installing the dependencies just run:

```console
$ pip install -r requirements.txt
```

*Note:* We encourage you to install those inside a virtual environment.

## Code Style

Following a style guide keeps the code's aesthetics clean and improves readability, making contributions and code reviews easier. Automated Python code formatters make sure your codebase stays in a consistent style without any manual work on your end. If adhering to a specific style of coding is important to you, employing an automated to do that job is the obvious thing to do. This avoids bike-shedding on nitpicks during code reviews, saving you an enormous amount of time overall.

[Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/) for automated code formatting in this project, you can run it with:

```console
$ isort --profile=black . && black --line-length 88 .
```

Wanna read more about Python code style and good practices? Please see:
- [The Hitchhiker’s Guide to Python: Code Style](https://docs.python-guide.org/writing/style/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
