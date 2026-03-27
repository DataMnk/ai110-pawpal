# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Core user actions:
1. Add a pet with basic information
2. Add care tasks to a pet
3. View a generated daily schedule

This is my initial UML design:
Classes:
- Owner: holds the owner's name and list of pets. Responsible for adding pets.
- Pet: holds pet details and a list of tasks. Responsible for adding tasks.
- Task: represents a single care activity with time, duration, priority, and frequency.
- Scheduler: the brain of the system. Retrieves, sorts, filters, and generates the daily schedule.

**b. Design changes**

After asking Cursor AI to review the class skeletons, two changes were made to Task:

1. Added `due_date` (string "YYYY-MM-DD") — the original design had no way 
   to know when a "once" or "weekly" task should run. Without this, the 
   scheduler couldn't decide if a task belongs to today.

2. Added `pet_name` (string) — when the Scheduler flattens all tasks from 
   all pets into one list, tasks lost their pet identity. This field lets 
   the schedule display "Feed Bella at 08:00" instead of just "Feed at 08:00".

Suggestions rejected for now: changing `time` to datetime.time (too complex 
for this stage), narrowing filter_tasks signature (deferred to Phase 4), 
and changing detect_conflicts return type (deferred to Phase 4).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
