
# TransModule3.py
# 2018-03-25
# python3
# ubuntu 64bit 16.04
#
# namespace is important
#
!pip install git+https://github.com/tour945/ArtPython.git
import shapely
import numpy
import ArtPython.setting3
#
# specifying the width and the height of the box in inches
# declare graphics area
#
# here width == height
def set_graphic_area(width,height) :
        
    cm2inch = 1/2.54    # inch per cm
    #
    # define graphic area
    #
    left_margin = 1.0   # cm
    right_margin = 1.0  # cm
    #
    figure_width  = width  # cm , from xmin to xmax
    figure_height = height # cm , from ymin to ymax
    #
    top_margin = 1.0    # cm
    bottom_margin = 1.0 # cm
    #
    box_width = left_margin + figure_width + right_margin   # cm
    box_height = top_margin + figure_height + bottom_margin # cm
    #
    top_value    = 1.0 - top_margin / box_height
    bottom_value = bottom_margin / box_height
    left_value   = left_margin / box_width
    right_value  = 1.0 - right_margin / box_width
    #
    return (box_width*cm2inch,box_height*cm2inch,top_value,bottom_value,left_value,right_value,width)
#
# end of def
#
# 求斜率
#
def slope(p1, p2) :
    if (p2[0] - p1[0]) == 0:
        return 9999
    elif (p2[1] - p1[1]) == 0:
        return 0
    else:
        return (p2[1] - p1[1]) * 1.0 / (p2[0] - p1[0])
    # end of function
#
# 斜率極值處理
#
def y_intercept(slope, p1) :
    if slope == 9999 :
        return p1[0]
    else :
        return p1[1] - 1. * slope * p1[0]
    # end of function
#
# 求兩線段的交點
#
def intersect(line1, line2) :
    min_allowed = 1e-5   # guard against overflow
    big_value = 1e10     # use instead (if overflow would have occurred)
    #
    m1 = slope(line1[0], line1[1])
    b1 = y_intercept(m1, line1[0])
    #
    m2 = slope(line2[0], line2[1])
    b2 = y_intercept(m2, line2[0])
        #
    if m1 == 9999 and m2 == 0 :
        x = line1[0][0]
        y = line2[0][1]
    elif m1 == 0 and m2 == 9999 :
        x = line2[0][0]
        y = line1[0][1]
    elif m1 == -1 and m2 == 9999 :
        x = line2[0][0]
        y = b1 - b2
    elif m1 == 9999 and m2 == -1 :
        x = line1[0][0]
        y = b2 - b1
    elif m1 == 9999 :
        x = line1[0][0]
        y = b1
    elif m2 == 9999 :
        x = line2[0][0]
        y = b2
    elif abs(m1 - m2) < min_allowed :
        x = big_value
        y = m1 * x + b1
    else :
        x = 1.0 * (b2 - b1) / (m1 - m2)
        y = 1.0 * m1 * x + b1
    #
    return (x, y)
    # end of function
#
#  either the intersection_pt returned, or None
#
# -------------------------------------------------------------------------------------
#
# 叫用 intersect 函數, 依回傳的交點, 判斷是否合理
# 若是合理, 回傳交點, 結束函數運算
# 若是4種不合理狀態之一, 回傳 None, 結束函數運算
# In Python, the 'null' object is None
#
def segment_intersect(line1, line2) :
    intersection_pt = intersect(line1, line2)
    #      
    if (line1[0][0] < line1[1][0]) :
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0] :
            print( 'error exit 1' )
            return None
    else :
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0] :
            print( 'error exit 2' )
            return None
    #     
    if (line2[0][0] < line2[1][0]) :
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0] :
            print( 'error exit 3' )
            return None
    else :
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0] :
            print( 'error exit 4' )
            return None
    #
    return intersection_pt
    # end of function
#
##
#
# ex: line = [(10.,10.),(70.,70.)]
#
# 求線段中點
#
def midpoint(line):
    return ((line[0][0] + line[1][0]) / 2.0, (line[0][1] + line[1][1]) / 2.0)
    # end of function
