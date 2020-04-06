# cv-py
This repository provides the COVID-19 Research Challenge Dataset as an installable data-package, similar to the way trained NLP/ML models are tracked/distributed in the various corresponding libraries (SpaCy, gensim, flair, nltk, etc.). This is intended to provide smooth access to the collection of publications for researchers and analysts, along with validated tools for preliminary preprocessing and interface to various formats. 

Data archival is achieved through the [cached archives](https://github.com/usnistgov/cord19-cdcs-nist) of a NIST-curated CORD19 instance, powered by the [Configurable Data Curation System](https://www.nist.gov/itl/ssd/information-systems-group/configurable-data-curation-system-cdcs/about-cdcs) (CDCS). If you are looking for a more DIY access to data in its raw form, head over to that releases page and download desired XML, JSON, or CSV data types. 

## Getting Started
This package is meant to assist analysts in accessing and processing COVID-19 publication data as quickly as possible. Please keep in mind that it is a work-in-progress, as the data situation evolves rapidly, the codebase and subsequent user interface likely will as well. 

### Installation
For now, this repository is installable via `pip` directly from its github location: 

`pip install git+https://github.com/usnistgov/cv-py.git`

This will provide access to `cv-py` modules via the `cv` namespace. 

### Usage
In addition to installing `cv-py`, installation will provide a `cv-download` command to be used in a terminal (in the same environment `cv-py` was installed). The default options will automatically install the latest compatible version of the curated CORD19 dataset. Use the `-h` flag for more information. 

After downloading, the data can be loaded directly: 

```python
from cv.data import cdcs
df = cdcs.load()
```

The `load()` function returns an out-of-memory Dask Datafame, ensuring scalability on a wide range of devices. Most Pandas functions are available, and the underlying `pandas.DataFrame` object is exposed upon executing the `.compute()` method. See [Dask Documentation](https://docs.dask.org/en/latest/dataframe.html) for more details. More data interfaces are to come!


## Why (another) package?
There are many excellent packages in the Python ecosystem for completing NLP tasks. In fact, `cv-py` depends on _many_ of them. 

However, one of the key barriers to rapid NLP analysis and tool development lies in _pipeline construction_... namely, cleaning, data munging, and "gluing together" all the libraries that, united, achieve the decision support we needed in the first place. 

This is not another attempt at collecting techniques together to create another "NLP framework"; rather, `cv-py` provides some of the "glue" needed to allow rapid data and method interaction between the excellent tools that already exist. 

This is done with the express purpose of _contextualization_ within the problem domain of the CORD-19 challenge, and to assist others in the public who are willing and able to apply their data-science skills, but may otherwise spend far more effort applying "glue" than building solutions. 

## Features (available and planned)

### Pre-processed data -- `cv.data`
- data "products" as packages -- `cdcs`
- tools to reproduce/alter text preprocessing workflows -- `clean`  (WIP)
- NER annotation and processing tools (spacy, scibert) -- `annotate`  (WIP)

### State-of-the-art VSM NLP -- `cv.embed` (WIP)
- Bag of Words and Topic Modeling (spacy/textacy) -- `bow`
- Word and Character-level embeddings (flair) -- `vsm` 

### Visualization and EDA -- `cv.viz` (WIP)
- topic model exploration (termite) -- `termite`
- Dimensionality reduction and clustering (umap, hdbscan) -- `drc`

...more?
