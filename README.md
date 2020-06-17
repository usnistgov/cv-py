# cv-py
This repository provides a low-friction interface to the COVID-19 Research Challenge Dataset (CORD19) through an installable data-package, similar to the way trained NLP/ML models are tracked/distributed in the various corresponding libraries (SpaCy, gensim, flair, nltk, etc.). This is intended to provide smooth access to the collection of publications for researchers and analysts, along with validated tools for preliminary preprocessing and interface to various formats. 



## Getting Started
This package is meant to assist analysts in accessing and processing COVID-19 publication data as quickly as possible. Please keep in mind that it is a work-in-progress, as the data situation evolves rapidly, the codebase and subsequent user interface likely will as well. 

### Demo
Roughly, features are split into *resources* (data and models to use in your analyes) and *tools* (things to help in getting data into models, into analysis). 

Some of the already supported features:

#### Tasks-as-data
Structured access to CORD19 challenge tasks as typed dataclasses:
```python
from cv_py.resources.builtins import cord19tasks
cord19tasks()[-2].question
>>> 'What do we know about COVID-19 risk factors?'
```
#### Public API helper-functions
Make use of powerful state-of-the-art Neural question answering, to search for relevant CORD19 passages with a single query to Korea University's [*covidAsk*]() model:
```python
from cv_py.tools.remote import covid_ask
ans = covid_ask(cord19tasks()[-2].question)
ans['ret'][0]['answer']
>>> 'patients with cancer had a higher risk of COVID-19'
```
#### Scalable, Fast, *Versioned* access to Data
Backed by the NIST-curated [COVID-19 Data Repository](https://covid19-data.nist.gov/), and versioned to ensure your pipelines don't break as the data changes:

 ```python
from cv_py.resources.datapackage import load
df = load("cord19_cdcs")

```
It's backed by Dask, using read-optimized Apache Parquet storage format. Need to get back to a more familiar `pandas` framework? Each parallel, lazy partition is itself a DataFrame, only a `.compute()` away. 

Data archival is achieved through the [cached archives](https://github.com/usnistgov/cord19-cdcs-nist) of the CDCS instance. If you are looking for a more DIY access to data in its raw form, head over to that releases page and download desired raw XML, JSON, or CSV data types. 

### Installation
For now, this repository is installable via `pip` directly from its github location: 

`pip install cv-py`

This will provide access to `cv-py` modules via the `cv_py` namespace, and includes `dask` and `scikit-learn` by default. `cv-py` is built to provide smooth access to *existing tools*, as needed for analysis. Consequently, dependencies to use the various tools supported are split into groups for convenience, installed with brackets as `pip install cv-py[extras]`:

 extras alias   |   dependencies
 ---            |   ---
 spacy          |   [`spacy`](https://spacy.io/usage), [`textacy`](https://github.com/chartbeat-labs/textacy), [`scispacy`](https://github.com/allenai/scispacy)
 flair          |   `flair`
 viz            |   `seaborn`, `holoviews[recommended]`
 
These can be combined, e.g. `pip install cv-py[flair,viz]`.

 
### Usage
In addition to installing `cv-py`, installation will provide a `cv-download` command to be used in a terminal (in the same environment `cv-py` was installed). The default options will automatically install the latest compatible version of the curated CORD19 dataset. Use the `-h` flag for more information. 

After downloading, the data can be loaded directly: 

```python
from cv_py.resources import datapackage
df = datapackage.load("cord19_cdcs")
```

The `load()` function returns an out-of-memory Dask Datafame, ensuring scalability on a wide range of devices. Most Pandas functions are available, and the underlying `pandas.DataFrame` object is exposed upon executing the `.compute()` method. See [Dask Documentation](https://docs.dask.org/en/latest/dataframe.html) for more details. More data interfaces are to come!


## Why (another) package?
There are many excellent packages in the Python ecosystem for completing NLP tasks. In fact, `cv-py` depends on _many_ of them. 

However, one of the key barriers to rapid NLP analysis and tool development lies in _pipeline construction_... namely, cleaning, data munging, and "gluing together" all the libraries that, united, achieve the decision support we needed in the first place. 

This is not another attempt at collecting techniques together to create another "NLP framework"; rather, `cv-py` provides some of the "glue" needed to allow rapid data and method interaction between the excellent tools that already exist. 

This is done with the express purpose of _contextualization_ within the problem domain of the CORD-19 challenge, and to assist others in the public who are willing and able to apply their data-science skills, but may otherwise spend far more effort applying "glue" than building solutions. 

## Features (available and planned)

- `resources`: *data and models*
    - `builtins`:
        *lightweight data/models contained natively*
        - Tasks: *from Kaggle*
        - TREC topics (?)
    - `datapackage`:
        *installable with `cv-download`*
        - CORD19: *papers and NER tags from NIST CDCS*
        - Sci-spaCy [models](https://allenai.github.io/scispacy/): *see their documentation for usage* 
- `tools` : *to assist in moving CORD19 data around*
    - `process`: *to spacy, flair, etc.* (WIP)
        - parallelism and scale (pandas -> dask)
        - ease of use: built-in pipeline tools
    - `remote`: *external tools, accessible via API*
        - Univ. S. Korea Neural NER APIs (CovidAsk, BERN(?))
        - TextAE pubannotation vizualizer (WIP)



## Development/Contribution Guidelines
More to come, but primary requirement is the use of [Poetry](https://python-poetry.org/). 

Notebooks are kept nicely git-ified thanks to [Jupytext](https://github.com/mwouts/jupytext)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
