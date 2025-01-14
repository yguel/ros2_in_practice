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

# Create a Plot object that will save to an SVG file
#plot_obj = ig.Plot(svg_file, bbox=(400, 1000), background="white")
#plot_obj = ig.Plot(target=surface, bbox=(800, 1000), background="white")

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
    edges=[(9,8), (8,7), (7,6), (6,5), (5,4), (4,3), (3,2), (2,1), (1,0)],
    directed=True,
)

# Vertex names
g.vs["name"] = [
    "base_link", 
    "gauntry_link", 
    "X_cyl_link", 
    "z_leg_link", 
    "X_cyl2_link", 
    "ankle_link", 
    "Y_cyl_link", 
    "toe_link", 
    "Z_cyl_link", 
    "camera_link"]

# edges names
g.es["name"] = [
    "foot_pitch_joint",
    "toe_fixed_joint",
    "foot_yaw_joint",
    "ankle_fixed_joint",
    "foot_roll_joint",
    "z_slider_joint",
    "leg_fold_joint",
    "y_slider_joint",
    "x_slider_joint",
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
svg_file = "tree_graph.svg"
surface = cairo.SVGSurface(svg_file, 800, 1000)
ctx = cairo.Context(surface)

# Plot and save as SVG
default_palette = getattr(g, "_default_palette", default_palette)
g.__plot__("cairo", ctx, palette = default_palette, **visual_style)

# Create a Plot object that will save to an SVG file
# plot_obj = ig.Plot("example_with_bbox.svg", bbox=(400, 400), background="white")

# ig.plot(
#     g,
#     target=svg_file,
#     **visual_style
# )
# plot_obj.add(g, **visual_style)

# # # Draw the graph so that igraph handles vertices/edges automatically
# plot_obj.redraw()




# def get_layout_bbox(layout, print_bbox=False):
#     """
#     Calculate the bounding box of a layout
#     """
#     coords = np.array(layout.coords)  # Convert to numpy array for easier calculation
#     min_x = coords[:,0].min()
#     max_x = coords[:,0].max()
#     min_y = coords[:,1].min()
#     max_y = coords[:,1].max()
#     minb = (min_x, min_y)
#     maxb = (max_x, max_y)
#     if print_bbox:
#         print(f"Top-left: ({min_x:.2f}, {min_y:.2f})")
#         print(f"Top-right: ({max_x:.2f}, {min_y:.2f})")
#         print(f"Bottom-left: ({min_x:.2f}, {max_y:.2f})")
#         print(f"Bottom-right: ({max_x:.2f}, {max_y:.2f})")
#     return minb, maxb

# mapper = plot_obj.world_coordinate_mapper
# print(mapper)

# # Function to manually transform coordinates
# def transform_coords(x, y, surface_width, surface_height, layout_min, layout_max):
#     """
#     Transform normalized coordinates (-1 to 1) to surface coordinates
#     """
#     # Calculate the available space for the plot
#     available_width = surface_width
#     available_height = surface_height

#     # Calculate the layout properties
#     layout_width = layout_max[0] - layout_min[0]
#     layout_height = layout_max[1] - layout_min[1]

#     # Scale factor (use the bigger dimension to maintain aspect ratio)
#     if layout_width > layout_height:
#         scale = available_width / layout_width
#     else:
#         scale = available_height / layout_height
    
#     # Transform coordinates:
#     # 1. Scale from layout coordinates to actual size
#     # 2. Shift to center of available space
#     # 3. Add margin
#     surface_x = (x-layout_min[0]) * scale
#     surface_y = (y-layout_min[1]) * scale
    
#     return surface_x, surface_y

# def draw_edge_labels(ctx,layout):
#     # Get the transformation parameters from the plot
#     # The plot automatically calculates these to fit the graph in the drawing area
#     plot_width = plot_obj.width  # Width of the plotting area
#     plot_height = plot_obj.height  # Height of the plotting area

#     # Get the bounding box of the layout
#     layout_min, layout_max = get_layout_bbox(layout)

#     # Manually draw displaced edge labels
#     for edge in g.es:
#         # Find the midpoint in layout coordinates
#         source, target = edge.tuple
#         x_mid = (layout[source][0] + layout[target][0]) / 2
#         y_mid = (layout[source][1] + layout[target][1]) / 2

#         print(x_mid,y_mid)

#         # Transform layout coords -> device coords (SVG coords)
#         tx, ty = transform_coords(x_mid, y_mid, plot_width, plot_height, layout_min, layout_max)

#         print(tx,ty)

#         # Apply displacement offsets
#         offset_x, offset_y = -10, 0
#         dx = tx + offset_x
#         dy = ty + offset_y

#         print(dx,dy)

#         print("\n")

#         # Draw the label using Cairo
#         ctx.set_font_size(14)
#         ctx.set_source_rgb(0, 0, 0)  # black text
#         ctx.move_to(dx, dy)
#         ctx.show_text(edge["name"])

# print(plot_obj.transform)

# # # # Get the underlying Cairo context
# ctx = cairo.Context(surface)
# draw_edge_labels(ctx,layout)

# Save the final result
surface.finish()

print("Graph has been exported as 'tree_graph.svg'.")