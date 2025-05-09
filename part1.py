from timeit import timeit

def integrate_st(f, a, b, n=1000):
    step = (b - a) / n
    start = a
    sum = 0.0

    for _ in range(n):
        sum += f(start) * step
        start += step

    return sum

def integrate_mt(f, a, b, n=1000):
    from threading import Thread, Lock
    from multiprocessing import cpu_count

    num_threads = cpu_count()

    lock = Lock()

    threads = []

    step = (b - a) / n
    sum = 0.0

    def worker(start, end):
        nonlocal sum
        sub_sum = 0.0

        for i in range(start, end):
            x = a + i * step
            sub_sum += f(x) * step

        with lock:
            nonlocal sum
            sum += sub_sum

    iter = n // num_threads

    for i in range(num_threads):
        start = i * iter
        end = (i + 1) * iter if i != num_threads - 1 else n
        thread = Thread(target=worker, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum

def part1_main():
    print("st 10**4 iterations: {}s".format(timeit("integrate_st(sin, 0, 1, 100000)", number=100, setup="from part1 import integrate_st; from math import sin")))
    print("st 10**5 iterations: {}s".format(timeit("integrate_st(sin, 0, 1, 1000000)", number=100, setup="from part1 import integrate_st; from math import sin")))
    print("st 10**6 iterations: {}s".format(timeit("integrate_st(sin, 0, 1, 10000000)", number=100, setup="from part1 import integrate_st; from math import sin")))

    print("mt 10**4 iterations: {}s".format(timeit("integrate_mt(sin, 0, 1, 100000)", number=100, setup="from part1 import integrate_mt; from math import sin")))
    print("mt 10**5 iterations: {}s".format(timeit("integrate_mt(sin, 0, 1, 1000000)", number=100, setup="from part1 import integrate_mt; from math import sin")))
    print("mt 10**6 iterations: {}s".format(timeit("integrate_mt(sin, 0, 1, 10000000)", number=100, setup="from part1 import integrate_mt; from math import sin")))
