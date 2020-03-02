#!/usr/bin/env python3
import configparser
import getopt
import os
import subprocess
import sys
import time


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
    
    Alternatively, you can create/edit ~/.config/break-timer/break-timer.conf file to configure break timer settings.
    Edit the following default with desired values.

    [default]
    desktop = gnome
    max_active_time_min = 30
    grace_period_sec = 10

    [snooze]
    snooze_enabled = no
    snooze_time_min = 5

    """

    print(usages)


def parse_boolean(_str):
    try:
        return _str.lower() in ["true", "yes", "y"]
    except AttributeError:
        return False


def is_locked(desktop="gnome"):
    screensaver_inactive_msg = "The screensaver is inactive"

    try:
        output = subprocess.check_output(
            ["{0}-screensaver-command".format(desktop), "-q"]).decode("utf-8").strip()

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
    subprocess.Popen(["notify-send", title, "--icon", icon])


def show_snooze_notification(snooze_time, icon):
    title = "Timer is snoozed for {0} minutes.".format(snooze_time)
    subprocess.Popen(["notify-send", title, "--icon", icon])


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
    subprocess.Popen(["{0}-screensaver-command".format(desktop), "-l"])


def get_settings_from_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    _desktop = 'gnome'
    _max_active_time = 30
    _grace_period_sec = 10
    _snooze_enabled = 'no'
    _snooze_time = 5

    try:
        _desktop = str(config['default']['desktop'])
    except KeyError:
        pass

    try:
        _max_active_time = int(config['default']['max_active_time_min'])
    except KeyError:
        pass

    try:
        _grace_period_sec = int(config['default']['grace_period_sec'])
    except KeyError:
        pass

    try:
        _snooze_enabled = config.getboolean('snooze', 'snooze_enabled')
    except KeyError:
        pass

    try:
        _snooze_time = int(config['snooze']['snooze_time_min'])
    except KeyError:
        pass

    return _desktop, _max_active_time, _grace_period_sec, _snooze_enabled, _snooze_time


def override_settings_with_commandline_values(argv, desktop, max_active_time, grace_period_sec, snooze_enabled,
                                              snooze_time):
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

    return desktop, grace_period_sec, max_active_time, snooze_enabled, snooze_time


def main(argv):
    one_minute = 60

    home = os.path.expanduser('~')
    config_location = os.path.join(home, '.config/break-timer')
    config_file = os.path.join(config_location, 'break-timer.conf')
    icon = os.path.join(config_location, 'icon.png')

    desktop, max_active_time, grace_period_sec, snooze_enabled, snooze_time = get_settings_from_config(config_file)

    desktop, grace_period_sec, max_active_time, snooze_enabled, snooze_time = override_settings_with_commandline_values(
        argv, desktop, max_active_time, grace_period_sec, snooze_enabled, snooze_time)

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
            print("Screen is active for {0} minutes. Next break in {1} minutes.".format(
                unlocked_time, max_active_time - unlocked_time))

        if unlocked_time >= max_active_time:
            if snooze_enabled:
                if is_snoozed(snooze_time):
                    show_snooze_notification(snooze_time, icon)
                    time.sleep(snooze_time * one_minute)
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
