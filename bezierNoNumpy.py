import matplotlib.pyplot as plt
import random

def determineMidPoint(p0,p2,offset):

    osx = random.gauss(0,offset)
    osy = random.gauss(0,offset)

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

def main():
    # t = .25
    # p0 = (0,0)
    # p1 = (1,1)
    # b = tuple((1-t)*element for element in p0)

    # print(tuple(2 * element for element in (2,2)))
    # calculatelinearControlPoints((2,3),(8,7),.25)

    
    # result = determineMidPoint((1,1),(2,2))
    # print(result)

    p0 = (100,100)
    p2 = (753,400)

    m = determineMidPoint(p0,p2,50)
    # m = (4,8)

    result = calculateQuadraticControlPoints(p0,m,p2,.01)
    
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