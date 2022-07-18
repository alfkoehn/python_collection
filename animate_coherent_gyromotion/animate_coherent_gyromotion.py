# coding=utf-8

__author__      = 'Alf Köhn-Seemann'
__email__       = 'koehn@igvp.uni-stuttgart.de'
__copyright__   = 'University of Stuttgart'
__license__     = 'MIT'

"""
Short script to animate a group of particles gyrating around a magnetic 
field line, where the magnetic field direction is perpendicular to the
simulation domain. This illustration corresponds to a simplified illustration
of an electron Bernstein waves (use with care in your talks and lectures).
This script was partly inspired by 
https://stackoverflow.com/a/61326526
"""

# import standard modules
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

#fname_plot  = 'movie_EBW_gyration.mp4'
fname_plot  = ""

# radius of gyration movement
r = 3

# function to return coordinates along a circle
def circle(phi, phi_offset, offset_x, offset_y):
    return np.array( [r*np.cos(phi+phi_offset), 
                      r*np.sin(phi+phi_offset)]
                   ) + np.array( [offset_x, offset_y] )

# plot formatting stuff
fig, ax = plt.subplots( figsize = (10,6) )
ax.axis( [-4, 51, -6, 25] )
ax.set_aspect("equal")
ax.axis("off")

# create initial conditions
# number of particles in horizontal direction
n_part_hor  = 8
# number of particles in vertical direction
n_part_vert = 4
# total number of particles
n_part_tot  = n_part_hor*n_part_vert
# coordinate offsets for each particles
phi_offsets = np.linspace(0., (n_part_tot-1.)*np.pi, n_part_tot)
offset_xs   = np.linspace(0., ((n_part_hor-1.)*2*r  + n_part_hor*r/5.),  n_part_hor)
offset_ys   = np.linspace(0., ((n_part_vert-1.)*2*r + n_part_vert*r/5.), n_part_vert)

# draw circles
for ii in range(n_part_hor):
    for jj in range(n_part_vert):
        circle1 = plt.Circle( (offset_xs[ii], 
                               offset_ys[jj]), 
                               r, color='r', fill=False )
        ax.add_patch(circle1)


# create a point in the axes
points  = []
for ii in range(n_part_hor):
    for jj in range(n_part_vert):
        x, y    = circle(0, 
                         phi_offsets[ii + jj*n_part_hor], 
                         offset_xs[ii], 
                         offset_ys[jj] )
        points.append( ax.plot(x, y, marker="o", color="black", markersize=10)[0] )


def update( phi, phi_offset, offset_x, offset_y ):
    # set point coordinates
    for ii in range(n_part_hor):
        for jj in range(n_part_vert):
            x, y    = circle( phi, 
                              phi_offset[ii + jj*n_part_hor], 
                              offset_x[ii], 
                              offset_y[jj] )
            points[ii + jj*n_part_hor].set_data( [x], [y] )
    return points

n_rotations = 4
ani = animation.FuncAnimation( fig, update,
        fargs=(phi_offsets, offset_xs, offset_ys),
        interval=2,
        frames=np.linspace(0, 
                           n_rotations*2*np.pi, 
                           int(round(n_rotations*360/2)), 
                           endpoint=False),
        blit=True
        )

if len(fname_plot) > 0:
    ani.save( fname_plot, 
               dpi=150, fps=30,
               writer='ffmpeg'
             )
else:
    plt.show()
