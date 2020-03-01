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
        -d, --desktop       Name of the desktop environment (e.g: "gnome", "cinnamon", default is taken from DESKTOP_SESSION)
        -t, --active-time   Time in minutes before the app shows screen lock notification after unlock (default 20)
        -p, --grace-period  Time in seconds before the screen get locked after showing notification (default 10)
        -s, --snooze-enable Enable snooze option (default false)
        -z, --snooze-time   Snooze time in minutes (default 5)
    
    Break Timer can also be configured via environment variable. Open .bashrc or .zshrc and add the following lines
    with desired changes -

        export BREAK_TIMER_MAX_ACTIVE_MIN=30
        export BREAK_TIMER_GRACE_SEC=10
        export BREAK_TIMER_SNOOZE_ENABLED=false
        export BREAK_TIMER_SNOOZE_TIME_MIN=5
    """
    print(usages)


def parse_boolean(str):
    try:
        return str.lower() in ["true", "yes", "y"]
    except:
        return False


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


def show_lock_notification(grace_period_sec, icon):
    title = "Time to take a break! Your PC will be locked in {0} sceconds.".format(
        grace_period_sec)
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
    desktop = os.getenv('DESKTOP_SESSION', 'gnome').strip()
    grace_period_sec = int(os.getenv('BREAK_TIMER_GRACE_SEC', '10'))
    max_active_time = int(os.getenv('BREAK_TIMER_MAX_ACTIVE_MIN', '30'))

    # snooze options
    snooze_enabled = parse_boolean(os.getenv('BREAK_TIMER_SNOOZE_ENABLED', ''))
    snooze_time = int(os.getenv('BREAK_TIMER_SNOOZE_TIME_MIN', '5'))

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
            grace_period_sec = int(arg)
        elif opt in options["snooze_enabled"]:
            snooze_enabled = arg.lower() in ["true", "yes", "y"]
        elif opt in options["snooze_time"]:
            snooze_time = int(arg)

    print("Break Timer Configuration")
    print("__________________________")
    print("Max Active Time: {0} min".format(max_active_time))
    print("Grace Period: {0} sec".format(grace_period_sec))
    print("Snooze Time: {0} min".format(snooze_time))
    print("Snooze Enabled: {0}".format(snooze_enabled))
    print("Desktop Environment: {0}".format(desktop))
    print("\n")

    print("Timer started. Next break in {0} minutes.".format(max_active_time))

    unlocked_time = 0

    while True:
        time.sleep(one_minute)

        if is_locked(desktop):
            unlocked_time = 0
        else:
            unlocked_time += 1
            print("Timer is running for {0} minutes. Next break in {1} minutes.".format(
                unlocked_time, max_active_time - unlocked_time))

        if unlocked_time >= max_active_time:
            if snooze_enabled:
                if is_snoozed(snooze_time):
                    show_snooze_notification(snooze_time, icon)
                    time.sleep(snooze_time*one_minute)
                else:
                    unlocked_time = 0
                    lock_screen(desktop)
            else:
                unlocked_time = 0
                show_lock_notification(grace_period_sec, icon)
                time.sleep(grace_period_sec)
                lock_screen(desktop)


if __name__ == "__main__":
    main(sys.argv[1:])
