# Description: This script generates a 3D model of a camera gantry.
# The following command is for use inside cq-editor:
# update the path with to the location of the script
# exec( open('/media/manu/manuLinux/code/sources.yguel/3D_modeling/cadquery/ros2_course_mobile_camera/scanbot.py').read() )

import math as m
from importlib import reload
import os

script_path = os.path.abspath(__file__)
current_path = os.path.dirname(script_path)

import sys
sys.path.append(current_path)

# import cam_portique__parameters
# reload(cam_portique__parameters)
# from cam_portique__parameters import *

import cq_utils
reload(cq_utils)
from cq_utils import *

import numpy as np
import scipy.spatial.transform as stf

# Warning view_trough cut the object in 2 parts
view_through = False
export_stl_step = True
SEE_HALF = False
export_tol = 0.001


# ==============================
#  Computed geometric dimensions
# ==============================

plate_depth = 20 # mm
plate_side = 1000 # mm

rail_length = 0.8*plate_side
rail_width = 80 # mm
rail_height = 40 # mm

rails_outer_spacing = plate_side - rail_width
y_center_r1 = -rails_outer_spacing/2 + rail_width/2
y_center_r2 = rails_outer_spacing/2 - rail_width/2

pillar_side = 60 # mm
pillar_height = 500 # mm

h_arch_width = rails_outer_spacing - 20 # mm
h_arch_height = 100 # mm
h_arch_thickness = 30 # mm
z_arch = pillar_height + rail_height - h_arch_height

X_cyl_radius = 40 # mm
X_cyl_height = 20 # mm

z_leg_height = pillar_height
z_leg_width = 2*X_cyl_radius - 10 # mm
z_leg_thickness = 20 # mm

ankle_side = 60 # mm
ankle_thickness = 40 # mm

cam_width = 70 # mm
cam_height = 50 # mm
cam_thickness = 20 # mm

cam_obj_rad = 0.75*cam_height/2
cam_obj_height = 25 # mm

Y_cyl_radius = 0.9*ankle_side/2
Y_cyl_height = X_cyl_radius

toe_side = 2*0.8*Y_cyl_radius

Z_cyl_radius = 0.9*toe_side/2
Z_cyl_height = 0.8*Y_cyl_height

z_leg_x_v = z_leg_thickness+X_cyl_height+h_arch_thickness/2

x_cyl2_z_v = X_cyl_radius+rail_height

ankle_x_v = z_leg_x_v + X_cyl_height

y_cyl_x_v = ankle_x_v + ankle_side/2

toe_x_v = y_cyl_x_v - toe_side/2
toe_y_v = ankle_thickness/2+Y_cyl_height + toe_side/2
z_cyl_z_v = x_cyl2_z_v + toe_side/2

cam_x_v = y_cyl_x_v + cam_thickness/2
cam_y_v = toe_y_v
cam_z_v = x_cyl2_z_v + Z_cyl_height + toe_side/2 + cam_height/2


####################################
####################################
# ACTUAL CODE
####################################



def base_plate():
    """
    Create a plate.
    Origin is at the center of the plate, on top of the plate.
    """
    # box produces a 3D rectangle with given dimensions, with origin at the center of the box
    # translate to move the origin to the top of the box
    return cq.Workplane("XY").box(plate_side, plate_side, plate_depth).translate((0, 0, -plate_depth/2))

def rail():
    """
    Create a rail.
    Origin is at the center of the rail, on bottom of the rail.
    """
    return cq.Workplane("XY").box(rail_length, rail_width, rail_height).translate((0, 0, rail_height/2))


def base_link():
    plate = base_plate()
    r1 = rail().translate((0, -plate_side/2+rail_width, 0))
    r2 = rail().translate((0, plate_side/2-rail_width, 0))
    return plate.union(r1).union(r2)

base_link_view = base_link

