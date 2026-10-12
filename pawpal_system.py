"""PawPal+ class skeletons.

Generated from diagrams/uml.mmd. Method bodies are intentionally unimplemented.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class Owner:
    """A pet owner who manages pets and declares when they are available."""

    def __init__(
        self,
        name: str,
        availability: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Create an owner with a name, availability map, and empty pet list."""
        self.name: str = name
        self.availability: Dict[str, List[str]] = availability or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        if pet is None:
            raise ValueError("pet cannot be None")
        if any(existing_pet.name == pet.name for existing_pet in self.pets):
            return
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove the named pet. Return True if a pet was removed."""
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                del self.pets[index]
                return True
        return False

    def update_availability(self, day: str, time_slots: List[str]) -> None:
        """Replace the available time slots for a single day."""
        self.availability[day] = list(time_slots)


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
        allowed_fields = {
            "name",
            "age",
            "weight",
            "height",
            "medications",
            "allergies",
            "health_history",
        }
        if field_name not in allowed_fields:
            raise ValueError(f"Unknown health profile field: {field_name}")
        setattr(self, field_name, value)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet. Pet owns and stores its tasks."""
        if task is None:
            raise ValueError("task cannot be None")
        if task.pet is not self:
            raise ValueError("task must belong to this pet before it can be added")
        if any(existing_task is task for existing_task in self.tasks):
            return
        if any(existing_task.name == task.name for existing_task in self.tasks):
            return
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> bool:
        """Remove the named task. Return True if a task was removed."""
        for index, task in enumerate(self.tasks):
            if task.name == task_name:
                del self.tasks[index]
                return True
        return False


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
        allowed_fields = {
            "name",
            "category",
            "duration_minutes",
            "priority",
            "frequency",
            "scheduled_time",
            "is_complete",
        }
        if field_name not in allowed_fields:
            raise ValueError(f"Unknown task field: {field_name}")
        setattr(self, field_name, value)

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_complete = True

    def is_recurring(self) -> bool:
        """Return True when frequency is not None."""
        return self.frequency is not None


class Scheduler:
    """Builds a daily plan from the owner's availability and each pet's tasks.

    Reaches pets and tasks through owner.pets and pet.tasks; stores only
    daily_plan.
    """

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler bound to an owner and an empty daily plan."""
        self.owner: Owner = owner
        self.daily_plan: List[Task] = []

    def generate_medication_tasks(self) -> List[Task]:
        """Build Task objects from each pet's medications dict."""
        generated_tasks: List[Task] = []
        for pet in self.owner.pets:
            for medication_name, frequency in pet.medications.items():
                task_name = f"{pet.name}-{medication_name}"
                if any(
                    existing_task.name == task_name and existing_task.category == "medication"
                    for existing_task in pet.tasks
                ):
                    continue
                medication_task = Task(
                    name=task_name,
                    pet=pet,
                    category="medication",
                    duration_minutes=15,
                    priority=10,
                    frequency=frequency,
                    scheduled_time=None,
                    is_complete=False,
                )
                pet.add_task(medication_task)
                generated_tasks.append(medication_task)
        return generated_tasks

    def prioritize_tasks(self) -> List[Task]:
        """Order tasks: medication first, then priority, then duration."""
        all_tasks: List[Task] = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return sorted(
            all_tasks,
            key=lambda task: (
                0 if task.category == "medication" else 1,
                -int(task.priority),
                int(task.duration_minutes),
            ),
        )

    def detect_conflicts(self) -> List[Task]:
        """Return tasks whose scheduled times overlap."""
        all_tasks: List[Task] = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)

        conflicts: List[Task] = []
        seen_task_ids = set()

        for index, first_task in enumerate(all_tasks):
            if first_task.scheduled_time is None:
                continue
            for second_task in all_tasks[index + 1 :]:
                if second_task.scheduled_time is None:
                    continue
                if first_task is second_task:
                    continue

                first_end = first_task.scheduled_time + timedelta(
                    minutes=first_task.duration_minutes
                )
                second_end = second_task.scheduled_time + timedelta(
                    minutes=second_task.duration_minutes
                )
                if (
                    first_task.scheduled_time < second_end
                    and second_task.scheduled_time < first_end
                ):
                    for task in (first_task, second_task):
                        task_id = id(task)
                        if task_id not in seen_task_ids:
                            seen_task_ids.add(task_id)
                            conflicts.append(task)
        return conflicts

    def alert_owner(self, conflicts: List[Task]) -> str:
        """Build a message describing the conflicts for the owner."""
        if not conflicts:
            return "No schedule conflicts detected."
        conflict_names = ", ".join(task.name for task in conflicts)
        return f"Conflict alert: {conflict_names} overlap in the schedule."

    def generate_daily_plan(self) -> List[Task]:
        """Produce the ordered plan and store it in daily_plan."""
        self.generate_medication_tasks()
        self.daily_plan = self.prioritize_tasks()
        return self.daily_plan
