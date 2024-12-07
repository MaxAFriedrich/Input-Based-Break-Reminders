import argparse
import subprocess
from enum import EnumType
from os import system


class Input(EnumType):
    click = 0
    key = 1


def play_beep(beep_count: int):
    system(
        f"for i in $(seq 1 {beep_count}); do paplay "
        f"/usr/share/sounds/freedesktop/stereo/complete.oga; done")


def notify(message: str):
    system(f"notify-send  -u critical -t 10000 '{message}'")


def get_keys():
    process = subprocess.Popen(['keyd', 'monitor'], stdout=subprocess.PIPE,
                               text=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line


def parse_line(line) -> int | None:
    # returns if a key, click, or None
    elements = line.strip().split("\t")
    if len(elements) != 3:
        return None

    device_type = None
    if any(device in elements[0].lower() for device in
           ["mouse", "pointer", "touchpad", "trackpoint"]):
        device_type = Input.click
    elif "keyboard" in elements[0].lower():
        device_type = Input.key
    else:
        return None

    input_name = elements[2].split(" ")[0]
    input_type = elements[2].split(" ")[1]

    if input_type == "up":
        return None

    if device_type == Input.click and not input_name.endswith("mouse"):
        return None

    return device_type


def main(threshold: int):
    total_clicks = 0
    total_keys = 0

    for line in get_keys():
        response = parse_line(line)
        if response == Input.click:
            total_clicks += 1
        elif response == Input.key:
            total_keys += 1

        if total_clicks * 1.2 + total_keys > threshold:
            message = (f"Take a break! You have clicked {total_clicks} times "
                       f"and pressed {total_keys} keys.")
            notify(message)
            print(message)
            play_beep(3)
            total_keys = 0
            total_clicks = 0
        else:
            print(f"Total Clicks: {total_clicks} Total Keys: {total_keys}\r", end="")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("threshold", type=int, default=1000, nargs="?")
    args = args.parse_args()
    main(args.threshold)
