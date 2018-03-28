# setting.py
# 2018-03-28
# python3
# ubuntu 64bit 16.04
#
import matplotlib.pyplot as plot
import ArtPython.TransModule3
#
def graphic_area(width, height):
    global tup7
    tup7 = TransModule3.set_graphic_area(width, height)
        
def fig_ax():
    global ax, fig
    fig = plot.figure(figsize=(tup7[0], tup7[1]))
    ax = fig.add_subplot(1,1,1)