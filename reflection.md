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

The AI features that helped me most were having it read my actual project files instead of guessing at my code, asking it to propose a focused diff before editing anything, having it explain what the code and the tests were doing, and having it run pytest to verify that the changes actually worked. Proposing a diff first mattered the most. It meant I could see exactly what would change, ask questions about it, and reject or adjust parts of it before a single file was touched, rather than finding out afterward.

I also used separate chat sessions for each phase of the project: UML design, implementation, UI wiring, the smarter scheduling algorithms, and testing. Working one phase at a time kept my instructions clearer and kept the AI from carrying assumptions from an earlier phase into a later one. It also made review easier, because each session produced a small, focused set of changes I could read through before approving them.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One suggestion I rejected was replacing my pairwise conflict-detection algorithm with an active-task approach that the AI described as O(n log n). When I worked through what the algorithm actually did, I saw that it repeatedly scans the active list, so it can still degrade to O(n²) when many tasks overlap. The complexity claim was better than the real worst case. Since PawPal works with a small daily task list, the performance difference would not be noticeable either way, so I kept the simpler pairwise method because it is easier to read and correctly checks every possible overlap.

The way I evaluated suggestions generally was to trace the logic myself against the edge cases I cared about instead of accepting the explanation that came with the code. I then confirmed the behavior with tests, including cases like tasks at the exact same time and back-to-back tasks that should not conflict, and ran pytest to see the results rather than assuming the change was correct.

**c. Your role as lead architect**

- What decisions did you own, and what did you delegate to the AI?

I acted as the lead architect on this project. I defined the system's purpose and requirements myself, including supporting multiple pets, recurring care tasks, health-priority warnings, chronological sorting, and conflict detection. The AI helped draft code and tests against those requirements, but it did not decide what PawPal+ should do.

My job was to review every suggestion, question assumptions that were wrong, approve only the edits that fit the design, and make the final call. That included catching a complexity claim that did not hold up, noticing when a proposed change would have quietly removed working UI, and deciding which tradeoffs were right for a small daily task list. The AI moved faster than I could have on my own, but the design decisions stayed mine.

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
