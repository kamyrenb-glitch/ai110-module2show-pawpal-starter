from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def make_pet(name):
    """Build a simple pet with no tasks."""
    return Pet(name=name, age=4, weight=18.5, height=42.0)


def make_task(name, pet, scheduled_time=None, duration_minutes=30, is_complete=False):
    """Build a plain one-time task and attach it to its pet."""
    task = Task(
        name=name,
        pet=pet,
        category="care",
        duration_minutes=duration_minutes,
        priority=5,
        frequency=None,
        scheduled_time=scheduled_time,
        is_complete=is_complete,
    )
    pet.add_task(task)
    return task


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


def test_sort_by_time_orders_scheduled_first_and_unscheduled_last():
    owner = Owner(name="Kamyren")
    pet = make_pet("Milo")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    afternoon = make_task("Afternoon Walk", pet, datetime(2026, 10, 11, 14, 0))
    morning = make_task("Morning Walk", pet, datetime(2026, 10, 11, 8, 0))
    anytime = make_task("Refill Water", pet, None)

    unsorted_tasks = [afternoon, morning, anytime]
    sorted_tasks = scheduler.sort_by_time(unsorted_tasks)

    assert [task.name for task in sorted_tasks] == [
        "Morning Walk",
        "Afternoon Walk",
        "Refill Water",
    ]
    assert unsorted_tasks[0] is afternoon
    assert unsorted_tasks[1] is morning
    assert unsorted_tasks[2] is anytime


def test_filter_tasks_incomplete_returns_only_incomplete_tasks():
    owner = Owner(name="Kamyren")
    pet = make_pet("Milo")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    make_task("Morning Walk", pet, datetime(2026, 10, 11, 8, 0))
    make_task("Evening Walk", pet, datetime(2026, 10, 11, 18, 0), is_complete=True)

    incomplete_tasks = scheduler.filter_tasks(is_complete=False)

    assert [task.name for task in incomplete_tasks] == ["Morning Walk"]
    assert all(task.is_complete is False for task in incomplete_tasks)


def test_detect_conflicts_flags_tasks_at_the_exact_same_time():
    owner = Owner(name="Kamyren")
    pet = make_pet("Milo")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    make_task("Bath", pet, datetime(2026, 10, 11, 8, 0), duration_minutes=30)
    make_task("Vet Call", pet, datetime(2026, 10, 11, 8, 0), duration_minutes=30)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 2
    assert sorted(task.name for task in conflicts) == ["Bath", "Vet Call"]


def test_detect_conflicts_ignores_back_to_back_tasks():
    owner = Owner(name="Kamyren")
    pet = make_pet("Milo")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    make_task("Morning Walk", pet, datetime(2026, 10, 11, 8, 0), duration_minutes=30)
    make_task("Breakfast", pet, datetime(2026, 10, 11, 8, 30), duration_minutes=30)

    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_pet_with_no_tasks_returns_empty_results():
    owner = Owner(name="Kamyren")
    pet = make_pet("Milo")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    assert pet.tasks == []
    assert scheduler.filter_tasks(pet_name="Milo") == []
    assert scheduler.filter_tasks(is_complete=False) == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.sort_by_time(pet.tasks) == []
    assert scheduler.generate_daily_plan() == []
    assert scheduler.alert_owner([]) == "No schedule conflicts detected."
