import scispacy

__title__ = "cv-py"

__scispacy_version__ = scispacy.__version__

__compatible__ = {
    "cord19_cdcs": "~0.2.3",
    "en_core_sci_sm": __scispacy_version__,
    "en_core_sci_md": __scispacy_version__,
    "en_core_sci_lg": __scispacy_version__,
    "en_ner_craft_md": __scispacy_version__,
    "en_ner_jnlpba_md": __scispacy_version__,
    "en_ner_bc5cdr_md": __scispacy_version__,
    "en_ner_bionlp13cg_md": __scispacy_version__,
    "en_core_sci_scibert": __scispacy_version__
}
__release__ = True
