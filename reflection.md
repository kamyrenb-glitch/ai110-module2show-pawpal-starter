# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design includes four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores the owner’s name and manages multiple pets. The Pet class stores each pet’s name, age, weight, height, medications, allergies, diagnoses, and health history. The Task class represents one-time or recurring care tasks and stores information such as the task name, duration, priority, and frequency. The Scheduler class creates a basic schedule using the pet’s profile and the tasks added by the owner. It also automatically creates recurring medication tasks based on how often the medication is needed, similar to a recurring Teams meeting or Apple Calendar event. If tasks conflict, the Scheduler alerts the owner and prioritizes the pet’s health needs.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

I kept the current pairwise conflict-detection method because it is easier to read and correctly checks every possible overlap. The AI suggested an active-task approach and described it as O(n log n), but I noticed it could still become O(n²) when many tasks overlap because it repeatedly scans the active list. Since PawPal works with a small daily task list, I chose readability and reliable behavior over added complexity.

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
