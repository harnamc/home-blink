# Home Blink Service

This project is a Python application designed to interact with Blink devices. Currently, it updates the thumbnails of all camera in the Blink account. The setup will create a `systemd` service and timer to run evert 15 minutes. The properties can be modified for your own use case.

## Prerequisites

- Linux system with systemd (e.g., RHEL 9, CentOS, Ubuntu)
- Python 3.x installed
- Git installed

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

### 3. Run `setup.py` Script to Generate `credentials.json`

```bash
python python ./src/home_blink/setup.py
```

Follow the prompt and enter `username`, `password` and OTP if it is setup. This script will generate/update the `credentials.json` file.

### 4. Configure `systemd` to Run the Script Every 15 Minutes

- Update the `example.home-blink.service` by replace `{USERNAME}` with your own username. Your repo location could be different, just make sure it matches to where your source code is.
- Copy the Files to the user `systemd` directory.

```bash
cp example.home-blink.service ~/.config/systemd/user/home-blink.service
cp example.home-blink.timer ~/.config/systemd/user/home-blink.timer
```

### 5. Enable and Start the Service

```bash
systemctl --user daemon-reload
systemctl --user enable home-blink.timer
systemctl --user start home-blink.timer
```

### 6. Verify Your Setup

```bash
systemctl --user status home-blink.timer
journalctl --user-unit home-blink.service --follow
```

## Updating the Service

When you pull new changes from GitHub, update your repository and virtual environment as follows:

```bash
cd ~/Projects/home-blink # or where you cloned the repo.
git pull
source venv/bin/activate
pip install -r requirements.txt
```

Then, reload the user `systemd` configuration and restart the timer:

```bash
systemctl --user daemon-reload
systemctl --user restart home-blink.timer
```

## Troubleshooting

```bash
journalctl --user-unit home-blink.service
```
