from typing import Union
import dataclasses

from ._knowledge import Knowledge


@dataclasses.dataclass
class EventModel:
    """A class that models a learning event in TrueLearn algorithm.

    Attributes:
        knowledge: A knowledge representation of the educational resources.
        event_time: A float that specifies the POSIX timestamp when the event occurs.
    """

    knowledge: Knowledge = dataclasses.field(default_factory=Knowledge)
    event_time: Union[float, None] = None
