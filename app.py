import streamlit as st

from pawpal_system import Owner, Pet, Task

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
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
