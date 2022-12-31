a = 54


def test():
    global a
    print(a)
    a = 10


test()
print(a)