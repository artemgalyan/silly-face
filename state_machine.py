from abc import abstractmethod, ABC
from collections.abc import Callable
from dataclasses import dataclass

from numpy.typing import NDArray


class Job(ABC):
    @abstractmethod
    def finish(self):
        pass

    @abstractmethod
    def execute(self, frame: NDArray) -> str | None:
        pass

    @abstractmethod
    def finish(self) -> None:
        pass


@dataclass
class State:
    name: str
    mapping: dict[str, 'State' | None]
    action: Job

    def add_edge(self, name: str, state: 'State') -> 'State':
        self.mapping[name] = state
        return self
    
    def move(self, name: str) -> 'State':
        if name in self.mapping:
            self.action.finish()
        return self.mapping.get(name, self)
        
    def execute(self, image: NDArray) -> str | None:
        return self.action(image)


class StateMachine:
    def __init__(self, states: dict[str, State]) -> None:
        self.states = states

    def add_edge(self, from_: str, to_: str, action: str) -> None:
        self.states[from_].add_edge(action, self.states[to_])
