import psutil
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import time
import winreg
import subprocess


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
            ["VBoxManage", "showvminfo", vm_name, "--machinereadable"],
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
        else:
            print("No game running")      
        time.sleep(5)  # Refresh every 5 seconds
        icon.update_menu()
        
        #icon.stop()

if __name__ == "__main__":   
    get_vm_status("Windows 11")  # Replace with your VM name

    exit()
    
     
    # Create the tray icon
    menu = Menu(
        MenuItem(lambda _: 
                 "--- GAMING MODE ---" if is_game_running() else "--- BORING MODE ---", 
                 lambda _: None, enabled=False),
        MenuItem("Start VM", lambda icon, item: None, enabled=False),
        MenuItem("Pause VM", lambda icon, item: None, enabled=False),
        MenuItem("Quit", quit_program)
        )
    icon = Icon("Process Monitor", create_image(), "Process Monitor", menu)

    # Run the process monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_processes, args=(icon, menu), daemon=True)
    monitor_thread.start()

    # Run the tray icon
    icon.run()