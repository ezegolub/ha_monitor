# Process Monitor

This project is a Python script that monitors the computer's processes and integrates with VirtualBox and Steam to manage virtual machines based on gaming activity. It includes a system tray icon for easy interaction.

## Features

- Monitors the Windows registry to detect if a game is running on Steam.
- Manages a VirtualBox virtual machine:
  - Pauses the VM when a game starts.
  - Resumes or starts the VM when no game is running.
- Displays a system tray icon with a menu for interaction.
- Ensures only one instance of the script runs globally.

## Installation

To get started, clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd process-monitor
```

Next, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the process monitor script, execute the following command:

```bash
python src/monitor.py
```

### Running on Startup

To ensure the script runs every time the computer boots up, you can:
1. Add it to the Windows Startup folder.
2. Use the Windows Task Scheduler.
3. Add a registry entry under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.

## Dependencies

This project requires the following Python packages:
- `psutil`: For retrieving system and process information.
- `pystray`: For creating a system tray icon.
- `Pillow`: For generating the tray icon image.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.