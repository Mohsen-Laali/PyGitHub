def fib():
    a = 1
    b = 1
    number = 0
    if number < 2:
        yield 1
    else:
        result = a + b
        b, a = result, b
        yield result

for i in fib():
    print i
    if i > 10:
        break

