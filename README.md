# Break Timer For Linux
A simple python application that reminds you to take break after certain amount of screen on time and automatically lock the screen. You can also enable an optional snooze option. 

Timer will reset itself when the screen gets locked and start again at the next unlock. 

The app will show the following notification before locking the screen.

![Break Timer For Linux Preview](break-timer-preview.jpg)

If you enalble snooze option you will get a prompt to take a break or snooze it for few minutes. Snooze time can be configured in startup.

![Break Timer For Linux Snooze Prompt](snooze-preview.jpg)

## Installation

This python app depends linux desktop screen saver packages like `gnome-screensaver-command` or `cinnamon-screensaver-command`. Also uses `send-notify` pacage to show notification. First make sure that you have this packages installed in your linux desktop.

Then clone git repository and cd into directory

```bash
git clone https://github.com/saifulislamplabon/break-timer-for-linux.git
cd break-timer-for-linux
```

## Usage

### Running as a Background Application

Run `install.py` and follow the prompt

```bash
sudo python3 install.py
```

To uninstall run `uninstall.py`

```bash
sudo python3 uninstall.py
```

To configure settings create/edit `~/.config/break-timer/break-timer.conf` file with desired values. A sample config file
will look like this -

```ini
[default]
desktop = gnome
max_active_time_min = 30
grace_period_sec = 10

[snooze]
snooze_enabled = no
snooze_time_min = 5
```

### Running as a Python Script

Run the `break-timer.py` with desired otptions. For example to set a break for every 20 minutes, run -

```bash
python3 break-timer.py -d gnome -t 20
```

To enable snooze option -

```bash
python3 break-timer.py -d gnome -t 20 -s true
```

Other available options are given here -

```
-h, --help          Show Help Options
-d, --desktop       Name of the desktop environment (e.g: "gnome", "cinnamon", default "gnome")
-t, --active-time   Time in minutes before the app shows screen lock notification after unlock (default 20)
-p, --grace-period  Time in seconds before the screen get locked after showing notification (default 10)
-s, --snooze-enable Enable snooze option (default false)
-z, --snooze-time   Snooze time in minutes (default 5)
```

## Credits
![Icon](icon.png)

Icon used in notification is made by [ultimatearm](https://www.flaticon.com/authors/ultimatearm) from [www.flaticon.com]("https://www.flaticon.com")
