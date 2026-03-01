import tkinter as tk
from tkinter import font as tkfont
import heapq, math, time, random

# --- Grid constants ---
ROWS = 15  # Increased slightly for better visibility
COLS = 15
CELL = 40
PANEL_W = 200
ANIM_DELAY = 1
AGENT_DELAY = 12
OBS_PROB = 0.01

# --- Colour palette ---
CL_PANEL = "#1C2663"
CL_PANEL2 = "#0D121A"
CL_BG = "#0D0007"         # Fixed hex length
CL_GRID = "#1F2D5A"       

CL_WHITE = "#FFFFFF"
CL_OFFWHITE = "#ECF0F1"
CL_MUTED = "#95A5A6"
CL_ACCENT = "#3468CB"
CL_ACCENT2 = "#5DAAE2"
CL_YELLOW = "#F2C40F"
CL_GREEN_LBL = "#2CCC71"
CL_ORANGE = "#E67A22"

# --- Cell colours ---
CL_EMPTY = "#161B12"
CL_WALL = "#2C3E58"
CL_WALL_STK = "#34425E"
CL_START = "#27AE40"
CL_GOAL = "#E74C2C"
CL_VISITED = "#1A3A5C"    # Fixed 'q' typo
CL_PATH = "#247113"
CL_PATH_LINE = "#5DA1E2"
CL_AGENT = "#F39112"
CL_AGENT_RIM = "#F1C10F"

# --- Button palette ---
BTN = {
    "run": ("#27AE61", "#1E8449"),
    "reset": ("#2980B9", "#1F618D"),
    "maze": ("#8E46AD", "#6C3483"),
    "clear": ("#E74C3C", "#CB4335"),
    "start": ("#1ABC9C", "#148F77"),
    "goal": ("#E67E22", "#CA611E"),
}

legend_items = [
    (CL_START, "Start node"),
    (CL_GOAL, "Goal node"),
    (CL_AGENT, "Agent"),
    (CL_WALL, "Wall"),
    (CL_VISITED, "Explored"),
    (CL_PATH, "Final path"),
]

# --- Heuristics ---
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

# --- Grid helpers ---
def make_grid(density=0.0):
    g = [[0]*COLS for _ in range(ROWS)]
    if density > 0:
        for r in range(ROWS):
            for c in range(COLS):
                if random.random() < density:
                    g[r][c] = 1
    return g

def neighbors(pos, grid):
    r, c = pos
    out = []
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 0:
            out.append((nr, nc))
    return out

def rebuild_path(cf, goal):
    path, node = [], goal
    while node is not None:
        path.append(node); node = cf[node]
    path.reverse()
    return path

# --- Search algorithms ---
def run_astar(grid, start, goal, h):
    counter = 0
    g = {start: 0}
    heap = [(h(start, goal), 0, start)]
    cf = {start: None}
    closed = set()
    visited_order = []
    while heap:
        _, _, cur = heapq.heappop(heap)
        if cur in closed: continue
        closed.add(cur)
        visited_order.append(cur)
        if cur == goal:
            return rebuild_path(cf, goal), visited_order, len(visited_order)
        for nb in neighbors(cur, grid):
            ng = g[cur] + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng; cf[nb] = cur; counter += 1
                heapq.heappush(heap, (ng + h(nb, goal), counter, nb))
    return None, visited_order, len(visited_order)

def run_gbfs(grid, start, goal, h):
    counter = 0
    heap = [(h(start, goal), 0, start)]
    cf = {start: None}
    seen = {start}
    visited_order = []
    while heap:
        _, _, cur = heapq.heappop(heap)
        visited_order.append(cur)
        if cur == goal:
            return rebuild_path(cf, goal), visited_order, len(visited_order)
        for nb in neighbors(cur, grid):
            if nb not in seen:
                seen.add(nb); cf[nb] = cur; counter += 1
                heapq.heappush(heap, (h(nb, goal), counter, nb))
    return None, visited_order, len(visited_order)

def run_dijkstra(grid, start, goal, h=None):
    counter = 0
    g = {start: 0}
    heap = [(0, 0, start)]
    cf = {start: None}
    closed = set()
    visited_order = []
    while heap:
        _, _, cur = heapq.heappop(heap)
        if cur in closed: continue
        closed.add(cur)
        visited_order.append(cur)
        if cur == goal:
            return rebuild_path(cf, goal), visited_order, len(visited_order)
        for nb in neighbors(cur, grid):
            ng = g[cur] + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng; cf[nb] = cur; counter += 1
                heapq.heappush(heap, (ng, counter, nb))
    return None, visited_order, len(visited_order)

def run_bfs(grid, start, goal, h=None):
    from collections import deque
    queue = deque([start])
    cf = {start: None}
    visited_order = []
    while queue:
        cur = queue.popleft()
        if cur in visited_order: continue
        visited_order.append(cur)
        if cur == goal:
            return rebuild_path(cf, goal), visited_order, len(visited_order)
        for nb in neighbors(cur, grid):
            if nb not in cf:
                cf[nb] = cur
                queue.append(nb)
    return None, visited_order, len(visited_order)

class PathfinderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent · AI2002")
        self.root.configure(bg=CL_PANEL)
        
        self.alg_var = tk.StringVar(value="A*")
        self.h_var = tk.StringVar(value="Manhattan")
        self.dyn_var = tk.BooleanVar(value=False)
        self.speed_var = tk.IntVar(value=5)

        self.grid = make_grid()
        self.start = (1, 1)
        self.goal = (ROWS-2, COLS-2)
        
        self.path = []; self.path_set = set()
        self.visited_set = set(); self.agent_pos = None
        self.agent_idx = 0; self._vlist = []; self._vidx = 0
        self._drawing = None; self._placing = None
        self._anim_job = None; self._agent_job = None; self._replans = 0

        self.m_nodes = tk.StringVar(value="—")
        self.m_cost = tk.StringVar(value="—")
        self.m_time = tk.StringVar(value="—")
        self.m_replan = tk.StringVar(value="0")
        self.m_status = tk.StringVar(value="Ready · Click/Drag to draw walls")
        self.m_alg_info = tk.StringVar(value="")

        self._build_ui()
        self._full_redraw()

    def _build_ui(self):
        main_frame = tk.Frame(self.root, bg=CL_PANEL)
        main_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(main_frame, width=COLS*CELL, height=ROWS*CELL, bg=CL_BG, highlightthickness=0)
        self.canvas.pack(side="left", padx=10, pady=10)
        
        self.canvas.bind("<Button-1>", self._press)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", lambda _: setattr(self, "_drawing", None))
        
        panel = tk.Frame(main_frame, bg=CL_PANEL, width=PANEL_W)
        panel.pack(side="right", fill="y", padx=10)

        tk.Label(panel, text="Pathfinding AI", fg=CL_WHITE, bg=CL_PANEL, font=("Arial", 12, "bold")).pack(pady=10)
        
        # Alg selection
        for a in ["A*", "GBFS", "Dijkstra", "BFS"]:
            tk.Radiobutton(panel, text=a, variable=self.alg_var, value=a, bg=CL_PANEL, fg=CL_WHITE, selectcolor=CL_ACCENT).pack(anchor="w")

        tk.Button(panel, text="RUN SEARCH", command=self._run, bg=BTN["run"][0], fg="white", relief="flat").pack(fill="x", pady=5)
        tk.Button(panel, text="RESET", command=self._reset, bg=BTN["reset"][0], fg="white", relief="flat").pack(fill="x", pady=2)
        tk.Button(panel, text="CLEAR WALLS", command=self._clear_walls, bg=BTN["clear"][0], fg="white", relief="flat").pack(fill="x", pady=2)
        
        tk.Label(panel, textvariable=self.m_status, wraplength=150, bg=CL_PANEL, fg=CL_GREEN_LBL, font=("Arial", 8)).pack(pady=10)

    def _draw_cell(self, r, c):
        tag = f"cell_{r}_{c}"
        self.canvas.delete(tag)
        x1, y1 = c*CELL, r*CELL
        x2, y2 = x1+CELL, y1+CELL
        
        fill = CL_EMPTY
        if (r,c) == self.start: fill = CL_START
        elif (r,c) == self.goal: fill = CL_GOAL
        elif (r,c) == self.agent_pos: fill = CL_AGENT
        elif self.grid[r][c] == 1: fill = CL_WALL
        elif (r,c) in self.path_set: fill = CL_PATH
        elif (r,c) in self.visited_set: fill = CL_VISITED
        
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=CL_GRID, tags=tag)

    def _full_redraw(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                self._draw_cell(r, c)

    def _press(self, event):
        c, r = event.x // CELL, event.y // CELL
        if 0 <= r < ROWS and 0 <= c < COLS:
            if (r,c) in (self.start, self.goal): return
            self._drawing = (self.grid[r][c] == 0)
            self.grid[r][c] = 1 if self._drawing else 0
            self._draw_cell(r, c)

    def _drag(self, event):
        c, r = event.x // CELL, event.y // CELL
        if 0 <= r < ROWS and 0 <= c < COLS:
            if (r,c) in (self.start, self.goal): return
            self.grid[r][c] = 1 if self._drawing else 0
            self._draw_cell(r, c)

    def _run(self):
        self.visited_set = set()
        self.path_set = set()
        alg = self.alg_var.get()
        h = manhattan if self.h_var.get() == "Manhattan" else euclidean
        
        if alg == "A*": res = run_astar(self.grid, self.start, self.goal, h)
        elif alg == "GBFS": res = run_gbfs(self.grid, self.start, self.goal, h)
        elif alg == "Dijkstra": res = run_dijkstra(self.grid, self.start, self.goal)
        else: res = run_bfs(self.grid, self.start, self.goal)
        
        path, vis, _ = res
        if path:
            self._vlist = vis
            self.path = path
            self._vidx = 0
            self._tick_visited()
        else:
            self.m_status.set("No Path Found!")

    def _tick_visited(self):
        if self._vidx < len(self._vlist):
            node = self._vlist[self._vidx]
            self.visited_set.add(node)
            self._draw_cell(node[0], node[1])
            self._vidx += 1
            self.root.after(10, self._tick_visited)
        else:
            self.path_set = set(self.path)
            for n in self.path: self._draw_cell(n[0], n[1])
            self.m_status.set("Path Found!")

    def _reset(self):
        self.grid = make_grid()
        self.visited_set = set()
        self.path_set = set()
        self.agent_pos = None
        self._full_redraw()

    def _clear_walls(self):
        for r in range(ROWS):
            for c in range(COLS): self.grid[r][c] = 0
        self._reset()

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()