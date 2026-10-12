"""PawPal+ class skeletons.

Generated from diagrams/uml.mmd. Method bodies are intentionally unimplemented.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


class Owner:
    """A pet owner who manages pets and declares when they are available."""

    def __init__(
        self,
        name: str,
        availability: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        self.name: str = name
        self.availability: Dict[str, List[str]] = availability or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        raise NotImplementedError

    def remove_pet(self, pet_name: str) -> bool:
        """Remove the named pet. Return True if a pet was removed."""
        raise NotImplementedError

    def update_availability(self, day: str, time_slots: List[str]) -> None:
        """Replace the available time slots for a single day."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet, its health profile, and the tasks it owns.

    medications maps a medication name to its frequency, e.g. {"insulin": "daily"}.
    """

    name: str
    age: int
    weight: float
    height: float
    medications: Dict[str, str] = field(default_factory=dict)
    allergies: List[str] = field(default_factory=list)
    health_history: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def update_health_profile(self, field_name: str, value: Any) -> None:
        """Update one field of this pet's health profile."""
        raise NotImplementedError

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet. Pet owns and stores its tasks."""
        raise NotImplementedError

    def remove_task(self, task_name: str) -> bool:
        """Remove the named task. Return True if a task was removed."""
        raise NotImplementedError


@dataclass
class Task:
    """A single care task belonging to one pet.

    frequency is None for one-time tasks; category marks health tasks,
    e.g. "medication".
    """

    name: str
    pet: Pet
    category: str
    duration_minutes: int
    priority: int
    frequency: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    is_complete: bool = False

    def update_task(self, field_name: str, value: Any) -> None:
        """Update one field of this task."""
        raise NotImplementedError

    def mark_complete(self) -> None:
        """Mark this task as done."""
        raise NotImplementedError

    def is_recurring(self) -> bool:
        """Return True when frequency is not None."""
        raise NotImplementedError


class Scheduler:
    """Builds a daily plan from the owner's availability and each pet's tasks.

    Reaches pets and tasks through owner.pets and pet.tasks; stores only
    daily_plan.
    """

    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner
        self.daily_plan: List[Task] = []

    def generate_medication_tasks(self) -> List[Task]:
        """Build Task objects from each pet's medications dict."""
        raise NotImplementedError

    def prioritize_tasks(self) -> List[Task]:
        """Order tasks: medication first, then priority, then duration."""
        raise NotImplementedError

    def detect_conflicts(self) -> List[Task]:
        """Return tasks whose scheduled times overlap."""
        raise NotImplementedError

    def alert_owner(self, conflicts: List[Task]) -> str:
        """Build a message describing the conflicts for the owner."""
        raise NotImplementedError

    def generate_daily_plan(self) -> List[Task]:
        """Produce the ordered plan and store it in daily_plan."""
        raise NotImplementedError
