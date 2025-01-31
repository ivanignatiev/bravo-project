# Adopted from https://gist.github.com/akupar/19ee10dd67a53fa170b42e588b720ad1

from timeit import default_timer as timer
from sys import stdout as terminal
from time import sleep
from itertools import cycle
from threading import Thread
from contextlib import contextmanager


@contextmanager
def loading_animation(running_text: str = "Running", finished_text: str = "Done!"):
    done = False

    def animation():
        timer_start = timer()
        for c in cycle(["|", "/", "-", "\\"]):
            if done:
                break
            time_in_sec = timer() - timer_start
            text_to_display = f"\r{running_text} " + "{:.2f}".format(time_in_sec) + "s " + c
            terminal.write(text_to_display)
            terminal.flush()
            sleep(0.1)

        diff = len(text_to_display) - len(finished_text) + 2
        spaces = " " * diff if diff > 0 else ""
        terminal.write(f"\r{finished_text}" + spaces + "\n")
        terminal.flush()

    try:
        t = Thread(target=animation)
        t.start()
        yield t
    finally:
        done = True
        t.join()
