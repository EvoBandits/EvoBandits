from collections.abc import Sequence
from functools import cached_property

from gmab.params.base_param import BaseParam


class CategoricalParam(BaseParam):
    """
    A class representing a categorical param.
    """

    def __init__(self, choices: Sequence):
        """
        ToDo
        """
        # ToDo: validate and typehint choices?
        # Raise value err if choices is not instanc of Sequence
        # Raise value err if any object in choices is not Choiceype

        super().__init__(size=1)
        self.choices: Sequence = choices

    def __repr__(self):
        return f"CategoricalParam(choices={self.choices})"

    @cached_property
    def bounds(self) -> list[tuple]:
        """
        ToDo
        """
        return [(0, len(self.choices) - 1)]

    def map_to_value(self, actions: list[int]):
        actions = [self.choices[idx] for idx in actions]

        if len(actions) == 1:
            return actions[0]
        return actions
