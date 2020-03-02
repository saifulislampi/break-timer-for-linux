import errno
import os

home = os.path.expanduser('~')
src_file_destination = '/usr/bin/break-timer.py'
desktop_launcher_destination = os.path.join(home, '.config/autostart/break-timer.desktop')


def remove_if_exist(filename):
    try:
        os.remove(filename)
        print("Removed {0}".format(filename))
    except PermissionError:
        print("Permission error! Try running with sudo.")
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("File {0} not found!".format(filename))
        else:
            raise


if __name__ == "__main__":
    remove_if_exist(src_file_destination)
    remove_if_exist(desktop_launcher_destination)
    print("Uninstall completed!")
