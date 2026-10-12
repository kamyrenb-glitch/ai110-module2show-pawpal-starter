# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```text
Today's Schedule
----------------------------------------------------------------------------------------------------
Unscheduled        | Pet: Milo     | Task: Milo-Insulin           | Category: medication   | Duration: 15 min | Frequency: daily    | Priority: 10 | Complete: No
Unscheduled        | Pet: Luna     | Task: Luna-Vitamin Supplement | Category: medication   | Duration: 15 min | Frequency: weekly   | Priority: 10 | Complete: No
2026-10-11 08:20   | Pet: Luna     | Task: Luna Follow-up Check   | Category: wellness     | Duration: 30 min | Frequency: Once     | Priority: 6 | Complete: No
2026-10-11 08:10   | Pet: Milo     | Task: Morning Walk           | Category: exercise     | Duration: 45 min | Frequency: Once     | Priority: 4 | Complete: No
2026-10-11 09:00   | Pet: Luna     | Task: Brush Coat             | Category: care         | Duration: 20 min | Frequency: weekly   | Priority: 3 | Complete: No

Schedule Alerts
----------------------------------------------------------------------------------------------------
Conflict alert: Morning Walk, Luna Follow-up Check overlap in the schedule.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## Smarter Scheduling

- Sorting: Scheduler.sort_by_time() sorts scheduled tasks chronologically, places unscheduled tasks last, and uses medication, priority, and duration as tie-breakers.
- Filtering: Scheduler.filter_tasks() filters tasks by pet name and/or completion status.
- Conflict detection: Scheduler.detect_conflicts() checks overlapping time intervals using scheduled time and duration; Scheduler.alert_owner() returns a warning message.
- Recurring tasks: Task.mark_complete() creates the next daily or weekly Task instance using timedelta when a recurring task is completed.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
