import psutil
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import time
import winreg
import subprocess
import os
import sys
import ctypes

VM_NAME = "HAVM"
MUTEX_NAME = "Global\\ProcessMonitorMutex"

def ensure_single_instance():
    """Ensure only one instance of the process is running globally."""
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        print("Another instance of this process is already running.")
        sys.exit(1)

def is_game_running():
    """Retrieve the Windows registry to check if a game is running."""
    key = r"Software\\Valve\Steam"
    value = "RunningAppID"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
            running_app_id, _ = winreg.QueryValueEx(reg_key, value)
            print(f"RunningAppID: {running_app_id}")
            return running_app_id != 0  # Return True if a game is running
    except FileNotFoundError:
        print("Registry key or value not found.")
    except OSError as e:
        print(f"Error accessing registry: {e}")
    return False

def get_vm_status(vm_name):
    """Check the status of a VirtualBox virtual machine."""
    try:
        result = subprocess.run(
            [r"C:\Program Files\Oracle\Virtualbox\VBoxManage.exe", "showvminfo", vm_name, "--machinereadable"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("VMState="):
                vm_state = line.split("=")[1].strip().strip('"')
                print(f"VM '{vm_name}' is in state: {vm_state}")
                return vm_state
    except FileNotFoundError:
        print("VBoxManage not found. Ensure VirtualBox is installed and VBoxManage is in PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error checking VM status: {e}")
    return "unknown"

def start_vm(vm_name):
    """Start a VirtualBox virtual machine."""
    try:
        subprocess.run(
            [r"C:\Program Files\Oracle\Virtualbox\VBoxManage.exe", "startvm", vm_name, "--type", "headless"],
            check=True
        )
        print(f"VM '{vm_name}' started successfully.")
    except FileNotFoundError:
        print("VBoxManage not found. Ensure VirtualBox is installed and VBoxManage is in PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting VM: {e}")

def interact_vm(vm_name, action):
    """Pause a VirtualBox virtual machine."""
    try:
        subprocess.run(
            [r"C:\Program Files\Oracle\Virtualbox\VBoxManage.exe", "controlvm", vm_name, action],
            check=True
        )
        print(f"VM '{vm_name}' paused successfully.")
    except FileNotFoundError:
        print("VBoxManage not found. Ensure VirtualBox is installed and VBoxManage is in PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error pausing VM: {e}")

def create_image():
    """Create an image for the tray icon."""
    width = 64
    height = 64
    color1 = "black"
    color2 = "green"

    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (width // 4, height // 4, width * 3 // 4, height * 3 // 4), fill=color2
    )
    return image

def quit_program(icon, item):
    """Stop the tray icon and exit the program."""
    icon.stop()

def monitor_processes(icon, menu):
    """Continuously monitor if a game is running."""
    while True:
        print(icon, menu)
        if is_game_running():
            print("Game is running")
            if get_vm_status(VM_NAME) == "running":
                print("Pausing VM...")
                interact_vm(VM_NAME, "pause")       
        else:
            print("No game running")
            vm_status = get_vm_status(VM_NAME)      
            if vm_status == "poweroff":
                print("Starting VM...")
                start_vm(VM_NAME)
            elif vm_status == "paused":
                print("Resuming VM...")
                interact_vm(VM_NAME, "resume")
        
        time.sleep(5)  # Refresh every 5 seconds
        icon.update_menu()
        
if __name__ == "__main__":
    ensure_single_instance()
    # Create the tray icon
    menu = Menu(
        MenuItem(lambda _: 
                 "--- GAMING MODE ---" if is_game_running() else "--- BORING MODE ---", 
                 lambda _: None, enabled=False),
        MenuItem("Quit", quit_program)
        )
    icon = Icon("Process Monitor", create_image(), "Process Monitor", menu)

    # Run the process monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_processes, args=(icon, menu), daemon=True)
    monitor_thread.start()

    # Run the tray icon
    icon.run()