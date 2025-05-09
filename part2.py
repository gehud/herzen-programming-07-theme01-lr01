def launch_threads(worker):
    import threading

    threads = []

    for i in range(2):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def print_names():
    import threading

    def worker(i):
        print(threading.current_thread().name)

    launch_threads(worker)

def download_images():
    def worker(i):
        import requests

        with requests.get("https://static.vecteezy.com/system/resources/thumbnails/012/176/986/small_2x/a-3d-rendering-image-of-grassed-hill-nature-scenery-png.png", stream=True) as r:
            with open("image_from_thread_{}.png".format(i), 'wb') as f:
                f.write(r.content)

    launch_threads(worker)

def fac_mt(n):
    import threading
    from multiprocessing import cpu_count

    def partial(start, end):
        result = 1
        for i in range(start, end + 1):
            result *= i
        return result

    num_threads = cpu_count()

    chunk_size = n // num_threads
    threads = []
    partial_results = [1] * num_threads

    def worker(thread_id, start, end):
        partial_results[thread_id] = partial(start, end)

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_threads - 1 else n
        thread = threading.Thread(target=worker, args=(i, start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_result = 1
    for res in partial_results:
        final_result *= res

    return final_result

import multiprocessing

def quicksort_mt(arr, low, high, max_threads = multiprocessing.cpu_count()):
    import threading

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quicksort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort(arr, low, pi - 1)
            quicksort(arr, pi + 1, high)

    if low >= high:
        return

    pi = partition(arr, low, high)

    # Create threads if we haven't reached the maximum thread count
    if max_threads > 1:
        # Create a thread for the left partition
        left_thread = threading.Thread(
            target=quicksort_mt,
            args=(arr, low, pi - 1, max_threads // 2)
        )
        left_thread.start()

        # Process right partition in current thread
        quicksort_mt(arr, pi + 1, high, max_threads // 2)

        # Wait for left thread to complete
        left_thread.join()
    else:
        # No more threads available, do sequential sort
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def part2_main():
    import random

    print_names()
    download_images()
    print(fac_mt(5))

    arr = [random.randint(0, 100000) for _ in range(1000)]
    quicksort_mt(arr, 0, len(arr) - 1)

