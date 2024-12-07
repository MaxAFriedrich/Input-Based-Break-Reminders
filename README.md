# Input-Based Break Reminders

This is a simple Python script that helps you to remember to take breaks. It keeps track of mouse clicks
and key presses. After the specified number of inputs, it reminds you to take a break.

I hacked this script together to solve a problem I had quickly. It is not very configurable, however, feel free to
create an issue, or a PR to add new features it is missing.

## Motivation

I built this because I use keyboards and mice a lot and often forget to take breaks. Because of this, I
sometimes get repetitive strain injury(RSI). I find taking small breaks frequently to break up intensive work mitigates
the worst of this.

## How it works

The script uses the `keyd monitor` command to listen for clicks and key-presses. It assumes that a click has taken some
effort to move the mouse and therefore increases the weight of clicks by 20% to compensate for this. The goal is not to
give a totally accurate count of key-presses.

## Dependencies

- `keyd`
- `/usr/share/sounds/freedesktop/stereo/complete.oga`
- `pulseaudio`
- `notify-send`
- `python ^3.11`

## Usage

Run the script with the number of inputs you want to wait for before reminding you to take a break. It takes a single
argument for the number of inputs to notify after. The default is 1000.

```bash
python3 keys.py 100
```