#
# begin of function
#
def drawLine_findSlope (line, str_line_color) :
    line_AB = shapely.geometry.LineString(line)
    xValue, yValue = line_AB.xy
    # plot the line
    setting.ax.plot(xValue, yValue, color=str_line_color, alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
    # Calculate the coefficients. line_p1_p2 is reflection line 
    coefficients = numpy.polyfit(xValue, yValue, 1)
    # coefficients is <class 'numpy.ndarray'>
#
    return coefficients
# end of function
#
def findSlope (line) :
    line_AB = shapely.geometry.LineString(line)
    xValue, yValue = line_AB.xy
    # Calculate the coefficients. line_p1_p2 is reflection line 
    coefficients = numpy.polyfit(xValue, yValue, 1)
    # coefficients is <class 'numpy.ndarray'>
#
    return coefficients
# end of function
#
# begin of function
# p1 is a shapely Point type, ex: point_A = Point(-6,6)
# p2 is reflection line, ex: reflection_line = [(10.,10.),(70.,70.)]
#
def set_reflection_matrix_and_draw_reflection_line(p1,p2) :
    cirA = p1.buffer(0.1)
    x_cirA, y_cirA = cirA.exterior.coords.xy
    setting.ax.fill(x_cirA, y_cirA, color='red', alpha=0.7, zorder=2)
    #
    mbList = drawLine_findSlope(p2, 'black')
    # Print return datatype
    print (type(mbList))# <class 'numpy.ndarray'> a multidimensional, homogeneous array of fixed-size items.
    print (mbList.ndim) # Number of array dimensions
    print (mbList.size) # Number of elements in the array
    print (mbList)
    #
    # Print the findings
    print("Line equation is y = mx + b")
    print ('m =', mbList[0])
    print ('b =', mbList[1])
    print("Line solution is y = {m}x + {b}".format(m=str(mbList[0]) + ' ',b=round(mbList[1],8)))
    #
    # algorithm 1 for reflecting a geometry unit across a line
    # http://planetmath.org/derivationof2dreflectionmatrix
    # line slope method --> We set m=tanθ to be the slope of the line of reflection
    # the reflection matrix for reflection about a line of slope m
    # matrix 與單純的一個數字(稱為 scalar 純量c) 可以相乘
    #
    m = mbList[0]
    b = round(mbList[1],8)
    c = 1/(m**2 + 1)    # 純量c
    # algorithm 1 : here we define a 2D reflection matrix
    reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), 0, 0]
    ref_A = shapely.affinity.affine_transform(p1, reflection_matrix)
    B1 = (ref_A.x, ref_A.y)
    cirB1 = shapely.geometry.Point(B1[0],B1[1]).buffer(0.1)
    x_cirB1, y_cirB1 = cirB1.exterior.coords.xy
    setting.ax.fill(x_cirB1, y_cirB1, color='green', alpha=0.7, zorder=2)
    #
    # for reflecting a point A across a line
    # https://stackoverflow.com/questions/3306838/algorithm-for-reflecting-a-point-across-a-line
    # algorithm 2 : only for a Point
    d = (p1.x + (p1.y - b)*m) / (1 + m**2)
    B2 = (2*d - p1.x, 2*d*m - p1.y + 2*b)
    cirB2 = shapely.geometry.Point(B2[0],B2[1]).buffer(0.1)
    x_cirB2, y_cirB2 = cirB2.exterior.coords.xy
    setting.ax.fill(x_cirB2, y_cirB2, color='blue', alpha=0.7, zorder=2)
    #
    print ('A  = ',round(p1.x,8), ',',round(p1.y,8))
    print ('B1 = ',round(B1[0],8), ',',round(B1[1],8))
    print ('B2 = ',round(B2[0],8), ',',round(B2[1],8))
    # begin if
    if m > 0 :
        if B1[1] > B2[1] :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), -(B1[1]-B2[1])]
        else :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), abs(B1[1]-B2[1])]
    else :
        if B1[1] > B2[1] :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), -(B1[1]-B2[1])]
        else :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), abs(B1[1]-B2[1])]
    # end if
    return reflection_matrix
    #
# end of function
#
# begin of function
# p1 is a shapely Point type, ex: point_A = Point(-6,6)
# p2 is reflection line, ex: reflection_line = [(10.,10.),(70.,70.)]
#
def set_reflection_matrix(p1,p2) :
    mbList = findSlope(p2)
    # Print return datatype
    print (type(mbList))# <class 'numpy.ndarray'> a multidimensional, homogeneous array of fixed-size items.
    print (mbList.ndim) # Number of array dimensions
    print (mbList.size) # Number of elements in the array
    print (mbList)
    #
    # Print the findings
    print("Line equation is y = mx + b")
    print ('m =', mbList[0])
    print ('b =', mbList[1])
    print("Line solution is y = {m}x + {b}".format(m=str(mbList[0]) + ' ',b=round(mbList[1],8)))
    print ('\n')
    #
    m = mbList[0]
    b = round(mbList[1],8)
    c = 1/(m**2 + 1)    # 純量c
    # algorithm 1 : here we define a 2D reflection matrix
    reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), 0, 0]
    ref_A = shapely.affinity.affine_transform(p1, reflection_matrix)
    B1 = (ref_A.x, ref_A.y)
    #
    d = (p1.x + (p1.y - b)*m) / (1 + m**2)
    B2 = (2*d - p1.x, 2*d*m - p1.y + 2*b)
    #
    print ('A  = ',round(p1.x,8), ',',round(p1.y,8))
    print ('B1 = ',round(B1[0],8), ',',round(B1[1],8))
    print ('B2 = ',round(B2[0],8), ',',round(B2[1],8))
    #
    # begin if
    if m > 0 :
        if B1[1] > B2[1] :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), -(B1[1]-B2[1])]
        else :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), abs(B1[1]-B2[1])]
    else :
        if B1[1] > B2[1] :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), -(B1[1]-B2[1])]
        else :
            reflection_matrix = [c*(1-m**2), c*2*m, c*2*m, c*(m**2-1), -(B1[0]-B2[0]), abs(B1[1]-B2[1])]
    # end if
    return reflection_matrix
    #
# end of function
#
