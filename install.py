#!/usr/bin/env python3
import os
import configparser
import shutil

user = os.environ["USERNAME"]
home = os.path.expanduser("~{0}".format(user))
src_file_destination = '/usr/bin/break-timer.py'
config_location = os.path.join(home, '.config/break-timer')
config_file_destination = os.path.join(config_location, 'break-timer.conf')
icon_destination = os.path.join(config_location, 'icon.png')
desktop_launcher_destination = os.path.join(home, '.config/autostart/break-timer.desktop')

os.makedirs(config_location, exist_ok=True)


def get_desktop_name_from_user():
    _desktop = ''

    desktop_prompt = 'Select a desktop environment:'
    desktop_prompt += '''
    1. gnome
    2. cinnamon
    3. xfce4 
    4. matte'''

    desktop_prompt += '\nEnter your desktop number: '

    desktop_dict = {
        1: 'gnome',
        2: 'cinnamon',
        3: 'xfce4',
        4: 'matte'
    }

    while _desktop == '':
        try:
            desktop_input = int(input(desktop_prompt))
            if 1 <= desktop_input <= 4:
                _desktop = desktop_dict.get(desktop_input)
            else:
                raise ValueError
        except ValueError:
            print("Enter a number between 1 -4")

    return _desktop


def get_max_active_time_from_user():
    _max_active_time = 0

    while _max_active_time == 0:
        try:
            max_active_time_input = input(
                "Set max active time in min(app will show notification after this time, default 30): ")
            if max_active_time_input == '':
                _max_active_time = 30
            elif int(max_active_time_input) > 0:
                _max_active_time = int(max_active_time_input)
            else:
                raise ValueError

        except ValueError:
            print("Enter a valid number greater than 0")

    return _max_active_time


def get_grace_period_from_user():
    _grace_period = 0

    while _grace_period == 0:
        try:
            grace_period_input = input(
                "Set grace period in sec (time before desktop get locked after showing notification, default: 10): ")
            if grace_period_input == '':
                _grace_period = 10
            elif int(grace_period_input) > 0:
                _grace_period = int(grace_period_input)
            else:
                raise ValueError

        except ValueError:
            print("Enter a valid number greater than 0")

    return _grace_period


def get_snooze_enabled_from_user():
    _snooze_enabled = ''

    while _snooze_enabled == '':
        try:
            snooze_enabled_input = input("Enable snooze yes/no (will show a prompt for snooze or break, default no):")
            if snooze_enabled_input == '':
                _snooze_enabled = 'no'
            elif snooze_enabled_input.lower() in ('yes', 'true', 'y'):
                _snooze_enabled = 'yes'
            elif snooze_enabled_input.lower() in ('no', 'false', 'n'):
                _snooze_enabled = 'no'
            else:
                raise ValueError
        except ValueError:
            print("Enter yes/no/y/n")

    return _snooze_enabled


def get_snooze_time_from_user():
    _snooze_time = 0

    while _snooze_time == 0:
        try:
            snooze_time_input = input(
                "Snooze time in min (works if snooze is enabled, default: 5): ")
            if snooze_time_input == '':
                _snooze_time = 5
            elif int(snooze_time_input) > 0:
                _snooze_time = int(snooze_time_input)
            else:
                raise ValueError

        except ValueError:
            print("Enter a valid number greater than 0")

    return str(_snooze_time)


def create_config_file(_desktop, _max_active_time, _grace_period, _snooze_enabled, _snooze_time):
    print("Creating configuration file...")
    config = configparser.ConfigParser()

    config.add_section('default')
    config['default']['desktop'] = str(_desktop)
    config['default']['max_active_time_min'] = str(_max_active_time)
    config['default']['grace_period_sec'] = str(_grace_period)
    config.add_section('snooze')
    config['snooze']['snooze_enabled'] = str(_snooze_enabled)
    config['snooze']['snooze_time_min'] = str(_snooze_time)

    with open(config_file_destination, 'w') as configfile:
        config.write(configfile)
        print("Configuration file created in {0}".format(config_file_destination))
    pass


def copy_icon():
    try:
        shutil.copyfile('./icon.png', icon_destination)
        print("Copied icon to {0}".format(icon_destination))
    except Exception as e:
        print(e)


def copy_src_file():
    try:
        shutil.copyfile('./src/break-timer.py', src_file_destination)
        print("Copied src file to to {0}".format(src_file_destination))
    except PermissionError:
        print("Permission error while copying to {0}. Try running with sudo.".format(src_file_destination))
    except Exception as e:
        print(e)


def copy_desktop_launcher():
    try:
        shutil.copyfile('./break-timer.desktop', desktop_launcher_destination)
        print("Copied launcher file to to {0}".format(desktop_launcher_destination))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    desktop = get_desktop_name_from_user()
    max_active_time = get_max_active_time_from_user()
    grace_period = get_grace_period_from_user()
    snooze_enabled = get_snooze_enabled_from_user()
    snooze_time = '5' if snooze_enabled == 'no' else get_snooze_time_from_user()  # default 5

    create_config_file(desktop, max_active_time, grace_period, snooze_enabled, snooze_time)
    copy_icon()
    copy_src_file()
    copy_desktop_launcher()
