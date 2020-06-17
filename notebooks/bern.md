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

# BioBERT and State-of-the-art NER

Neural NER is cool. 

Domain specific neural-NER is even _cooler_. It's also really hard to do _right_. 

Luckily the folks at DMIS in S. Korea have pain-stakingly created a system, based on pre-trained Bio-BERT models, that extracts and normalizes several key named entity types from medical text. 

It arrives via their web-api (which can be self-hosted!) in the well-tested _PubAnnotate_ format. This means we can also use visualization tools --- namely, `textae`--- to quickly see which entities were extracted and where.

```python
# from cv.data import annotate as annot
# import spacy
```

```python

import requests
from IPython.display import display, HTML

def query_raw(text, url="https://bern.korea.ac.kr/plain"):
    return requests.post(url, data={'sample_text': text}).text
```

```python
snippet = """
Autophagy maintains tumour growth through circulating arginine. 
Autophagy captures intracellular components and delivers them to lysosomes, 
where they are degraded and recycled to sustain metabolism and to enable 
survival during starvation1-5. 
Acute, whole-body deletion of the essential autophagy gene Atg7 in adult mice 
causes a systemic metabolic defect that manifests as starvation intolerance and 
gradual loss of white adipose tissue, liver glycogen and muscle mass1. 
Cancer cells also benefit from autophagy. 
Deletion of essential autophagy genes impairs the metabolism, proliferation, 
survival and malignancy of spontaneous tumours in models of autochthonous cancer6,7. 
Acute, systemic deletion of Atg7 or acute, systemic expression of a 
dominant-negative ATG4b in mice induces greater regression of KRAS-driven cancers 
than does tumour-specific autophagy deletion, which suggests that host autophagy 
promotes tumour growth1,8. 
Here we show that host-specific deletion of Atg7 impairs the growth of multiple 
allografted tumours, although not all tumour lines were sensitive to host autophagy status. 
Loss of autophagy in the host was associated with a reduction in circulating arginine,
and the sensitive tumour cell lines were arginine auxotrophs owing to the lack of 
expression of the enzyme argininosuccinate synthase 1. 
Serum proteomic analysis identified the arginine-degrading enzyme arginase I (ARG1) 
in the circulation of Atg7-deficient hosts, and in vivo arginine metabolic tracing 
demonstrated that serum arginine was degraded to ornithine. ARG1 is predominantly 
expressed in the liver and can be released from hepatocytes into the circulation. 
Liver-specific deletion of Atg7 produced circulating ARG1, and reduced both serum 
arginine and tumour growth. Deletion of Atg5 in the host similarly regulated [corrected] 
arginine and suppressed tumorigenesis, which demonstrates that this 
phenotype is specific to autophagy function rather than to deletion of Atg7. 
Dietary supplementation of Atg7-deficient hosts with arginine partially restored levels 
of circulating arginine and tumour growth. Thus, defective autophagy in the host leads to 
the release of ARG1 from the liver and the degradation of circulating arginine, which is essential
for tumour growth; this identifies a metabolic vulnerability of cancer. 
(PMID:30429607) 
""".replace("\n", "")
# snippet = "genes are nice"
```

```python
annot = query_raw(snippet)
annot
```

```python
# TODO make cell-magics/functions in cv/data/annotate
# TODO prettify css?
html_code = """
<link rel="stylesheet" href="http://textae.pubannotation.org/lib/css/textae.min.css" />
<script src="http://textae.pubannotation.org/lib/textae.min.js"></script>
<div class="textae-editor">
    %s
</div>
"""%annot
HTML(html_code)
```

TODO: extracted NER (pubannotate) to pandas, nextworkx(?)

```python
import panel as pn
pn.extension(
    js_files={'textae': "http://textae.pubannotation.org/lib/textae.min.js"},
    css_files=["http://textae.pubannotation.org/lib/css/textae.min.css"]
)
```

```python

pane = pn.panel("""
<link rel="stylesheet" href="http://textae.pubannotation.org/lib/css/textae.min.css" />
<script src="http://textae.pubannotation.org/lib/textae.min.js"></script>
<div class="textae-editor">
	{
		"text":"Hello World!",
		"denotations":[
			{"span":{"begin":0,"end":5},"obj":"Greet"},
			{"span":{"begin":6,"end":11},"obj":"Object"}
		]
	}
</div>
""")

pane

```

```python
pn.panel('<marquee>Here is some custom HTML</marquee>')

```
