# setting.py
# 2018-03-28
# python3
# ubuntu 64bit 16.04
#
import sys
# must have this append
sys.path.append('/home/tour945/0_ipynb/my_package')
import matplotlib.pyplot as plot
import TransModule2
#
def graphic_area(width, height):
    global tup7
    tup7 = TransModule2.set_graphic_area(width, height)
        
def fig_ax():
    global ax, fig
    fig = plot.figure(figsize=(tup7[0], tup7[1]))
    ax = fig.add_subplot(1,1,1)