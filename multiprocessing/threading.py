import concurrent.futures
import time


def do_something(seconds):
    print(f"Start processing for {seconds} seconde(s)...")
    time.sleep(seconds)
    return f"End processing after {seconds} seconde(s)"


def main():
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(do_something, range(5))

    end = time.perf_counter()
    print(f"Finished in {round(end-start,2)} second(s)")


if __name__ == "__main__":
    main()
