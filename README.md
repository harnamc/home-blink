# Home Blink Service

This project is a Python application designed to interact with Blink devices.

## Prerequisites

- Linux system with systemd (e.g., RHEL 9, CentOS, Ubuntu)
- Python 3.x installed
- Git installed
- Sudo privileges (for system-wide configuration) **or** use user-level systemd if preferred

## Setup

### 1. Clone the Repository

```bash
mkdir -p ~/Projects
cd ~/Projects
git clone git@github.com:harnamc/home-blink.git
cd home-blink
```

### 2. Create a Python Virtual Environment and Install Requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure `systemd` to Run the Script Every 5 Minutes

- Create a file named `home-blink.service` with the following content and replace `{USERNAME}` with your own username.

```bash
[Unit]
Description=Home Blink Python Service
After=network.target

[Service]
WorkingDirectory=/home/{USERNAME}/Projects/home-blink
ExecStart=/home/{USERNAME}/Projects/home-blink/venv/bin/python -m home_blink.main
Restart=always
RestartSec=5

StandardOutput=append:/home/{USERNAME}/Projects/home-blink/log/home-blink.og
StandardError=append:/home/{USERNAME}/Projects/home-blink/log/home-blink.log

[Install]
WantedBy=multi-user.target
```

- Create a file named `home-blink.timer` with the following content:

```bash
[Unit]
Description=Run Home Blink Service every 5 minutes

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=home-blink.service

[Install]
WantedBy=timers.target
```

- Copy the Files to the user `systemd` directory, replace `{USERNAME}` with your username.

```bash
cp home-blink.service /home/{USERNAME}/.config/systemd/user
cp home-blink.timer /home/{USERNAME}/.config/systemd/user
```

### 4. Enable and Start the Service

```bash
systemctl --user daemon-reload
systemctl --user enable home-blink.timer
systemctl --user start home-blink.timer
```

### 5. Verify Your Setup

```bash
systemctl --user status home-blink.timer
journalctl --user-unit home-blink.service --follow
cat ~/Projects/home-blink/log/home-blink.log
```

### 6. Updating the Service

When you pull new changes from GitHub, update your repository and virtual environment as follows:

```bash
cd ~/Projects/home-blink
git pull
source venv/bin/activate
pip install -r requirements.txt
```

Then, reload the user systemd configuration and restart the timer:

```bash
systemctl --user daemon-reload
systemctl --user restart home-blink.timer
```

## Troubleshooting

```bash
journalctl --user-unit home-blink.service
```
