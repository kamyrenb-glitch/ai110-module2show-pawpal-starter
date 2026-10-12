from datetime import datetime

from pawpal_system import Pet, Task


def test_mark_complete_changes_is_complete_to_true():
    pet = Pet(
        name="Milo",
        age=4,
        weight=18.5,
        height=42.0,
    )
    task = Task(
        name="Morning Walk",
        pet=pet,
        category="exercise",
        duration_minutes=30,
        priority=5,
        frequency=None,
        scheduled_time=None,
        is_complete=False,
    )

    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_pet_add_task_increases_task_count_by_one():
    pet = Pet(
        name="Luna",
        age=2,
        weight=6.8,
        height=24.0,
    )
    task = Task(
        name="Brush Coat",
        pet=pet,
        category="care",
        duration_minutes=20,
        priority=3,
        frequency="weekly",
        scheduled_time=None,
        is_complete=False,
    )

    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
    assert pet.tasks[-1] is task


def test_mark_complete_daily_creates_one_future_task():
    pet = Pet(
        name="Milo",
        age=4,
        weight=18.5,
        height=42.0,
    )
    task = Task(
        name="Insulin",
        pet=pet,
        category="medication",
        duration_minutes=15,
        priority=10,
        frequency="Daily",
        scheduled_time=datetime(2026, 10, 11, 8, 0),
        is_complete=False,
    )
    pet.add_task(task)

    task.mark_complete()

    assert len(pet.tasks) == 2
    assert pet.tasks[1].name == "Insulin"
    assert pet.tasks[1].pet is pet
    assert pet.tasks[1].category == "medication"
    assert pet.tasks[1].duration_minutes == 15
    assert pet.tasks[1].priority == 10
    assert pet.tasks[1].frequency == "Daily"
    assert pet.tasks[1].scheduled_time == datetime(2026, 10, 12, 8, 0)
    assert pet.tasks[1].is_complete is False


def test_mark_complete_weekly_creates_one_future_task():
    pet = Pet(
        name="Luna",
        age=2,
        weight=6.8,
        height=24.0,
    )
    task = Task(
        name="Brush Coat",
        pet=pet,
        category="care",
        duration_minutes=20,
        priority=3,
        frequency="Weekly",
        scheduled_time=datetime(2026, 10, 11, 9, 0),
        is_complete=False,
    )
    pet.add_task(task)

    task.mark_complete()

    assert len(pet.tasks) == 2
    assert pet.tasks[1].name == "Brush Coat"
    assert pet.tasks[1].pet is pet
    assert pet.tasks[1].category == "care"
    assert pet.tasks[1].duration_minutes == 20
    assert pet.tasks[1].priority == 3
    assert pet.tasks[1].frequency == "Weekly"
    assert pet.tasks[1].scheduled_time == datetime(2026, 10, 18, 9, 0)
    assert pet.tasks[1].is_complete is False


def test_mark_complete_twice_does_not_create_another_occurrence():
    pet = Pet(
        name="Milo",
        age=4,
        weight=18.5,
        height=42.0,
    )
    task = Task(
        name="Insulin",
        pet=pet,
        category="medication",
        duration_minutes=15,
        priority=10,
        frequency="daily",
        scheduled_time=datetime(2026, 10, 11, 8, 0),
        is_complete=False,
    )
    pet.add_task(task)

    task.mark_complete()
    first_count = len(pet.tasks)

    task.mark_complete()

    assert len(pet.tasks) == first_count
    assert pet.tasks[-1].name == "Insulin"
    assert pet.tasks[-1].scheduled_time == datetime(2026, 10, 12, 8, 0)
    assert pet.tasks[-1].is_complete is False
