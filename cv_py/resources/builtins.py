from typing import List, Dict, Union, Optional
import yaml
from dataclasses import dataclass
from dacite import from_dict
from pathlib import Path


@dataclass
class CordTask:
    question: str
    details: str
    subtasks: List[Union[str, List[str]]]


@dataclass
class CordTasks:
    # TODO convenience functions for bulk processing text
    tasklist: List[CordTask]

    def __getitem__(self, item):
        return self.tasklist[item]


def cord19tasks(type_hooks: Optional[Dict] = None) -> CordTasks:
    """
    Retrieve a structured representation of the original CORD19 tasks.
    For convenience, the tasks are stored as typed dataclasses, with a schema:
        > CordTasks: List[CordTask: {
                question: str
                details: str
                subtasks: List[Union[str, List[str]]]
            }]

    Parameters
    ----------
    type_hooks : dict
        type -> callable mappings, instrtucting the constructor to apply the
        passed function to all data of that type. e.g. {str: str.lower}

    Returns
    -------
    CordTasks, a dataclass containing structured text of the CORD19 tasks.
    """
    yml_loc = Path(__file__).parent / "cord-tasks.yml"
    with yml_loc.open() as fp:
        task_dict = yaml.safe_load(fp)
    return from_dict(data_class=CordTasks, data=task_dict)
