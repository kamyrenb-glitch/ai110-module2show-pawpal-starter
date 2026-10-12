from datetime import datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

PRIORITY_LEVELS = {"low": 3, "medium": 6, "high": 9}

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Add a Pet.")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="")
    pet_age = st.number_input("Age", min_value=0, step=1, value=1)
    pet_weight = st.number_input("Weight", min_value=0.0, step=0.1, value=1.0)
    pet_height = st.number_input("Height", min_value=0.0, step=0.1, value=1.0)
    submitted = st.form_submit_button("Add pet")

    if submitted:
        pet_name = pet_name.strip()
        if not pet_name:
            st.warning("Please enter a pet name.")
        else:
            duplicate_pet = any(
                existing_pet.name.lower() == pet_name.lower()
                for existing_pet in st.session_state.owner.pets
            )
            if duplicate_pet:
                st.warning(f"A pet named '{pet_name}' already exists.")
            else:
                pet = Pet(
                    name=pet_name,
                    age=int(pet_age),
                    weight=float(pet_weight),
                    height=float(pet_height),
                    medications={},
                    allergies=[],
                    health_history=[],
                    tasks=[],
                )
                st.session_state.owner.add_pet(pet)
                st.success(f"Added pet: {pet.name}")

if st.session_state.owner.pets:
    st.write("Current pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} | Age: {pet.age} | Weight: {pet.weight} | Height: {pet.height}")
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed directly into the scheduler below.")

if not st.session_state.owner.pets:
    st.info("Add a pet before adding tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5, col6 = st.columns(3)
    with col4:
        task_pet_name = st.selectbox("Pet", [pet.name for pet in st.session_state.owner.pets])
    with col5:
        task_category = st.selectbox(
            "Category", ["exercise", "care", "medication", "health", "enrichment"]
        )
    with col6:
        is_scheduled = st.checkbox("Schedule a time", value=True)

    if is_scheduled:
        col7, col8 = st.columns(2)
        with col7:
            task_date = st.date_input("Date")
        with col8:
            task_time = st.time_input("Start time", value=time(8, 0))

    if st.button("Add task"):
        task_pet = next(
            pet for pet in st.session_state.owner.pets if pet.name == task_pet_name
        )
        scheduled_time = datetime.combine(task_date, task_time) if is_scheduled else None
        new_task = Task(
            name=task_title.strip() or "Untitled task",
            pet=task_pet,
            category=task_category,
            duration_minutes=int(duration),
            priority=PRIORITY_LEVELS[priority],
            frequency=None,
            scheduled_time=scheduled_time,
            is_complete=False,
        )
        task_count_before = len(task_pet.tasks)
        task_pet.add_task(new_task)
        if len(task_pet.tasks) == task_count_before:
            st.warning(
                f"{task_pet.name} already has an open task named '{new_task.name}'."
            )
        else:
            st.success(f"Added '{new_task.name}' for {task_pet.name}.")

st.divider()

st.subheader("Today's Schedule")
st.caption("Incomplete tasks across all pets, ordered by scheduled time.")

scheduler = Scheduler(owner=st.session_state.owner)
# generate_medication_tasks() skips any medication task that already exists,
# so Streamlit reruns cannot create duplicates.
scheduler.generate_medication_tasks()

incomplete_tasks = scheduler.filter_tasks(is_complete=False)
sorted_tasks = scheduler.sort_by_time(incomplete_tasks)

if not sorted_tasks:
    st.info("No open tasks yet. Add a pet and a task above to build a schedule.")
else:
    st.table(
        [
            {
                "When": (
                    task.scheduled_time.strftime("%Y-%m-%d %H:%M")
                    if task.scheduled_time is not None
                    else "Unscheduled"
                ),
                "Pet": task.pet.name,
                "Task": task.name,
                "Category": task.category,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
            }
            for task in sorted_tasks
        ]
    )

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        conflict_names = ", ".join(
            f"{task.name} ({task.pet.name})" for task in conflicts
        )
        st.warning(
            f"Schedule conflict: {conflict_names} overlap in time. "
            "Reschedule the lower-priority task — medication and health tasks "
            "should be handled first."
        )
    else:
        st.success("No schedule conflicts detected.")
