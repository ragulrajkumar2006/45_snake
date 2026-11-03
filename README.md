# Snake Game

This project is a terminal-based Snake game using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

---

## What’s Provided

A partially working version of a snake game with:

- Grid-based snake movement controlled by the player
- Food spawning and snake growth
- Score display

You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

---


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Refine Collision Detection

> The snake can die instantly and unfairly if you tap the opposite direction key while moving (e.g. pressing Left while already moving Right), because the new head moves straight into the segment behind it. Investigate and enhance collision accuracy so direction changes and self/wall collisions behave fairly.


### Task 2: Implement Game Over Condition

> Add a screen that displays the final score once the snake hits a wall or itself, then gracefully waits for input instead of just printing to the console.


### Task 3: Add Replay Option

> After Game Over, allow the user to play again by choosing a difficulty (Easy, Medium, or Hard speed), or exit.



### Task 4: Add Sound Feedback

> Add basic sound effects for eating food and for the game-over moment.


---

## Expected Behavior

- Smooth, grid-based snake movement using arrow keys or `WASD`
- Snake grows by one segment each time it eats food
- Food never spawns on top of the snake
- Score updates as food is eaten
- Game ends (and optionally restarts) when the snake hits a wall or itself

---

## Folder Structure

```
snake-main/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── snake.py
│   └── food.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
