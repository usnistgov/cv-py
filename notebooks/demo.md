---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.0
  kernelspec:
    display_name: Python [conda env:cv-py]
    language: python
    name: conda-env-cv-py-py
---

<!-- #region slideshow={"slide_type": "slide"} -->
# cv-py

*Collection of tools and techniques to kick-start analysis of the COVID-19 Research Challenge Dataset* 
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## Motivation
For those of us that analyze data, the vast majority of our time is spent **preprocessing**. 

- finding data sources
- manipulating data to comply to desired frameworks
- transforming intermediary data products
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
If we hope for rapid adoption and application of our datasets, reducing these points of friction is key.

> *As part of the reference dataset design, deployment, and maintenance!* 


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## Proposed Solutions

A need for easy, reliable access to **resources**
- Low-friction interface to CORD19 and associated data
- Versioning of data products and data pipelines, in tandem
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
and the models/frameworks needed to **process them**
- Pre-configured defaults for processing
- Optional by design: don't get in your way if ignored
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Feature Demo
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
> Please keep in mind that it is a work-in-progress, as the data situation evolves rapidly, the codebase and subsequent user interface likely will as well. 
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Tasks-as-data
Structured access to CORD19 challenge tasks as typed `dataclass`es
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
from pprint import pprint
from cv_py.resources.builtins import cord19tasks, CordTask, CordTasks
task = cord19tasks()[-2]
pprint((task.question, task.details, task.subtasks))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Public API helper-functions
Make use of powerful state-of-the-art Neural question answering, to search for relevant CORD19 passages with a single query to Korea University's [*covidAsk*](https://covidask.korea.ac.kr/) model:
<!-- #endregion -->

```python slideshow={"slide_type": "-"}
from cv_py.tools.remote import covid_ask
ans = covid_ask(task.question)

print(task.question, '\n')
pprint([r['answer'] for r in ans['ret']])
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Scalable, Fast, *Versioned* Access to Data
- Datapackages backed by the NIST-curated [COVID-19 Data Repository](https://covid19-data.nist.gov/)
- Versioned as releases [usnistgov/cord19_cdcs_nist](https://github.com/usnistgov/cord19-cdcs-nist) to ensure your pipelines don't break as the data changes.
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
from cv_py.resources.datapackage import load
d = load("cord19_cdcs")

d[['cord_uid', 'title', 'authors', 'publish_time']].head()
```

<!-- #region slideshow={"slide_type": "subslide"} -->
- Validated against CDCS schema and saved as read-optimized Apache Parquet
- Includes pre-extracted state-of-the-art neural NER keywords, courtesy of Sci-spaCy
<!-- #endregion -->

```python slideshow={"slide_type": "-"}
pprint(d.columns.tolist(), compact=True)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Journal/publishing location distribution
<!-- #endregion -->

```python slideshow={"slide_type": "-"}
d.journal.value_counts().head(20)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Beware: AI2's `cord_uid` intentionally "clusters" documents, leading to name collisions!
<!-- #endregion -->

```python slideshow={"slide_type": "-"}
d.cord_uid.value_counts().head(20)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## How to Get Started
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Installation

```bash
$ pip install cv-py
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Comes with basics, like `scikit-learn`, `pandas`, `dask`.

**Modular design:** 
```bash
$ pip install cv-py[extras]
```

 extras alias   |   dependencies
 ---            |   ---
 spacy          |   `spacy`, `textacy`, `scispacy`
 flair          |   `flair`
 viz            |   `seaborn`, `holoviews[recommended]`
 
These can be combined, e.g. `cv-py[flair,viz]`. More to come!
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Getting Remote Resources
Installation provides a `cv-download` command to your PATH

Options: 
 - `cord19_cdcs` (checks/installs compatible updates!)
 - Sci-spaCy pretrained models



This keeps the initial install size low, and your workflow flexible. 
> optional dependencies are checked for/suggested as you need them. 
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Going Forward
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Upcoming and Possible Features

- Keyword annotation vizualization/interface
- Interface to TREC topics, labels, etc
- Process to representations for network analyses, knowledge graphs
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### How can I help?

Python development is always appreciated (tests, process tools, etc)

If you **do** find use for `cv-py` please submit your notebooks, scripts, etc as examples for documentation.  If others can use your techniques, we might even inlude them as a contextualized, reproducible tools in the package!


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Future of Continuous Delivery for Data@NIST

Importance of *developing, deploying, and continuously improving* our datasets and the analyses that accompany them. **And making that easy.**

> I've built a lot of `cv-py` infrastructure by hand...

Alternatives: 
- [Data Version Control](https://dvc.org/) (DVC) 
- [Intake](https://intake.readthedocs.io/en/latest/) 
- [Quilt](https://quiltdata.com/)
- [DoltHub](https://www.dolthub.com/)

Interest in this? Experience in what has/hasn't worked? -> Let me know!
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Thank you

**Thurston Sexton**

tbs4@nist.gov
<!-- #endregion -->

```python slideshow={"slide_type": "skip"}
import scispacy
import spacy

nlp = spacy.load("en_core_sci_sm")
text = """
Myeloid derived suppressor cells (MDSC) are immature 
myeloid cells with immunosuppressive activity. 
They accumulate in tumor-bearing mice and humans 
with different types of cancer, including hepatocellular 
carcinoma (HCC).
"""
doc = nlp(text)

pprint(list(doc.sents))

print(doc.ents)
```

```python slideshow={"slide_type": "skip"}
from collections import Counter
from itertools import chain
# @sdc
def get_ents(d):
    return [e.text for e in d.ents]

Counter(chain(*d.abstract
     .dropna()
     .to_bag()
     .map(nlp)
     .map(get_ents)
     .take(100)
)).most_common(15)
```
