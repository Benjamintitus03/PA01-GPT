import heapq
from collections import deque
import sys
import os

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

def round_robin_scheduling(processes, quantum, total_time, output_file):
    # Open the output file for writing
    with open(output_file, 'w') as file:
        queue = deque()
        time = 0
        process_index = 0
        n = len(processes)
        remaining = n
        
        processes.sort(key=lambda p: p.arrival_time)
        file.write(f"  {n} processes\n")
        file.write("Using Round-Robin\n")
        file.write(f"Quantum   {quantum}\n\n")
        
        while time < total_time:
            while process_index < n and processes[process_index].arrival_time <= time:
                file.write(f"Time {time:3} : {processes[process_index].name} arrived\n")
                queue.append(process_index)
                process_index += 1
            
            if queue:
                idx = queue.popleft()
                process = processes[idx]
                
                if process.response_time == -1:
                    process.response_time = time - process.arrival_time
                
                execution_time = min(quantum, process.remaining_time)
                file.write(f"Time {time:3} : {process.name} selected (burst {process.remaining_time:3})\n")
                time += execution_time
                process.remaining_time -= execution_time
                
                while process_index < n and processes[process_index].arrival_time <= time:
                    file.write(f"Time {time:3} : {processes[process_index].name} arrived\n")
                    queue.append(process_index)
                    process_index += 1
                
                if process.remaining_time == 0:
                    process.completion_time = time
                    file.write(f"Time {time:3} : {process.name} finished\n")
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    remaining -= 1
                else:
                    queue.append(idx)
            else:
                file.write(f"Time {time:3} : Idle\n")
                time += 1
        
        file.write(f"Finished at time  {total_time}\n\n")
        print_results(processes, file)

def print_results(processes, output_file):
    for p in sorted(processes, key=lambda p: p.name):
        output_file.write(f"{p.name} wait {p.waiting_time:3} turnaround {p.turnaround_time:3} response {p.response_time:3}\n")

# Sample input parsing
def parse_input(input_lines):
    processes = []
    quantum = 0
    total_time = 0

    for line in input_lines:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "processcount":
            continue
        elif parts[0] == "runfor":
            total_time = int(parts[1])
        elif parts[0] == "use":
            continue  # This implementation assumes Round Robin
        elif parts[0] == "quantum":
            quantum = int(parts[1])
        elif parts[0] == "process":
            name = parts[2]
            arrival = int(parts[4])
            burst = int(parts[6])
            processes.append(Process(name, arrival, burst))

    return processes, quantum, total_time

# Main function
def main():
    if len(sys.argv) < 2:
        print("Please provide an input file as an argument.")
        return

    input_file = sys.argv[1]
    
    # Generate output file name by appending '.out' to the input file name
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}.out"

    with open(input_file, 'r') as file:
        input_lines = file.readlines()

    processes, quantum, total_time = parse_input(input_lines)
    round_robin_scheduling(processes, quantum, total_time, output_file)

if __name__ == "__main__":
    main()
