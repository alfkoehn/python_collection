# coding=utf-8

__author__      = 'Alf Köhn-Seemann'
__email__       = 'koehn@igvp.uni-stuttgart.de'
__copyright__   = 'University of Stuttgart'
__license__     = 'MIT'

"""
Short script to animate travelling waves. Various scenarios are possible
and then can either be displayed directly or saved into mp4 files using
ffmpeg (look for variable 'fname_plot').
Partly inspired by 
https://dododas.github.io/posts/2021/2021-01-17-matplotlib-waves/
"""

# import standard modules
import matplotlib as mpl
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np

# possible scenarios
# 1: signal with single frequency
# 2: signal with 2 frequencies with v_ph = v_gr
# 3: signal with 2 frequencies with v_ph = 2*v_gr
# 4: signal with 2 frequencies with v_ph = -2*v_gr
# 5: signal with 2 frequencies, one pulse
scenario    = 4

# the horizontal coordinate x can be either interpreted as a wavenumber
# or a frequency
if scenario == 1:
    fname_plot  = 'waves_singleFreq.mp4'
    plot_title  = 'Signal with single frequency'
    dt_plot     = np.pi/100
    n_points    = 100*4
    f   = lambda x: np.sin(x)
elif scenario == 2:
    fname_plot  = 'wave_vph_vgr.mp4'
    plot_title  = r'$v_\mathrm{group} = v_\mathrm{phase}$'
    dt_plot     = np.pi/200
    n_points    = 100*4*2
    f1  = lambda x: np.sin(x)
    f2  = lambda x: np.sin(20*x)
    f   = lambda x: f1(x) * f2(x)
elif scenario == 3:
    fname_plot  = 'wave_vph_2vgr.mp4'
    plot_title  = r'$v_\mathrm{phase} = 2\cdot v_\mathrm{group}$'
    dt_plot     = np.pi/200
    n_points    = 100*4*2
    f1  = lambda x: np.sin(x)
    f2  = lambda x: np.sin(20*x)
    f   = lambda x: f1(x) * f2(x)
elif scenario == 4:
    fname_plot  = 'wave_vph_m2vgr.mp4'
    plot_title  = r'$v_\mathrm{phase} = -2\cdot v_\mathrm{group}$'
    dt_plot     = np.pi/200
    n_points    = 100*4*2
    f1  = lambda x: np.sin(x)
    f2  = lambda x: np.sin(20*x)
    f   = lambda x: f1(x) * f2(x)
elif scenario == 5:
    dt_plot     = np.pi/200
    n_points    = 100*4*2
    f   = lambda x: np.exp(-x**2/2) * np.cos(10*x)
n_frames    = round(2*np.pi/dt_plot * 4)

# comment following line to save into files, using filenames as defined
# in case structure above
fname_plot  = ''

# create x and y data
# note that for the case of very different frequencies, you might want to increase n_points
x           = np.linspace( -np.pi, np.pi, n_points )
y           = f(x)

# initialize the plot
# figsize=(10,6) is optimized for presentation on a 16:9 screen
fig, ax = plt.subplots( figsize = (10,6) )
wave,   = ax.plot(x, y, "-", color='xkcd:blue', linewidth=2 )

# format plot
ax.set_xticks( [-np.pi, -np.pi/2, 0, np.pi/2, np.pi] )
ax.set_xticklabels( (r'$-\pi$', r'$\pi/2$', '0', r'$\pi/2$', r'$\pi$') )
ax.set_yticks( (-1, 0, 1) )
ax.set_xlim( np.amin(x), np.amax(x) )
ax.grid( True )
ax.tick_params( axis='both', which='both', direction='in', top=True, right=True )
ax.tick_params( axis='both', labelsize=18 )
ax.set_title( plot_title, fontsize=20 )

# evolve the wave in time: f(x) -> f(x - ct)
def shift(t, c=1 ):
    if scenario == 1:
        new_y   = f(x - c*t)
    elif scenario == 2:
        new_y   = f1(x - c*t) * f2(x - c*t)
    elif scenario == 3:
        new_y   = f1(x - c*t) * f2(x - 2*c*t)
    elif scenario == 4:
        new_y   = f1(x - c*t) * f2(x + 2*c*t)
    elif scenario == 5:
        new_y   = f(x - c*t)
    wave.set_ydata(new_y)
    return(wave,)

# set-up animation
anim = anim.FuncAnimation( fig, 
                           shift,           # function to call in each frame
                           fargs=(dt_plot,),# arguments to pass to func 'shift', here dt
                           frames=n_frames, # number of frames iterator produces
                           interval=30,     # delay between frames in ms
                           blit=True        # blitting makes rendering faster for raster graphics
                         )

# display or save animation
if len(fname_plot) > 0:
    anim.save( fname_plot, 
               dpi=150, fps=30,
               writer='ffmpeg'
             )
else:
    plt.show()
