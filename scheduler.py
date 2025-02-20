from collections import deque

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1

        # Human code
        self.selected_times = []
        self.remaining_burst = []

class InputData:
    def __init__(self, name, quantum, runfor, numProcesses, processes):
        self.scheduler = name
        self.quantum = quantum
        self.runfor = runfor
        self.numProcesses = numProcesses
        self.processes = processes

class OutputHolder:
    def __init__(self, section1="", section2="", section3=""):
        self.outputSection1 = section1
        self.outputSection2 = section2
        self.outputSection3 = section3

# Schedulers
def fcfs_scheduler(processes, runfor):
    # Human Code
    sorted_processes = processes.copy()
    sorted_processes.sort(key=lambda p: p.arrival_time)  # Sort by arrival time
    current_time = 0
    for process in sorted_processes:
        if current_time >= runfor:
            break  # Stop execution if max allowed time is reached
        
        if current_time < process.arrival_time:
            current_time = process.arrival_time  # CPU is idle until the process arrives
        
        process.start_time = current_time
        process.selected_times.append(current_time)
        process.remaining_burst.append(process.burst_time)
        process.completion_time = min(current_time + process.burst_time, runfor)
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time
        
        current_time = process.completion_time  # Move current time forward

def round_robin_scheduling(processes, quantum, total_time):
    queue = deque()
    time = 0
    process_index = 0
    n = len(processes)
    remaining = n
    
    sorted_processes = processes.copy() # added
    sorted_processes.sort(key=lambda p: p.arrival_time)# added

    while time < total_time:
        while process_index < n and sorted_processes[process_index].arrival_time <= time:
            queue.append(process_index)
            process_index += 1
        
        if queue:
            idx = queue.popleft()
            process = sorted_processes[idx]
            
            if process.response_time == -1:
                process.response_time = time - process.arrival_time

            if process.start_time < 0: # added
                process.start_time = time # added
            
            process.selected_times.append(time) # added
            execution_time = min(quantum, process.remaining_time)
            time += execution_time
            process.remaining_time -= execution_time
            process.remaining_burst.append(process.burst_time - quantum * len(process.remaining_burst)) # added
            
            while process_index < n and sorted_processes[process_index].arrival_time <= time:
                queue.append(process_index)
                process_index += 1
            
            if process.remaining_time == 0:
                process.completion_time = time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                remaining -= 1
            else:
                queue.append(idx)
        else:
            time += 1

# Output
def format_scheduler_info(scheduler_info):
    if scheduler_info.scheduler == "rr":
        scheduler_name = "Using Round-Robin"
    elif scheduler_info.scheduler == "fcfs":
        scheduler_name = "Using First-Come First-Served"
    elif scheduler_info.scheduler == "sjf":
        scheduler_name = "Using preemptive Shortest Job First"
    else:
        scheduler_name = ""
    
    return f"{scheduler_info.numProcesses} processes", scheduler_name

def get_quantum_info(scheduler_info):
    if scheduler_info.scheduler == "rr":
        return f"Quantum   {scheduler_info.quantum}\n\n"
    return ""

def create_log(input_data):
    time = 0
    processes = input_data.processes[:]
    log = []
    running_process = False
    current_process = None

    while time < input_data.runfor:

        if running_process and current_process.completion_time == time:
                log.append(f"Time {time:3} : {current_process.name} finished")
                current_process = None
                running_process = False
        
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == time:
                log.append(f"Time {time:3} : {process.name} arrived")
            
            if len(process.selected_times) > 0 and process.selected_times[0] == time:
                log.append(f"Time {time:3} : {process.name} selected (burst   {process.remaining_burst[0]})")
                del process.selected_times[0]
                del process.remaining_burst[0]
                current_process = process
                running_process = True
        
        if not running_process:
            log.append(f"Time {time:3} : Idle")
        # Select process (if not already running)
        # if running_process is None:
        #     for process in processes:
        #         if process.selected_t
        #         if process.arrival_time <= time and process.remaining_time > 0:
        #             running_process = process
        #             log.append(f"Time {time:3} : {process.name} selected (burst {process.remaining_time})")
        #             break
        
        # If there is a running process, update it
        # if running_process:
        #     running_process.remaining_time -= 1
        #     running_process.selected_times.append(time)
        #     running_process.remaining_burst.append(running_process.remaining_time)

        #     if running_process.remaining_time == 0:
        #         log.append(f"Time {time + 1:3} : {running_process.name} finished")
        #         running_process = None
        
        # # If no process is running, log Idle
        # if running_process is None and not any(process.arrival_time <= time and process.remaining_time > 0 for process in processes):
        #     log.append(f"Time {time:3} : Idle")

        time += 1

    log.append(f"Finished at time {time}")
    return "\n".join(log)

def calculate_metrics(input_data):
    log = []
    
    for process in input_data.processes:
        # Use the pre-calculated times from the process object
        waiting_time = process.waiting_time
        turnaround_time = process.turnaround_time
        response_time = process.response_time
        
        # Prepare the log string
        log.append(f"{process.name} wait {waiting_time:3} turnaround {turnaround_time:3} response {response_time:3}")
    
    return "\n".join(log)

# Generates string to be placed in file
def getResultText(inputData):
    outputHandler = OutputHolder()
    numProcessText, schedulerNameText = format_scheduler_info(inputData)
    quantumText = get_quantum_info(inputData)
    outputString1 = numProcessText + "\n" + schedulerNameText + "\n" + quantumText

    schedulerLog = create_log(inputData)

    processMetrics = calculate_metrics(inputData)

    outputHandler.outputSection1 = outputString1
    outputHandler.outputSection2 = schedulerLog
    outputHandler.outputSection3 = processMetrics

    return outputHandler.outputSection1 + outputHandler.outputSection2 + "\n\n" + outputHandler.outputSection3


# IGNORE EVERYTHING BELOW (TESTING)
def InputTest():
    # will be done by reading file
    scheduler = "rr"
    quantum = 2
    runfor = 20
    numProcesses = 2
    process_list = [
        Process("P1", 0, 5),
        Process("P2", 7, 9)
        ]
    
    # up above should be determined by reading file
    inputData = InputData(scheduler, quantum, runfor, numProcesses, process_list)

    if (inputData.scheduler == "rr"):
        round_robin_scheduling(inputData.processes, inputData.quantum, inputData.runfor)
    elif (inputData.scheduler == "fcfs"):
        fcfs_scheduler(inputData.processes, inputData.runfor)

    output = getResultText(inputData)

    print(output)

InputTest()