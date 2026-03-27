from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    duration: int  # minutes
    time: str  # "HH:MM"
    frequency: str  # daily/weekly/once
    priority: str  # low/medium/high
    is_complete: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    age: int
    breed: str
    health_conditions: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str, pets: List[Pet] | None = None) -> None:
        self.name = name
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        pass

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        pass

    def filter_tasks(self, criteria: str) -> List[Task]:
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        pass

    def generate_schedule(self) -> List[Task]:
        pass
