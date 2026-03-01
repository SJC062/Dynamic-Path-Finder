#  Dynamic Pathfinding Agent  
### Roll Number: 24F-0594  
### Comprehensive Implementation Report  


---

# 1️ Project Overview

This project presents a comprehensive implementation of the **Dynamic Pathfinding Agent**, a GUI-based application developed using **Python** and **Tkinter**.

The application visualizes four classic search algorithms on a **15x15 grid**, allowing users to:

- Interactively place walls
- Select search algorithms
- Choose heuristics
- Observe animated exploration in real time
- View reconstructed shortest paths

###  Implemented Algorithms
- A* Search
- Greedy Best-First Search (GBFS)
- Dijkstra's Algorithm
- Breadth-First Search (BFS)

---

# 2️ Implementation Logic

---

## 2.1 System Architecture

The system is divided into three logical layers:

### 🔹 Grid & State Layer
- 2D List representing environment (`ROWS x COLS = 15 x 15`)
- `0` → Passable cell
- `1` → Wall / Obstacle

---

### 🔹 Algorithm Layer
Four standalone functions implement search strategies using:

- `heapq` (Priority Queue)
- `collections.deque` (Queue)

---

### 🔹 UI Layer

The `PathfinderApp` class manages:
- Tkinter canvas rendering
- Mouse input events
- Animation loops
- Metric display
- Path reconstruction

---

## 2.2 A* Search

A* is an informed search algorithm defined as:


f(n) = g(n) + h(n)


Where:
- `g(n)` → Cost from start
- `h(n)` → Heuristic estimate to goal

### Implementation Details
- Uses min-heap ordered by `f-cost`
- Tracks `g-cost` in dictionary
- Maintains `came_from` map
- Uses closed set to avoid re-expansion
- Path reconstructed using `rebuild_path()`
- Supports Manhattan & Euclidean heuristics

---

## 2.3 Greedy Best-First Search (GBFS)

GBFS considers only the heuristic:


f(n) = h(n)


### Key Characteristics
- Min-heap ordered by `h(n)`
- Faster in many scenarios
- Not guaranteed optimal
- Uses `seen` set to avoid revisits
- Supports Manhattan & Euclidean heuristics

---

## 2.4 Dijkstra's Algorithm

An uninformed search expanding nodes by cumulative cost.

### Key Characteristics
- Min-heap ordered by `g-cost`
- No heuristic
- Equivalent to A* when `h(n) = 0`
- Guarantees shortest path
- Uniform edge cost = 1

---

## 2.5 Breadth-First Search (BFS)

Level-order search for unweighted graphs.

### Key Characteristics
- Uses `collections.deque`
- FIFO queue
- Explores depth-by-depth
- Guarantees shortest path
- Equivalent to Dijkstra with uniform cost

---

## 2.6 Heuristic Functions

| Heuristic   | Formula | Applicable To | Notes |
|-------------|----------|---------------|--------|
| Manhattan   | \|r1-r2\| + \|c1-c2\| | A*, GBFS | Best for 4-direction movement |
| Euclidean   | √((r1-r2)² + (c1-c2)²) | A*, GBFS | Smoother distance |

---

## 2.7 Animation & Visualization

The `_tick_visited()` method drives animation using:


root.after(delay, callback)

10ms delay per explored node

Explored nodes rendered sequentially

Final path drawn in green


---


 Color Scheme
Element	Color
Start Node	Green
Goal Node	Red
Agent	Orange
Explored Nodes	Dark Blue
Final Path	Bright Green
Walls	Slate Blue
3️ Pros and Cons Analysis
3.1 Algorithm Comparison Table
Algorithm	Optimal?	Complete?	Time Complexity	Space Complexity
A*	Yes (admissible h)	Yes	O(b^d)	O(b^d)
GBFS	No	Yes*	O(b^m)	O(b^m)
Dijkstra	Yes	Yes	O(V log V)	O(V)
BFS	Yes (uniform cost)	Yes	O(b^d)	O(b^d)

* GBFS is complete in finite graphs without cycles when a visited set is maintained.


---



3.2 A* Search
Advantages

Optimal with admissible heuristic

Efficient node expansion

Flexible heuristic selection

Disadvantages

Memory intensive

Performance depends on heuristic

Slower than GBFS when optimality not required


---


3.3 Greedy Best-First Search (GBFS)
Advantages

Very fast in best-case scenarios

Lower memory usage

Quickly reaches visible goal

Disadvantages

Not optimal

Can get trapped in dead ends

Poor worst-case performance

---



3.4 Dijkstra's Algorithm
Advantages

Always optimal

No heuristic required

Works for weighted graphs

Disadvantages

Explores uniformly in all directions

High node expansion

Slower on large open grids

---



3.5 Breadth-First Search (BFS)
Advantages

Simple and predictable

Optimal for unweighted graphs

Always complete

Disadvantages

High memory usage

No heuristic guidance

Large explored region for distant goals

---


4️ Test Cases and Visual Proof

Default Configuration:

Start Node → (1,1)

Goal Node → (13,13)

Grid Size → 15x15
---


4.1 A* Search
 Best Case: Open Grid

No walls

Manhattan heuristic

Minimal explored nodes

Direct optimal path
---
 

 Worst Case: Dense Maze

Walls force long detour

Heuristic initially misleading

Larger explored region

Still optimal path

---

4.2 Greedy Best-First Search
 Best Case: Clear Path

No walls

Rapid goal reach

Minimal exploration

 Worst Case: U-Shaped Trap

Wall blocks greedy direction

Backtracking required

Possibly sub-optimal path

  ---

4.3 Dijkstra's Algorithm
 Best Case: Goal Near Start

Goal at (2,2)

Minimal expansion

  

 Worst Case: Dense Walls

Large expansion region

Explores most accessible grid

---

4.4 Breadth-First Search
 Best Case: Goal at Depth 2

Very limited expansion

Worst Case: Maximum Distance

Goal at (13,13)

Nearly entire grid explored

 
---
5️ Conclusion

This project visually demonstrates the difference between informed and uninformed search strategies.

 Key Findings

A* → Best balance of efficiency and optimality

GBFS → Fastest but sacrifices optimality

Dijkstra → Always optimal but inefficient in large grids

BFS → Simple, predictable, but memory heavy

 Final Observation

A* with Manhattan distance consistently provided:

Lowest explored node count

Optimal path length

Best performance balance
---
 How to Run
python main.py

Requires:

Python 3.x

Tkinter (pre-installed)