def pillar():
    """
    Create a pillar.
    Origin is at the center of the pillar, on bottom of the pillar.
    """
    return cq.Workplane("XY").box(pillar_side, pillar_side, pillar_height).translate((0, 0, pillar_height/2))
    

def arch():
    """
    Create an arch that will moves on the rails.
    """
    p1 = pillar().translate((0, y_center_r1, rail_height))
    p2 = pillar().translate((0, y_center_r2, rail_height))

    
    # Create the horizontal arch
    # Set its origin to the center of the arch, on the bottom of the arch, centered.
    arch = cq.Workplane("XY").box(h_arch_thickness, h_arch_width, h_arch_height).translate((0, 0, z_arch+h_arch_height/2))

    return arch.union(p1).union(p2)

def gauntry():
    return arch()

gauntry_view = gauntry

def X_cyl():
    """
    Create a cylinder for rotation along axe x
    Origin is at the center of the cylinder, on bottom of the cylinder.
    """
    return cq.Workplane("YZ").circle(X_cyl_radius).extrude(X_cyl_height)

def X_cyl_view():
    return X_cyl().translate((h_arch_thickness/2, 0, z_arch + h_arch_height/2))

def z_leg():
    """
    Create a leg that will moves the camera up and down.
    Origin is at the center of the leg in y, on bottom of the leg in z and on top of the leg in x.
    """
    return cq.Workplane("XY").box(z_leg_thickness, z_leg_width, z_leg_height).translate((-z_leg_thickness/2, 0, z_leg_height/2))

def z_leg_view():
    return z_leg().translate((z_leg_x_v, 0, rail_height))

def X_cyl2_view():
    cyl2 = X_cyl()
    return cyl2.translate((z_leg_x_v, 0, x_cyl2_z_v))

def ankle():
    """
    Create an ankle to attach the before the last revolute joint.
    Origin is at the center of the ankle, on bottom (YZ plane) of the ankle.
    """
    return cq.Workplane("ZX").box(ankle_side,ankle_side, ankle_thickness).translate((ankle_side/2, 0, 0))

def ankle_view():
    return ankle().translate((ankle_x_v, 0, x_cyl2_z_v))

def Y_cyl():
    """
    Create a cylinder for rotation along axe y
    Origin is at the center of the cylinder, on bottom of the cylinder.
    """
    return cq.Workplane("ZX").circle(Y_cyl_radius).extrude(Y_cyl_height)

def Y_cyl_view():
    return Y_cyl().translate((y_cyl_x_v, ankle_thickness/2, x_cyl2_z_v))

def toe():
    """
    Create a toe to attach the last revolute joint
    """
    return cq.Workplane("ZX").box(toe_side, toe_side, toe_side).translate((toe_side/2, 0, 0))

def toe_view():
    return toe().translate((toe_x_v, toe_y_v, x_cyl2_z_v))

def Z_cyl():
    """
    Create a cylinder for rotation along axe z
    Origin is at the center of the cylinder, on bottom of the cylinder.
    """
    return cq.Workplane("XY").circle(Z_cyl_radius).extrude(Z_cyl_height)

def Z_cyl_view():
    return Z_cyl().translate((y_cyl_x_v, toe_y_v, z_cyl_z_v))

def camera():
    """
    Create a camera.
    Origin is at the center of the camera, on bottom of the camera.
    """
    box = cq.Workplane("XY").box(cam_height, cam_width, cam_thickness).translate((0, 0, -cam_thickness/2))
    cyl = cq.Workplane("XY").circle(cam_obj_rad).extrude(cam_obj_height)
    return box.union(cyl)

def camera_view():
    return camera().rotate((0, 0, 0), (0, 1, 0), 90).translate((cam_x_v, cam_y_v, cam_z_v))

