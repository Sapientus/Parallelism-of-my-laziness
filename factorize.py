from time import time
from multiprocessing import Process, cpu_count, Pool


# Function for synchronic code
def factorize_s(*number):
    # result = []
    time_start = time()
    for n in number:
        division_list = []
        for d in range(1, n + 1):
            if n % d == 0:
                division_list.append(d)
        print(f"Number {n} may be divided by {division_list}")
        # result.append(division_list)
    time_end = time()
    full_time = time_end - time_start
    return f"Time taken for operation {full_time}"


def factorize(n):
    result = []
    for d in range(1, n + 1):
        if n % d == 0:
            result.append(d)
    return f"Number {n} may be divided by {result}"


def main(*numbers):
    count = cpu_count()
    time_start = time()
    with Pool(count) as pool:
        for i in numbers:
            print(f"Operation for number {i}")
            pool.apply_async(print(factorize(i)))

    pool.close()
    pool.join()
    time_end = time()
    full_time = time_end - time_start
    return f"Time taken for operation: {full_time}"


if __name__ == "__main__":
    print("\n{:=^80}\n".format(" Synchronic code "))
    print(factorize_s(128, 255, 99999, 10651060))
    print("\n{:=^80}\n".format(" Code with multiprocessing "))
    print(main(128, 255, 99999, 10651060))
