from dask.distributed import get_worker
from typing import *

_dependency_map = dict(spacy=True, flair=True)
try:
    import spacy
except ImportError:
    _dependency_map["spacy"] = False

try:
    import flair
except ImportError:
    _dependency_map["flair"] = False


def _check_dependencies(dep):
    """
    decorator factory used to check that optional dependencies are satisfied
    Parameters
    ----------
    dep: str
        dependency that the decorated function needs
        (see `_dependency_map`)

    Returns
    -------
    decorated function, or an `ImportError` will be raised.
    """

    def wraps(func):
        def wrapped(*args, **kwargs):
            if not _dependency_map[dep]:
                raise ImportError(f"You may be missing optional dependency {dep}!")
            else:
                return func(*args, **kwargs)

        return wrapped

    return wraps


@_check_dependencies("spacy")
def spacy_dask_context(model: str):
    """ **NOT CURRENTLY SUPPORTED**
    decorator factory that prepares a `spacy.Doc`-processing function for
    use on, e.g., a dask container `map` over strings (the text).

    Inspired by https://github.com/explosion/spaCy/issues/5111#issuecomment-595808605

    >>> sdc = spacy_dask_context('en_core_web_sm')
    >>> bag.map(sdc(lambda d:[str(e) for e in d.ents])).compute()

    # TODO use `nlp.pipe` with some batch size (faster)
        >>> ents = bag.map_partition(process_partition).compute()

    Parameters
    ----------
    model: str
        Alias for a locally installed spacy model, e.g. `en_core_web_sm`

    Returns
    -------
    function that may wrap/decorate a function that processes any `spacy.Doc`
    """

    def wraps(func: Callable[[spacy.tokens.Doc], Any]):
        def wrapped(doc: str, *args, **kwargs):
            worker = get_worker()
            try:
                nlp = worker.nlp
            except AttributeError:
                nlp = spacy.load(model)
                worker.nlp = nlp
            return func(nlp(doc), *args, **kwargs)

        return wrapped

    return wraps