full_model_info = [
    {
        "name": "base_link",
        "gen": base_link_view,
        "color": "gray",
        "export": True,
        "display": True
    },
    {
        "name": "gauntry",
        "gen": gauntry_view,
        "color": "blue",
        "export": True,
        "display": True
    },
    {
        "name": "X_cyl",
        "gen": X_cyl_view,
        "color": "red",
        "export": True,
        "display": True
    },
    {
        "name": "z_leg",
        "gen": z_leg_view,
        "color": "green",
        "export": True,
        "display": True
    },
    {
        "name": "X_cyl2",
        "gen": X_cyl2_view,
        "color": "red",
        "export": False,
        "display": True
    },
    {
        "name": "ankle",
        "gen": ankle_view,
        "color": "yellow",
        "export": False,
        "display": True
    },
    {
        "name": "Y_cyl",
        "gen": Y_cyl_view,
        "color": "red",
        "export": True,
        "display": True
    },
    {
        "name": "toe",
        "gen": toe_view,
        "color": "yellow",
        "export": True,
        "display": True
    },
    {
        "name": "Z_cyl",
        "gen": Z_cyl_view,
        "color": "red",
        "export": True,
        "display": True
    },
    {
        "name": "camera",
        "gen": camera_view,
        "color": "purple",
        "export": True,
        "display": True
    }
]


if (export_stl_step):
    import os
    from cadquery import exporters
    ex_path = os.path.join(current_path, "exports", "models")

    if not os.path.exists(ex_path):
        os.makedirs(ex_path)

    sol_pfx = "cam_gauntry" + "_"

    base_link_base_file_name = sol_pfx + "base_link"
    gauntry_link_base_file_name = sol_pfx + "gauntry_link"
    x_cyl_link_base_file_name = sol_pfx + "x_cyl_link"
    z_leg_link_base_file_name = sol_pfx + "z_leg_link"
    ankle_link_base_file_name = sol_pfx + "ankle_link"
    y_cyl_link_base_file_name = sol_pfx + "y_cyl_link"
    toe_link_base_file_name = sol_pfx + "toe_link"
    z_cyl_link_base_file_name = sol_pfx + "z_cyl_link"
    camera_link_base_file_name = sol_pfx + "camera_link"

    file_names = [
        base_link_base_file_name,
        gauntry_link_base_file_name,
        x_cyl_link_base_file_name,
        z_leg_link_base_file_name,
        ankle_link_base_file_name,
        y_cyl_link_base_file_name,
        toe_link_base_file_name,
        z_cyl_link_base_file_name,
        camera_link_base_file_name,
    ]

    gen_funcs = [
        base_link,
        gauntry,
        X_cyl,
        z_leg,
        ankle,
        Y_cyl,
        toe,
        Z_cyl,
        camera
    ]

    models = []
    for i in range(0, len(file_names)):
        d = {
            "file_name": file_names[i],
            "gen_f": gen_funcs[i]
        }
        models.append(d)

    for item in models:
        f_name = item["file_name"]
        gen_f = item["gen_f"]

        # STL
        stl_full_file_name = os.path.join(ex_path, f_name + ".stl")
        exporters.export(
            gen_f(), stl_full_file_name, exportType=exporters.ExportTypes.STL, tolerance=export_tol)

        # STEP
        step_full_file_name = os.path.join(ex_path, f_name + ".step")
        exporters.export(
            gen_f(), step_full_file_name, exportType=exporters.ExportTypes.STEP, tolerance=export_tol)

if SEE_HALF:
    cut_side = 1000
    cut_cube = cq.Workplane("XY").box(
        cut_side, cut_side, cut_side, centered=True).translate((0, cut_side / 2, 0))


for mod in full_model_info:
    if mod["display"]:
        if SEE_HALF:
            show_object(mod["gen"]().cut(cut_cube), mod["name"],
                        options={"color": mod["color"]})
        else:
            show_object(mod["gen"](), mod["name"],
                        options={"color": mod["color"]})


print("=============")
print(" Cotes utiles")
print("=============")
