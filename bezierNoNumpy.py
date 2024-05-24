import matplotlib.pyplot as plt
import pyautogui
import random

def calculateTincrement(p0, p2):

    p0x, p0y = p0
    p2x, p2y = p2

    totalDistance = abs(p0x-p2x) + abs(p0y-p2y)
    tIncrement = totalDistance

    return tIncrement

def calculateOffSet(p0,p2):

    p0x, p0y = p0
    p2x, p2y = p2

    totalDistance = abs(p0x-p2x) + abs(p0y-p2y)
    offSet = totalDistance / 5
    return offSet

def determineMidPoint(p0,p2,offset):

    osx = random.gauss(0,offset)
    osy = random.gauss(0,offset)
    print(f"Offset X: {osx}, Offset Y: {osy}")

    p0x, p0y = p0
    p2x, p2y = p2

    x = ((p0x + p2x)/2) + osx
    y = ((p0y + p2y)/2) + osy

    return (x,y)
    
def calculateQuadraticControlPoints(p0, p1, p2, tIncrement):
    t = 0
    bArr = []
    while t <= 1:
        p0t = tuple( ((1-t)**2) * digit for digit in p0 )
        p1t = tuple( ((2*(1-t))*t) * digit for digit in p1 )
        p2t = tuple( (t**2) * digit for digit in p2 )
        b = tuple( a+b+c for a,b,c in zip(p0t,p1t,p2t))
        print(b)
        bArr.append(b)
        t += tIncrement
    return bArr

def calculatelinearControlPoints(p0,p1,tIncrement):
    t = 0
    while t <= 1:
        p0t = tuple((1-t) * digit for digit in p0) 
        p1t = tuple(t * digit for digit in p1)
        b = tuple(a + b for a,b in zip(p0t, p1t))
        print(b)
        t += tIncrement

def moveMouseWithArray(cpArr):

    while cpArr:
        cords = cpArr.pop(0)
        x,y = cords
        x = round(x)
        y = round(y)
        pyautogui.moveTo(x,y,0.001)


def main():
    pyautogui.MINIMUM_DURATION = 0.001
    pyautogui.PAUSE = 0.005

    """
    distance  | increment
    000 - 100 | 0.10 (10cp)
    101 - 500 | 0.05 (50cp)
    500+ - inf| 0.01 (100cp)

    would want variablespeed - the move function could handle the speed and divide it amonst the control points
    and multiple curves
    for more precise clicks a different type of algorithm would need to be used
    """

    p0 = (100,100)
    p2 = (140,140)

    # p0 = (100,100)
    # p2 = (1500,100)

    os = calculateOffSet(p0,p2)
    m = determineMidPoint(p0,p2,os)
    # m = (4,8)

    result = calculateQuadraticControlPoints(p0,m,p2,.10)

    moveMouseWithArray(result)
    
    x_coords = [point[0] for point in result]
    y_coords = [point[1] for point in result]

    fig , ax = plt.subplots()
    ax.plot(x_coords, y_coords, label='Quadratic Bézier Curve')

    ax.scatter(*zip(*[p0, m, p2]), color='red', label='Control Points')  # Plot the control points

    ax.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Quadratic Bézier Curve')
    plt.show()


if __name__ == "__main__":
    main()