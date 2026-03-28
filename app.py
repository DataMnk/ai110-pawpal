from collections import defaultdict
from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = None
if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False


def _time_sort_key(time_str: str) -> tuple[int, int]:
    parts = time_str.split(":")
    hour = int(parts[0])
    minute = int(parts[1]) if len(parts) > 1 else 0
    return (hour, minute)

st.title("🐾 PawPal+")

# --- Owner ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", placeholder="Your name")

if st.button("Initialize owner", type="primary"):
    if not owner_name.strip():
        st.error("Please enter an owner name.")
    else:
        st.session_state.owner = Owner(name=owner_name.strip())
        st.session_state.schedule_generated = False
        st.success(f"Owner **{owner_name.strip()}** is ready.")
        st.rerun()

owner = st.session_state.owner
if owner is None:
    st.info("Initialize an owner above to add pets and tasks.")
    st.stop()

st.caption(f"Signed in as **{owner.name}**.")

# --- Add pet ---
st.subheader("Pets")
c1, c2, c3 = st.columns(3)
with c1:
    pet_name = st.text_input("Pet name", key="pet_name")
with c2:
    pet_age = st.number_input("Age", min_value=0, max_value=50, value=1, step=1)
with c3:
    pet_breed = st.text_input("Breed", key="pet_breed")

if st.button("Add pet"):
    if not pet_name.strip():
        st.error("Pet name is required.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), age=int(pet_age), breed=pet_breed.strip() or "—"))
        st.rerun()

if owner.pets:
    st.write("**Your pets:**")
    for p in owner.pets:
        st.write(f"- **{p.name}** — age {p.age}, {p.breed} ({len(p.tasks)} task(s))")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add task ---
st.subheader("Tasks")
if not owner.pets:
    st.warning("Add at least one pet before creating tasks.")
else:
    pet_labels = [p.name for p in owner.pets]
    task_pet = st.selectbox("Pet", pet_labels, key="task_pet_select")

    t1, t2 = st.columns(2)
    with t1:
        task_name = st.text_input("Task name", key="task_name")
    with t2:
        task_time = st.text_input("Time (HH:MM)", placeholder="09:30", key="task_time")

    t3, t4 = st.columns(2)
    with t3:
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=24 * 60, value=30)
    with t4:
        task_due = st.date_input("Due date", value=date.today(), key="task_due")

    t5, t6 = st.columns(2)
    with t5:
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
    with t6:
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add task"):
        if not task_name.strip():
            st.error("Task name is required.")
        elif not task_time.strip():
            st.error("Time is required.")
        else:
            pet = next(p for p in owner.pets if p.name == task_pet)
            task = Task(
                name=task_name.strip(),
                duration=int(task_duration),
                time=task_time.strip(),
                frequency=task_frequency,
                priority=task_priority,
                due_date=task_due.isoformat(),
                pet_name=pet.name,
            )
            pet.add_task(task)
            st.rerun()

st.divider()

# --- Schedule ---
st.subheader("Schedule")
scheduler = Scheduler(owner)

if st.button("Generate schedule", type="primary"):
    st.session_state.schedule_generated = True
    st.rerun()

if st.session_state.schedule_generated:
    all_tasks = scheduler.get_all_tasks()
    scheduled = scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts(all_tasks)

    if scheduled:
        st.success(f"{len(scheduled)} task(s) ordered by time.")

    if conflicts:
        by_time: defaultdict[str, list] = defaultdict(list)
        for t in conflicts:
            by_time[t.time].append(t)
        for slot in sorted(by_time.keys(), key=_time_sort_key):
            group = by_time[slot]
            lines = [
                f"**{t.pet_name}** — task **{t.name}** at **{t.time}**"
                for t in group
            ]
            detail = "; ".join(lines)
            st.warning(
                f"**Time conflict at {slot}:** {len(group)} task(s) share this time. {detail} "
                "Consider staggering times so care blocks do not overlap."
            )

    if not scheduled:
        st.info("No tasks to schedule. Add tasks to your pets first.")
    else:
        rows = []
        for i, t in enumerate(scheduled, start=1):
            rows.append(
                {
                    "#": i,
                    "Time": t.time,
                    "Task": t.name,
                    "Pet": t.pet_name,
                    "Duration (min)": t.duration,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                    "Due": t.due_date,
                }
            )
        st.dataframe(rows, use_container_width=True, hide_index=True)

        st.subheader("Filter tasks")
        fp1, fp2 = st.columns(2)
        with fp1:
            pet_filter_options = ["All pets"] + [p.name for p in owner.pets]
            filter_pet = st.selectbox("Pet", pet_filter_options, key="schedule_filter_pet")
        with fp2:
            filter_status = st.selectbox(
                "Completion status",
                ["All", "Pending", "Completed"],
                key="schedule_filter_status",
            )

        pet_all = filter_pet == "All pets"
        status_all = filter_status == "All"

        if pet_all and status_all:
            st.caption("Select a pet and/or completion status to narrow the list below.")
            filtered: list = []
        elif pet_all:
            crit = "pending" if filter_status == "Pending" else "complete"
            filtered = scheduler.filter_tasks(crit)
        elif status_all:
            filtered = scheduler.filter_tasks(filter_pet)
        else:
            crit = "pending" if filter_status == "Pending" else "complete"
            by_pet = scheduler.filter_tasks(filter_pet)
            by_stat = scheduler.filter_tasks(crit)
            filtered = [t for t in by_pet if t in by_stat]

        if not (pet_all and status_all):
            filtered_sorted = scheduler.sort_by_time(filtered)
            if not filtered_sorted:
                st.info("No tasks match your filters.")
            else:
                filter_rows = []
                for i, t in enumerate(filtered_sorted, start=1):
                    filter_rows.append(
                        {
                            "#": i,
                            "Time": t.time,
                            "Task": t.name,
                            "Pet": t.pet_name,
                            "Duration (min)": t.duration,
                            "Priority": t.priority,
                            "Frequency": t.frequency,
                            "Due": t.due_date,
                        }
                    )
                st.dataframe(filter_rows, use_container_width=True, hide_index=True)
