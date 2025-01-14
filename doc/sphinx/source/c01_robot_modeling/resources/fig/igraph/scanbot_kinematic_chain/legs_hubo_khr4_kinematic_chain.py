import igraph as ig
from igraph.configuration import Configuration
from igraph.drawing.colors import Palette, palettes

print(ig.__version__)

import numpy as np
import math
import cairo

config = Configuration.instance()
default_palette = config["plotting.palette"]
if not isinstance(default_palette, Palette):
    default_palette = palettes[default_palette]

# Define the custom shape drawer for rounded rectangles
class RoundedRectangleDrawer(ig.drawing.shapes.ShapeDrawer):
    names = ["rounded_rectangle"]  # Specify the shape's name

    @staticmethod
    def draw_path(ctx, center_x, center_y, width, height=None, corner_radius=10):
        if height is None:
            height = width
        radius = min(corner_radius, width / 2, height / 2)
        ctx.new_path()
        ctx.arc(center_x + width / 2 - radius, center_y - height / 2 + radius, radius, -math.pi / 2, 0)
        ctx.arc(center_x + width / 2 - radius, center_y + height / 2 - radius, radius, 0, math.pi / 2)
        ctx.arc(center_x - width / 2 + radius, center_y + height / 2 - radius, radius, math.pi / 2, math.pi)
        ctx.arc(center_x - width / 2 + radius, center_y - height / 2 + radius, radius, math.pi, 3 * math.pi / 2)
        ctx.close_path()
    
    @staticmethod
    def intersection_point(center_x,center_y,source_x,source_y,width,height=None):
        if height is None:
            height = width
        if source_x < center_x - width / 2:
            return center_x - width / 2, center_y
        if source_x > center_x + width / 2:
            return center_x + width / 2, center_y
        if source_y < center_y - height / 2:
            return center_x, center_y - height / 2
        if source_y > center_y + height / 2:
            return center_x, center_y + height / 2
        return source_x, source_y


g = ig.Graph(
    edges=[(1,0), (2,1), (3,2), (4,3), (5,4), (6,5), (7,6), (8,0), (9,8), (10,9), (11,10), (12,11), (13,12), (14,13)],
    directed=True,
)

# Vertex names
g.vs["name"] = [
    "L1_link", #0
    "L2_R_link", #1
    "H1_R_link", #2
    "H2_R_link", #3
    "L3_R_link", #4
    "L4_R_link", #5
    "A1_R_link", #6
    "L5_R_link", #7

    "L2_L_link", #8
    "H1_L_link", #9
    "H2_L_link", #10
    "L3_L_link", #11
    "L4_L_link", #12
    "A1_L_link", #13
    "L5_L_link", #14
    ]

# edges names
g.es["name"] = [
    "right_hip_right_fixed_joint",
    "right_hip_right_yaw_joint",
    "right_hip_right_roll_joint",
    "right_hip_right_pitch_joint",
    "right_knee_pitch_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",

    "left_hip_right_fixed_joint",
    "left_hip_right_yaw_joint",
    "left_hip_right_roll_joint",
    "left_hip_right_pitch_joint",
    "left_knee_pitch_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint"
]

# Choose a layout suitable for trees
layout = g.layout("tree")

# Invert the y-coordinates to flip the tree upside down
for coord in layout:
    coord[1] = -coord[1]

# Assign colors to specific edges
g.es["color"] = "#EED84D" # Yellow  (rgb(238, 216, 77))
# other colors: rgb(255,214,0)

# Register the custom shape drawer
ig.drawing.shapes.ShapeDrawerDirectory.register(RoundedRectangleDrawer)

# Function to calculate vertex size based on label length
def calculate_vertex_size(label, base_size=20, char_width=7):
    return base_size + len(label) * char_width

# Calculate vertex sizes dynamically
vertex_sizes = [calculate_vertex_size(name) for name in g.vs["name"]]

# Define visual style (optional but recommended for better visualization)
visual_style = {
    "layout": layout,
    "vertex_label": g.vs["name"],
    "edge_label": g.es["name"],
    "vertex_shape" : "rounded_rectangle", # Boxes with rounded corners
    "vertex_size": 25, # Dynamically set sizes
    "vertex_width": vertex_sizes, # Dynamically set sizes
    "corner_radius": 10, # Rounded corners
    "vertex_color": "lightblue",
    "vertex_label_color": "black",
    "edge_arrow_size": 0.75,
    "vertex_label_size": 10, # Adjust label size as needed
    "vertex_label_dist": 0, # Center the label
    "bbox": (1000, 800),  # Size of the SVG
    "margin": 100,
}

# SVG file output
svg_file = "hubo_KHR4_legs_tree_graph.svg"
surface = cairo.SVGSurface(svg_file, 2000, 1000)
ctx = cairo.Context(surface)

# Plot and save as SVG
default_palette = getattr(g, "_default_palette", default_palette)
g.__plot__("cairo", ctx, palette = default_palette, **visual_style)


# Save the final result
surface.finish()

print(f"Graph has been exported as {svg_file}.")