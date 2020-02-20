#!/usr/bin/env python3
import os
import sys
import time
import getopt
import subprocess


def show_usages():
    usages = """
    Usage:
        python3 break-timer.py [OPTION…]

    Options:
        -h, --help          Show Help Options
        -d, --desktop       Name of the desktop environment (e.g: "gnome", "cinnamon", default "gnome")
        -t, --active-time   Time in minutes before the app shows screen lock notification after unlock (default 20)
        -p, --grace-period  Time in seconds before the screen get locked after showing notification (default 10)
        -s, --snooze-enable Enable snooze option (default false)
        -z, --snooze-time   Snooze time in minutes (default 5)
    """
    print(usages)


def is_locked(desktop="gnome"):
    screensaver_inactive_msg = "The screensaver is inactive"

    try:
        output = subprocess.check_output(
            ["{0}-screensaver-command".format(desktop),  "-q"]).decode("utf-8").strip()

        if screensaver_inactive_msg in output:
            return False
        else:
            return True

    except subprocess.CalledProcessError:
        print("Error running screensaver-command. Make sure you have screensaver-command\
             installed for your desktop environment.")
        sys.exit(2)


def show_lock_notification(grace_period, icon):
    title = "Time to take a break! Your PC will be locked in {0} sceconds.".format(
        grace_period)
    subprocess.Popen(["notify-send",  title, "--icon", icon])


def show_snooze_notification(snooze_time, icon):
    title = "Timer is snoozed for {0} minutes.".format(snooze_time)
    subprocess.Popen(["notify-send",  title, "--icon", icon])


def is_snoozed(snooze_time):
    try:
        title = "Time to take break!"
        text = "Do you want to take a break now?"
        snooze_button_label = "Snooze for {0} minutes".format(snooze_time)

        command = ["zenity", "--question", "--title", title,
                   "--text", text, "--cancel-label", snooze_button_label,
                   "--no-wrap", "true"]

        subprocess.check_output(command)
        return False

    except subprocess.CalledProcessError:
        return True


def lock_screen(desktop):
    subprocess.Popen(["{0}-screensaver-command".format(desktop),  "-l"])


def main(argv):
    desktop = "gnome"
    unlocked_time = 0
    grace_period = 10
    max_active_time = 30

    # snooze options
    snooze_enabled = False
    # default snooze time in minutes
    snooze_time = 5

    one_minute = 60
    icon = os.path.abspath("icon.png")

    options = {
        "help": ["-h", "help"],
        "desktop": ["-d", "--desktop"],
        "active_time": ["-t", "--active-time"],
        "grace_period": ["-p", "--grace-period"],
        "snooze_enabled": ["-s", "--snooze-enable"],
        "snooze_time": ["-z", "--snooze-time"]
    }

    try:
        opts, args = getopt.getopt(argv, "hd:t:p:s:z:", ["help", "desktop=", "active-time=", "grace-period=",
                                                         "snooze-enable=", "snooze-time="])
    except getopt.GetoptError:
        show_usages()
        sys.exit(2)

    for opt, arg in opts:
        if opt in options["help"]:
            show_usages()
            sys.exit(2)
        elif opt in options["desktop"]:
            desktop = arg
        elif opt in options["active_time"]:
            max_active_time = int(arg)
        elif opt in options["grace_period"]:
            grace_period = int(arg)
        elif opt in options["snooze_enabled"]:
            snooze_enabled = arg.lower() in ["true", "yes", "y"]
        elif opt in options["snooze_time"]:
            snooze_time = int(arg)

    print("Timer started. Next break in {0} minutes.".format(max_active_time))

    while True:
        time.sleep(one_minute)

        if is_locked(desktop):
            unlocked_time = 0
        else:
            unlocked_time += 1
            print("Timer is running for {0} minutes. Next break in {1} minutes.".format(
                unlocked_time, max_active_time - unlocked_time))

        if unlocked_time >= max_active_time:
            unlocked_time = 0

            if snooze_enabled:
                if is_snoozed(snooze_time):
                    show_snooze_notification(snooze_time, icon)
                    time.sleep(snooze_time*one_minute)
                else:
                    lock_screen(desktop)
            else:
                show_lock_notification(grace_period, icon)
                time.sleep(grace_period)
                lock_screen(desktop)


if __name__ == "__main__":
    main(sys.argv[1:])
