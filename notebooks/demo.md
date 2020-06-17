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
    display_name: Python [conda env:cord19dev]
    language: python
    name: conda-env-cord19dev-py
---

```python
client

```

<!-- #region slideshow={"slide_type": "slide"} -->
## Basic Uses
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
- Resources
    - Builtins:
        *data contained natively*
        - Tasks: *from Kaggle*
    - Datapackages
        - CORD19: *from CDCS*
        
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
- Tools
    - Processing (to spacy, flair, etc.)
        - parallelism and scale (pandas -> dask)
        - ease of use: built-in pipeline tools
    - External Tools
        - Univ. S. Korea Neural NER APIs (CovidAsk, BERN)
        - TextAE pubannotation vizualizer

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Load Tasks
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
from cv_py.resources.builtins import cord19tasks, CordTask

tasks = cord19tasks()
task = -2
pprint((tasks[task].question,
        tasks[task].details,
        tasks[task].subtasks))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Query *AskCovid*
<!-- #endregion -->

```python slideshow={"slide_type": "-"}
from cv_py.tools.remote import covid_ask
ans = covid_ask(tasks[task].question)

print(tasks[task].question, '\n')
pprint([r['answer'] for r in ans['ret']])
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Load CORD19
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
from cv_py.resources.datapackage import load
d = load("cord19_cdcs")

```

```python slideshow={"slide_type": "subslide"}
d.columns.tolist()
```

```python slideshow={"slide_type": "subslide"}
d.head()[['cord_uid', 'title', 'authors', 'publish_time']]
```

```python slideshow={"slide_type": "subslide"}
d.journal.value_counts().head(20)
```

```python slideshow={"slide_type": "subslide"}
d.cord_uid.value_counts().head(20)
```

```python
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

```python
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

```python

```
