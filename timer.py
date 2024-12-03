import argparse
import threading
from dataclasses import dataclass
from os import system
from time import sleep

from rich.console import Console
from rich.progress import track

console = Console()


def count(time: float):
    paused = threading.Event()

    def toggle_pause():
        while True:
            input("Press Enter to pause/resume.")
            if paused.is_set():
                paused.clear()
            else:
                paused.set()

    threading.Thread(target=toggle_pause, daemon=True).start()

    for i in track(range(int(time)), description="Time left..."):
        while paused.is_set():
            sleep(0.1)
        sleep(1)


def play_beep(beep_count: int):
    system(
        f"for i in $(seq 1 {beep_count}); do paplay "
        f"/usr/share/sounds/freedesktop/stereo/complete.oga; done")


def notify(message: str):
    system(f"notify-send  -u critical -t 10000 '{message}'")


def cycle(work_time: float, rest_time: float):
    console.print("[bold green]Work Time[/bold green]")
    count(work_time * 60)
    notify("Rest Time Start")
    play_beep(3)
    console.print("[bold blue]Rest Time[/bold blue]")
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
        console.print(f"[bold yellow]Starting cycle {i + 1}[/bold yellow]")
        cycle(state.work_time, state.rest_time)


if __name__ == "__main__":
    main()
