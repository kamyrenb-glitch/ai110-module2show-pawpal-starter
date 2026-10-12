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
