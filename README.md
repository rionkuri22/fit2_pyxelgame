# 🐇 Run Rabbit Run

> **Final Project for Fundamentals of Information Technology 2 (FIT2)**  
> **Author:** Rion Kurihara (Policy Management, 1st Year)  
> **Engine / Language:** [Pyxel](https://github.com/kitao/pyxel) (Retro Game Engine for Python) | Python 3  

---

## 📌 Project Overview

**Run Rabbit Run** is a 2D pixel-art arcade survival game developed as the final project for the **Fundamentals of Information Technology 2 (FIT2)** course. The primary focus of the class was mastering core Python programming fundamentals—such as Object-Oriented Programming (OOP), mathematical calculations, state management, and event loops—by building interactive retro games with **Pyxel**.

In *Run Rabbit Run*, the player controls a quick-witted rabbit attempting to evade chasing foxes across increasingly challenging environments.

---

## 🎮 Game Rules & How to Play

### 🎯 Objective
Survive each **30-second round** without getting caught by the fox(es). If the timer hits zero, you clear the level and advance to the next stage!

### 🕹️ Controls

| Action | Control / Key |
| :--- | :--- |
| **Move Rabbit** | `Arrow Keys` or `W` / `A` / `S` / `D` |
| **Activate Edge Teleport** | `Left Mouse Click` on moving border buttons |
| **Select Level (Start Screen)** | `1` (Level 1), `2` (Level 2), `3` (Level 3) |
| **Restart / Continue (End Screen)** | `0` |

### 🏆 Win & Loss Conditions
* **Victory:** Avoid enemy contact until the **30-second countdown** reaches 0.
* **Game Over:** Touched by a fox (enemy collision within 10 pixels). Pressing `0` returns to the start menu.

---

## 🏁 Level Progression

* **Level 1 — The Escape:** 
  * 1 Enemy Fox chasing the player.
  * 7 randomly generated terrain obstacles.
  * Standard full-visibility playfield.
* **Level 2 — Pack Attack:** 
  * 3 Enemy Foxes attacking from multiple corners.
  * 7 randomly generated terrain obstacles.
  * Tests quick reflexes and strategic routing.
* **Level 3 — Dark Night (Torchlight Mode):** 
  * 1 Enemy Fox spawning at the center.
  * Pitch-black arena with a **dynamic torchlight effect** attached to the player.
  * Enemies and obstacles are invisible outside the spotlight radius!

---

## ✨ Standout Technical Features

### 1. 🌀 Dynamic Edge-Warp Portal System (Interactive Border Buttons)
Unlike standard arena games with static screen-wrapping, player wrapping is gated by an interactive mechanic:
* Four border buttons (`left`, `right`, `top`, `bottom`) patrol back and forth along the screen edges (`BUTTON_SPEED = 0.5`).
* Clicking a patrolling button turns it **red**, unlocking a single-use edge warp.
* Stepping off that boundary warps the rabbit to the opposite side of the screen, creating crucial escape routes when cornered by foxes.
* Enemies wrap automatically (`x % SCREEN_WIDTH`), creating asymmetrical movement dynamics between player and chasers.

### 2. 💡 Dynamic Torchlight / Fog of War (Level 3)
* Built using Pyxel drawing primitives without external shader libraries.
* Clears the canvas in pitch black (`COLOR_BLACK`) and draws concentric yellow radial gradients (`pyxel.circ`) centered on the player (`torchlight_radius = 40`).
* Render distance check: Enemies and obstacles calculate Euclidean distance to the player and are rendered **only** when within the torchlight radius (`dist <= torchlight_radius`).

### 3. 🎯 Euclidean Vector Chasing AI
* Enemy tracking calculates distance components `(dx, dy)` between the fox and rabbit each frame.
* Uses Pythagorean theorem (`math.sqrt(dx^2 + dy^2)`) to construct normalized directional unit vectors multiplied by `ENEMY_SPEED (0.9)`.
* Ensures smooth, realistic chase angles rather than simple grid-axis movement.

### 4. 🎲 Procedural Safe-Spawn Obstacle Generator
* Obstacle positions and sprite variations (4 unique designs) are generated randomly per round using `random.randint()`.
* Implements distance validation (`abs(obstacle - player_start) >= min_distance (20px)`) to guarantee the rabbit never spawns trapped inside or adjacent to obstacles.

### 5. 🏗️ Robust Object-Oriented Architecture & State Machine
* Clean separation of concerns with entity classes (`Player`, `Enemy`, `Button`, `Obstacle`) managing coordinate state and design parameters.
* Finite State Machine (`"start"` → `"playing"` → `"end"`) cleanly governing game loop updates, input handlers, frame timer conversions (60 FPS → 30 seconds), and conditional rendering routines.

---

## 🛠️ Code Architecture

```
run.rabbit.run copy.py
├── Player                         # Manages player position & movement limits
├── Enemy                          # Manages fox coordinates & screen wrapping
├── Button                         # Manages edge portal position, direction & click state
├── Obstacle                       # Manages static terrain placement & sprite coords
└── Game                           # Central controller (Pyxel engine, loop, states, rendering)
    ├── init / reset()             # State initialization & level setup
    ├── generate_obstacles()       # Procedural placement with safety radius
    ├── update() / update_playing()# Input handling, vector AI, collision & timer
    ├── move_player() / move_enemy()# Collision detection & warp portal logic
    ├── update_buttons()           # Border patrol physics & mouse click detection
    └── draw() / draw_level_3()    # Rendering engine & torchlight lighting mask
```

---

## 🚀 How to Run

### Prerequisites
Make sure Python 3 is installed along with `pyxel`:

```bash
pip install pyxel
```

### Launching the Game
Run the python script directly from the project directory:

```bash
python "run.rabbit.run copy.py"
```

*(Note: Ensure `IMAGES.pyxres` is present in the same working directory for custom pixel art assets to load properly.)*

---

## 🏫 Class Context

Developed for **Fundamentals of Information Technology 2 (FIT2)**  
*Final Project Presentation & Design Document by Rion Kurihara (ID: 72335117)