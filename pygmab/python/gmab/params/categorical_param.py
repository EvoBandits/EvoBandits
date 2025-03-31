from functools import cached_property

from gmab.params.base_param import BaseParam

ChoiceType = bool | int | float | str | None


class CategoricalParam(BaseParam):
    """
    A class representing a categorical param.
    """

    def __init__(self, choices: list[ChoiceType]):
        """
        ToDo
        """
        if not isinstance(choices, list):
            raise ValueError("choices must be a list")
        if not all(isinstance(c, ChoiceType) for c in choices):
            raise ValueError("All elements in choices must be of an immutable type")

        super().__init__(size=1)
        self.choices: list[ChoiceType] = choices

    def __repr__(self):
        return f"CategoricalParam(choices={self.choices})"

    @cached_property
    def bounds(self) -> list[tuple]:
        """
        ToDo
        """
        return [(0, len(self.choices) - 1)]

    def map_to_value(self, actions: list[int]) -> ChoiceType | list[ChoiceType]:
        """
        ToDo
        """
        actions = [self.choices[idx] for idx in actions]

        if len(actions) == 1:
            return actions[0]
        return actions
