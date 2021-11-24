def make_bezier(xys):
    # code copied from https://stackoverflow.com/a/2292690
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n, memo={}):
    # code copied from https://stackoverflow.com/a/2292690
    # This returns the nth row of Pascal"s Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result
    

class Polygon:
    def __init__(self, N):
        self.ts = [t/N for t in range(N+1)]
        self.points = []

    def extend(self, xys):
        bezier = make_bezier(xys)
        self.points.extend(bezier(self.ts))
        
    def draw(self, draw, color = "black"):
        draw.polygon(self.points, fill = color)
