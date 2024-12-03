import argparse
from dataclasses import dataclass
from os import system
from time import sleep


def count(time: float):
    # TODO allow pausing
    for i in range(int(time)):
        sleep(1)
        print(f"{time - i} seconds left", end="\r")


def play_beep(beep_count: int):
    # beep n times
    system(
        f"for i in $(seq 1 {beep_count}); do paplay "
        f"/usr/share/sounds/freedesktop/stereo/complete.oga; done")


def notify(message: str):
    # show message
    system(f"notify-send  -u critical -t 10000 '{message}'")


def cycle(work_time: float, rest_time: float):
    """
    :param work_time:  time in minutes
    :param rest_time:  time in minutes
    :return:
    """
    # work time
    print("Work Time")
    count(work_time * 60)
    # rest time
    notify("Rest Time Start")
    play_beep(3)
    print("Rest Time")
    count(rest_time * 60)
    notify("Rest Time End")
    play_beep(1)


@dataclass
class State:
    work_time: float
    rest_time: float
    cycles: int

    def save(self):
        with open("state.txt", "w") as f:
            f.write(f"{self.work_time}\n{self.rest_time}\n{self.cycles}")

    @classmethod
    def load(cls):
        with open("state.txt", "r") as f:
            work_time = float(f.readline())
            rest_time = float(f.readline())
            cycles = int(f.readline())
            return cls(work_time, rest_time, cycles)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("work_time", type=float, default=None, nargs="?")
    parser.add_argument("rest_time", type=float, default=None, nargs="?")
    parser.add_argument("cycles", type=int, default=None, nargs="?")
    args = parser.parse_args()

    if args.work_time and args.rest_time and args.cycles:
        state = State(args.work_time, args.rest_time, args.cycles)
        state.save()
    else:
        state = State.load()

    for i in range(state.cycles):
        print(f"Starting cycle {i + 1}")
        cycle(state.work_time, state.rest_time)


if __name__ == "__main__":
    main()
