import matplotlib.pyplot as plt
import random
import mouse_input
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from collections import Counter
from math import floor
import tkinter as tk
from tkinter import filedialog
import os


def read_points_from_file(filename='points.txt'):
    """
    filename: filename of file with points written as "x, y"
    return: list of points of orthogonal polygon
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    points = []
    for line in lines:
        x_str, y_str = line.strip().split(', ')
        x = int(x_str)
        y = int(y_str)
        points.append((x, y))

    return points


def create_random_points(num_points=20):
    """
    function creates file 'random_points.txt' with random points of orthogonal polygone
    num_points: amount of points to generate
    """
    points = []
    current_x = 0
    current_y = 0
    turned = False
    direction = 'vertical'
    num_points -= num_points%2
    
    for i in range(num_points - 1):
        points.append((current_x, current_y))
        
        if current_y >= num_points * 0.5:
            turned = True
            
        if direction == 'vertical':
            if not turned:
                current_y += random.randint(1, 4)
                direction = 'horizontal'
            else:
                current_y -= random.randint(1, 4)
                direction = 'horizontal'
        else:
            current_x += random.randint(1, 5)
            direction = 'vertical'

        if current_y <= 0:
            turned = not turned
            create_random_points(num_points)
            break
    
    points.append((current_x, 0))

    filename = 'random_points.txt'
    with open(filename, 'w') as file:
        for point in points:
            file.write(f"{point[0]}, {point[1]}\n")


def create_polygon_figure(points: list, cameras_points: list):
    """
    points: list of polygon vertices
    cameras_points: list of cameras coordinates
    """
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]
    # Connect the last point with the first point
    x_values.append(x_values[0])
    y_values.append(y_values[0])

    cameras_x_values = [point[0] for point in cameras_points]
    cameras_y_values = [point[1] for point in cameras_points]

    n = len(points)
    # print("all points amount, n = ", n)
    # print("cameras points amount = ", len(cameras_points))
    # print("upper bound for cameras ⌊5n/12⌋+1 = ", floor((5*n)/12)+1)

    plt.figure(figsize=(8, 6))
    plt.scatter(x_values[:], y_values[:], color='blue', label='Points')
    plt.scatter(cameras_x_values, cameras_y_values, color='black', label='Cameras')
    plt.plot(x_values, y_values, color='red', linestyle='-', linewidth=1)
    plt.title('orthogonal prison yard')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()


def delaunay_triangulation(points: list, build_figure=False):
    """
    function executes, builds a triangulation of a given polygon.
    points: a list of polygon points written as "x, y"
    build_figure: builds a triangulation figgure if =True
    return: a list of triangles defined by the corresponding three points.
    """
    tri = Delaunay(points)

    if build_figure:
        plt.triplot([p[0] for p in points], [p[1] for p in points], tri.simplices)
        plt.plot([p[0] for p in points], [p[1] for p in points], 'o')
        plt.title('Delaunay Triangulation')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.show()

    triangles = tri.simplices.tolist()
    triangle_points = [[points[idx] for idx in triangle] for triangle in triangles]
    return triangle_points


def main():
    mode_choice = mode_var.get()

    if mode_choice == '1':
        filename = "points.txt"
    elif mode_choice == '2':
        n = int(entry_points.get())
        create_random_points(n)
        filename = "random_points.txt"
    elif mode_choice == '3':
        mouse_input.create_points()
        filename = "mouse_points.txt"
    
    build_fig = 1 if build_var.get() == 1 else 0

    points = read_points_from_file(filename)
    triangulation_points = delaunay_triangulation(points, build_figure=build_fig) 

    cameras = []
    triangles_without_most_common = triangulation_points[:]
    while triangles_without_most_common:
        all_points = [point for triangle in triangles_without_most_common for point in triangle]
        point_counter = Counter(all_points)
        most_common_point, occurrences = point_counter.most_common(1)[0]
        cameras.append(most_common_point)
        triangles_without_most_common = [triangle for triangle in triangles_without_most_common if most_common_point not in triangle]

    create_polygon_figure(points, cameras)


def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        if os.path.exists(file_path):
            os.replace(file_path, "points.txt")
            status_label.config(text="File uploaded successfully!")
        else:
            status_label.config(text="File does not exist.")
    else:
        status_label.config(text="No file selected.")


if __name__=="__main__":
    root = tk.Tk()
    root.title("Orthogonal Prison Yard")

    mode_var = tk.StringVar()
    mode_var.set('1')

    label = tk.Label(root, text="Choose input mode of points:")
    label.pack()

    modes = [
        ("From file", '1'),
        ("Random input", '2'),
        ("Mouse input", '3')
    ]

    for text, mode in modes:
        tk.Radiobutton(root, text=text, variable=mode_var, value=mode).pack(anchor=tk.W)

    build_var = tk.IntVar()
    build_var.set(0)
    check_button = tk.Checkbutton(root, text="Show triangulation", variable=build_var)
    check_button.pack()

    entry_points_label = tk.Label(root, text="No. of Example Points:")
    entry_points_label.pack()

    entry_points = tk.Entry(root)
    entry_points.pack()


    upload_button = tk.Button(root, text="Upload File", command=upload_file)
    upload_button.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    button = tk.Button(root, text="Select Mode", command=main)
    button.pack()
    root.mainloop()