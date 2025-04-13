import psutil

def get_processes():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            process_info = proc.info
            process_list.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list

def display_processes(process_list):
    print(f"{'PID':<10} {'Name':<25} {'CPU Usage (%)':<15}")
    print("=" * 50)
    for process in process_list:
        print(f"{process['pid']:<10} {process['name']:<25} {process['cpu_percent']:<15}")

if __name__ == "__main__":
    processes = get_processes()
    display_processes(processes)