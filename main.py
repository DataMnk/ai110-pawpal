"""Demo script for PawPal+ scheduling and conflict detection."""

from __future__ import annotations

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    today = "2026-03-27"

    # Two pets
    buddy = Pet(name="Buddy", age=4, breed="Golden Retriever", health_conditions=["mild arthritis"])
    whiskers = Pet(name="Whiskers", age=2, breed="Domestic Shorthair", health_conditions=[])

    owner = Owner(name="Alex Rivera", pets=[buddy, whiskers])

    # Buddy: morning walk, evening meal prep
    buddy.add_task(
        Task(
            name="Morning walk (30 min)",
            duration=30,
            time="07:30",
            frequency="daily",
            priority="high",
            due_date=today,
            pet_name=buddy.name,
        )
    )
    buddy.add_task(
        Task(
            name="Evening feeding - kibble + joint supplement",
            duration=15,
            time="18:00",
            frequency="daily",
            priority="high",
            due_date=today,
            pet_name=buddy.name,
        )
    )

    # Whiskers: insulin + play - conflict: two tasks at 08:00
    whiskers.add_task(
        Task(
            name="Insulin injection (breakfast dose)",
            duration=10,
            time="08:00",
            frequency="daily",
            priority="high",
            due_date=today,
            pet_name=whiskers.name,
        )
    )
    whiskers.add_task(
        Task(
            name="Interactive play session",
            duration=20,
            time="08:00",
            frequency="daily",
            priority="medium",
            due_date=today,
            pet_name=whiskers.name,
        )
    )

    # Additional task at a different time (litter / third distinct time)
    whiskers.add_task(
        Task(
            name="Litter box scoop + refresh",
            duration=10,
            time="12:30",
            frequency="daily",
            priority="medium",
            due_date=today,
            pet_name=whiskers.name,
        )
    )

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()
    conflicts = scheduler.detect_conflicts(scheduler.get_all_tasks())

    print("=" * 56)
    print("Today's Schedule")
    print(f"  Owner: {owner.name}  |  Date: {today}")
    print("=" * 56)

    for task in schedule:
        status = "done" if task.is_complete else "pending"
        print(
            f"  {task.time}  |  {task.pet_name:10}  |  {task.name}  "
            f"({task.duration} min, {task.priority})  [{status}]"
        )

    print()
    print("-" * 56)
    print("Detected conflicts (same start time)")
    print("-" * 56)

    if not conflicts:
        print("  None — no overlapping start times.")
    else:
        by_time: dict[str, list] = {}
        for t in conflicts:
            by_time.setdefault(t.time, []).append(t)
        for time_key in sorted(by_time.keys(), key=lambda s: (int(s.split(":")[0]), int(s.split(":")[1]))):
            items = by_time[time_key]
            print(f"  {time_key} - {len(items)} tasks:")
            for t in items:
                print(f"    - {t.pet_name}: {t.name}")


if __name__ == "__main__":
    main()
