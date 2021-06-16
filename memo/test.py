code = """
def E(x, y):
    # Exy = x+y
    return x + y
"""
a = exec(code)
print(a)
print(code)
e = E(3, 1)
print(e)
