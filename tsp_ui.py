import tkinter as tk
from tkinter import messagebox
import math
import random


# -----------------------------
# TSP Solver: Nearest Neighbor + 2-Opt
# -----------------------------

def euclidean_distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def total_route_distance(route, cities):
    if len(route) <= 1:
        return 0.0
    dist = 0.0
    for i in range(len(route)):
        a = cities[route[i]]
        b = cities[route[(i + 1) % len(route)]]  # wrap around to form a cycle
        dist += euclidean_distance(a, b)
    return dist


def nearest_neighbor_tour(cities, start_index=0):
    n = len(cities)
    if n == 0:
        return []

    unvisited = set(range(n))
    tour = [start_index]
    unvisited.remove(start_index)

    current = start_index
    while unvisited:
        next_city = min(
            unvisited,
            key=lambda j: euclidean_distance(cities[current], cities[j])
        )
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return tour


def two_opt(route, cities):
    """
    Basic 2-opt improvement.
    Tries to improve the route by swapping segments.
    """
    improved = True
    best_route = route[:]
    best_distance = total_route_distance(best_route, cities)

    while improved:
        improved = False
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1:
                    continue  # adjacent edges; skip (no real change)
                new_route = best_route[:]
                new_route[i:j] = reversed(best_route[i:j])
                new_distance = total_route_distance(new_route, cities)
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_route = new_route
                    improved = True
        route = best_route

    return best_route


def solve_tsp(cities):
    """
    High-level solver.
    Returns best route (list of city indices) and total distance.
    """
    n = len(cities)
    if n <= 1:
        return list(range(n)), 0.0

    # Try multiple starting points for a better heuristic result
    best_route = None
    best_distance = float("inf")

    starts_to_try = min(5, n)  # for speed
    start_indices = list(range(n))
    random.shuffle(start_indices)
    start_indices = start_indices[:starts_to_try]

    for start in start_indices:
        route = nearest_neighbor_tour(cities, start)
        route = two_opt(route, cities)
        dist = total_route_distance(route, cities)
        if dist < best_distance:
            best_distance = dist
            best_route = route

    return best_route, best_distance


# -----------------------------
# Tkinter UI
# -----------------------------

class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traveling Salesman Problem Visualizer")

        self.cities = []  # list of (x, y)
        self.city_radius = 6
        self.canvas_width = 800
        self.canvas_height = 600

        self.mode_label_var = tk.StringVar()
        self.mode_label_var.set("Left-click: add city | Right-click: remove city")

        self._build_ui()
        self._bind_events()

    def _build_ui(self):
        # Top info bar
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.info_label = tk.Label(top_frame, textvariable=self.mode_label_var)
        self.info_label.pack(side=tk.LEFT)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.solve_button = tk.Button(btn_frame, text="Solve TSP", command=self.on_solve)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(btn_frame, text="Clear", command=self.on_clear)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.distance_var = tk.StringVar()
        self.distance_var.set("Total distance: -")
        self.distance_label = tk.Label(btn_frame, textvariable=self.distance_var)
        self.distance_label.pack(side=tk.LEFT, padx=20)

        # Canvas
        self.canvas = tk.Canvas(self.root,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _bind_events(self):
        # Left-click to add city
        self.canvas.bind("<Button-1>", self.on_canvas_left_click)
        # Right-click to remove city
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)

    # -------------------------
    # City management
    # -------------------------

    def on_canvas_left_click(self, event):
        x, y = event.x, event.y
        self.cities.append((x, y))
        self._redraw()

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y
        # Find and remove nearest city within radius
        idx_to_remove = None
        for idx, (cx, cy) in enumerate(self.cities):
            if euclidean_distance((x, y), (cx, cy)) <= self.city_radius + 3:
                idx_to_remove = idx
                break

        if idx_to_remove is not None:
            del self.cities[idx_to_remove]
            self._redraw()

    def on_clear(self):
        self.cities = []
        self.distance_var.set("Total distance: -")
        self._redraw()

    # -------------------------
    # Solving & drawing
    # -------------------------

    def on_solve(self):
        if len(self.cities) < 2:
            messagebox.showinfo("Not enough cities", "Add at least 2 cities to solve the TSP.")
            return

        route, dist = solve_tsp(self.cities)
        self.distance_var.set(f"Total distance: {dist:.2f}")
        self._draw_route(route)

    def _redraw(self):
        self.canvas.delete("all")
        self._draw_cities()

    def _draw_cities(self):
        for x, y in self.cities:
            self.canvas.create_oval(
                x - self.city_radius,
                y - self.city_radius,
                x + self.city_radius,
                y + self.city_radius,
                fill="black"
            )

    def _draw_route(self, route):
        self._redraw()
        if not route or len(route) < 2:
            return

        # Draw lines for the route (cycle)
        n = len(route)
        for i in range(n):
            idx_a = route[i]
            idx_b = route[(i + 1) % n]
            x1, y1 = self.cities[idx_a]
            x2, y2 = self.cities[idx_b]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        # Draw cities again on top
        self._draw_cities()


def main():
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
