# Break Timer For Linux
A simple python application that reminds you to take break after certain amount of screen on time and automatically lock the screen. 

![Break Timer For Linux Preview](break-timer-preview.jpg)

## Installation

This python app depends linux desktop screen saver packages like `gnome-screensaver-command` or `cinnamon-screensaver-command`. Also uses `send-notify` pacage to show notification. First make sure that you have this packages installed in your linux desktop.

Then clone git repository and cd into directory

```
git clone https://github.com/saifulislamplabon/break-timer-for-linux.git
cd break-timer-for-linux
```

Run the `break-timer.py` file with desired otptions. For example to set a break after every 20 minutes in gnome desktop, run -

```
python3 break-timer.py -t 20
```

Other available options are given here -

```
-h, --help          Show Help Options
-d, --desktop       Name of the desktop environment (e.g: "gnome", "cinnamon", default "gnome")
-t, --active-time   Time in minutes before the app shows screen lock notification after unlock (default 20)
-p, --grace-period  Time in seconds before the screen get locked after showing notification (default 10)
```