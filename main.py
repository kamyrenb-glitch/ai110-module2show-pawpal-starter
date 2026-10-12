from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def format_time(task_time):
    return task_time.strftime("%Y-%m-%d %H:%M") if task_time else "Unscheduled"


def main():
    owner = Owner(
        name="Jordan",
        availability={
            "Monday": ["08:00-12:00", "14:00-18:00"],
            "Tuesday": ["09:00-13:00"],
        },
    )

    milo = Pet(
        name="Milo",
        age=4,
        weight=18.5,
        height=42.0,
        medications={"Insulin": "daily"},
        allergies=["Chicken"],
        health_history=["Recovered from ear infection", "Routine bloodwork completed"],
        tasks=[],
    )

    luna = Pet(
        name="Luna",
        age=2,
        weight=6.8,
        height=24.0,
        medications={"Vitamin Supplement": "weekly"},
        allergies=["Wheat"],
        health_history=["Healthy annual checkup", "No current issues"],
        tasks=[],
    )

    owner.add_pet(milo)
    owner.add_pet(luna)

    walk_task = Task(
        name="Morning Walk",
        pet=milo,
        category="exercise",
        duration_minutes=45,
        priority=4,
        frequency=None,
        scheduled_time=datetime(2026, 10, 11, 8, 10),
        is_complete=False,
    )
    milo.add_task(walk_task)

    grooming_task = Task(
        name="Brush Coat",
        pet=luna,
        category="care",
        duration_minutes=20,
        priority=3,
        frequency="weekly",
        scheduled_time=datetime(2026, 10, 11, 9, 0),
        is_complete=False,
    )
    luna.add_task(grooming_task)

    checkup_task = Task(
        name="Luna Follow-up Check",
        pet=luna,
        category="wellness",
        duration_minutes=30,
        priority=6,
        frequency=None,
        scheduled_time=datetime(2026, 10, 11, 8, 10),
        is_complete=False,
    )
    luna.add_task(checkup_task)

    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_daily_plan()

    print("Today's Schedule")
    print("-" * 100)
    for task in daily_plan:
        time_label = format_time(task.scheduled_time)
        frequency_label = task.frequency if task.frequency is not None else "Once"
        print(
            f"{time_label:<18} | Pet: {task.pet.name:<8} | "
            f"Task: {task.name:<22} | Category: {task.category:<12} | "
            f"Duration: {task.duration_minutes:>2} min | "
            f"Frequency: {frequency_label:<8} | "
            f"Priority: {task.priority} | Complete: {'Yes' if task.is_complete else 'No'}"
        )

    print()
    print("Tasks Sorted by Time")
    print("-" * 100)
    sorted_tasks = scheduler.sort_by_time(scheduler.filter_tasks())
    for task in sorted_tasks:
        time_label = format_time(task.scheduled_time)
        print(
            f"{time_label:<18} | Pet: {task.pet.name:<8} | "
            f"Task: {task.name:<22} | Complete: {'Yes' if task.is_complete else 'No'}"
        )

    print()
    print("Incomplete Tasks for Luna")
    print("-" * 100)
    luna_incomplete_tasks = scheduler.filter_tasks(pet_name="Luna", is_complete=False)
    for task in scheduler.sort_by_time(luna_incomplete_tasks):
        time_label = format_time(task.scheduled_time)
        print(
            f"{time_label:<18} | Pet: {task.pet.name:<8} | "
            f"Task: {task.name:<22} | Complete: {'Yes' if task.is_complete else 'No'}"
        )

    conflicts = scheduler.detect_conflicts()
    print()
    print("Schedule Alerts")
    print("-" * 100)
    print(scheduler.alert_owner(conflicts))


if __name__ == "__main__":
    main()
