import subprocess

def get_netstat_pids():
    try:
        # Run netstat command and capture the output
        netstat_output = subprocess.check_output(['netstat', '-ano'], universal_newlines=True)
        return netstat_output
    except subprocess.CalledProcessError as e:
        print(f"Error running netstat command: {e}")
        return None

def get_tasklist():
    try:
        # Run tasklist command and capture the output
        tasklist_output = subprocess.check_output(['tasklist'], universal_newlines=True)
        return tasklist_output
    except subprocess.CalledProcessError as e:
        print(f"Error running tasklist command: {e}")
        return None

def link_pids_to_programs(netstat_output, tasklist_output):
    if netstat_output is None or tasklist_output is None:
        return "Error getting command output."

    # Extract PIDs from netstat output
    netstat_pids = [line.split()[-1] for line in netstat_output.splitlines() if line.strip().endswith("LISTENING")]

    # Extract programs from tasklist output
    tasklist_programs = {line.split()[1]: line.split()[0] for line in tasklist_output.splitlines()[3:]}

    # Link PIDs to programs
    linked_info = {}
    for pid in netstat_pids:
        program = tasklist_programs.get(pid, "Unknown Program")
        linked_info[pid] = program

    return linked_info

if __name__ == "__main__":
    # Get netstat and tasklist output
    netstat_output = get_netstat_pids()
    tasklist_output = get_tasklist()

    # Link PIDs to programs
    linked_info = link_pids_to_programs(netstat_output, tasklist_output)

    # Display the linked information
    print("PID   Program")
    print("-" * 15)
    for pid, program in linked_info.items():
        print(f"{pid}   {program}")
import subprocess

# Run netstat -ano to get the list of PIDs associated with open ports
netstat_output = subprocess.check_output(['netstat', '-ano'], text=True)

# Run tasklist to get the list of running programs and their corresponding PIDs
tasklist_output = subprocess.check_output(['tasklist'], text=True)

# Display the PIDs and corresponding program names
print("PID   Program")
print("---------------")

# Iterate over each line in the netstat output
for line in netstat_output.splitlines():
    # Extract the PID from the netstat output
    parts = line.split()
    if len(parts) >= 5 and parts[0].lower() == 'tcp':
        pid = parts[4]
        # Search for the PID in the tasklist output to find the corresponding program name
        program_line = next((p for p in tasklist_output.splitlines() if pid in p), None)
        if program_line:
            program_name = program_line.split()[0]
            print(f"{pid}   {program_name}")
        else:
            print(f"{pid}   Unknown Program")
