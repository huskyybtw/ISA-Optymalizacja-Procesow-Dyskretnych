import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import random
import math

def plot_tsp_solution(distance, order):
    plt.figure(figsize=(12, 8))
    
    order_x = [city[1] for city in order]
    order_y = [city[2] for city in order]
    order_x.append(order[0][1])
    order_y.append(order[0][2])

    colors = plt.cm.jet(np.linspace(0, 1, len(order_x)-1))
    
    # Roads
    for i in range(len(order_x)-1):
        plt.plot([order_x[i], order_x[i+1]], 
                 [order_y[i], order_y[i+1]], 
                 '--', 
                 color="black", 
                 linewidth=2,
                 zorder=1)
        mid_x = (order_x[i] + order_x[i+1]) / 2
        mid_y = (order_y[i] + order_y[i+1]) / 2
        
        plt.annotate(f"{i+1}", 
                    (mid_x, mid_y),
                    color='black',
                    fontsize=9,
                    fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", alpha=0.8, color = "red"),
                    ha='center', 
                    va='center',
                    zorder=2)
    
    # Cities
    for i, city in enumerate(order):
        plt.scatter(city[1], city[2], c='blue', s=300, zorder=3)
        plt.annotate(f"{i+1}", (city[1], city[2]), 
                    color='white',
                    fontsize=10,
                    fontweight='bold',
                    ha='center', 
                    va='center',
                    zorder=4)
    
    plt.title('TSP Solution - Total Distance: {:.2f}'.format(distance))
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

#saPath = load_file("burma14.tsp")
#calculate_distance, order, _ = calculate_distance_annealing(saPath)
#plot_tsp_solution(calculate_distance, order)

def plot_benchmark_results(results):
    distances = [r['avg_distance'] for r in results]
    times = [r['avg_time'] for r in results]
    labels = [f"T:{r['config']['saTempStart']}, α:{r['config']['saTempAlpha']}, S:{r['config']['steps']}" for r in results]

    x = range(len(results))

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Configurations')
    ax1.set_ylabel('Average Distance', color='tab:blue')
    ax1.bar(x, distances, color='tab:blue', alpha=0.6, label='Avg Distance')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Time (s)', color='tab:red')
    ax2.plot(x, times, color='tab:red', marker='o', label='Avg Time')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.xticks(x, range(len(results)) , rotation=45, ha='right', fontsize=1)  
    plt.title('Benchmark Results for Simulated Annealing Configurations')
    plt.tight_layout()
    plt.show()

def load_file(filename):
    with open(filename, 'r') as file:
        data = []
        found_section = False
        for line in file:
            line = line.strip()
            if not found_section:
                if line == "NODE_COORD_SECTION":
                    found_section = True
            else:
                if line == "EOF":
                    break
                parts = line.split()
                if len(parts) == 3:
                    data.append((int(parts[0]), float(parts[1]), float(parts[2])))
        return data

#print(load_file("burma14.tsp"))

def calculate_distance_random(data):
    random.shuffle(data)
    distance = 0
    order = []
    order.append(data[0])

    for i in range(len(data)):
        if i == 0:
            continue
        dist = ((data[i][1] - order[i-1][1]) ** 2 + (data[i][2] - order[i-1][2]) ** 2) ** 0.5
        order.append(data[i])
        distance += dist
    distance += ((data[0][1] - order[-1][1]) ** 2 + (data[0][2] - order[-1][2]) ** 2) ** 0.5
    return distance, order

def calculate_total_distance(path):
    total = 0
    for i in range(len(path)):
        x1, y1 = path[i][1], path[i][2]
        x2, y2 = path[(i+1) % len(path)][1], path[(i+1) % len(path)][2]
        total += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return total

def calculate_distance(a, b):
    return math.hypot(a[1] - b[1], a[2] - b[2])

def dismantle_crossings(order, total_distance):
    improved = True
    improvements = 0
    improved_order = order[:]

    while improved:
        improved = False
        for i in range(len(improved_order) - 1):
            for j in range(i + 2, len(improved_order)):
                if j == len(improved_order) - 1 and i == 0:
                    continue 

                a, b = improved_order[i], improved_order[i + 1]
                c, d = improved_order[j], improved_order[(j + 1) % len(improved_order)]

                old_dist = calculate_distance(a, b) + calculate_distance(c, d)
                new_dist = calculate_distance(a, c) + calculate_distance(b, d)

                if new_dist < old_dist:
                    improved_order[i + 1: j + 1] = reversed(improved_order[i + 1: j + 1])
                    total_distance = total_distance - old_dist + new_dist
                    improved = True
                    improvements += 1
                    break
            if improved:
                break

    return improved_order, total_distance, improvements
#print(calculate_distance_random(load_file("burma14.tsp")))

def plot_temperature_changes(temperatures):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(temperatures)), temperatures, marker='o', color='blue', label='Temperature')
    plt.title('Temperature Changes During Simulated Annealing')
    plt.xlabel('Step')
    plt.ylabel('Temperature')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()    