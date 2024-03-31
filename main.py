import threading
import time
import random

class Philosopher(threading.Thread):
    running = True

    def __init__(self, name, left_fork, right_fork):
        threading.Thread.__init__(self)
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while self.running:
            time.sleep(random.uniform(1, 3))
            print(f'{self.name} is hungry.')
            self.dine()

    def dine(self):
        fork1, fork2 = self.left_fork, self.right_fork

        while self.running:
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked:
                break
            fork1.release()
            print(f'{self.name} swaps forks')
            fork1, fork2 = fork2, fork1
        else:
            return

        self.eat()
        fork2.release()
        fork1.release()

    def eat(self):
        print(f'{self.name} starts eating.')
        time.sleep(random.uniform(1, 3))
        print(f'{self.name} finishes eating and starts thinking.')


def main():
    forks = [threading.Lock() for _ in range(5)]
    philosophers = [Philosopher(f'Philosopher {i}', forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]

    for philosopher in philosophers:
        philosopher.start()

    time.sleep(10)
    Philosopher.running = False

    for philosopher in philosophers:
        philosopher.join()

    print("Now we're finishing.")

if __name__ == "__main__":
    main()
