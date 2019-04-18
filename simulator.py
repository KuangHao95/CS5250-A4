'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import copy
import queue 

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.burst_time_bak = burst_time
        self.compare = None
        self.first_call = None
        self.finish_time = None
        self.predicted_burst = None

    def amount_waited(self):
        return self.finish_time - self.arrive_time - self.burst_time_bak

    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

    def __lt__(self, other):
        #return self.burst_time < other.burst_time
        return self.compare(self, other)

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time

def RR_scheduling(process_list, time_quantum):
    # Create deep copy to keep process_list intact
    mymymy_process_list = copy.deepcopy(process_list)
    schedule = []
    current_time = 0
    waiting_time = 0

    while len(mymymy_process_list) > 0:
        flag = 0
        for process in mymymy_process_list:
            if process.burst_time > 0:
                if current_time >= process.arrive_time:
                    schedule.append((current_time, process.id))
                    if process.last_scheduled_time == 0:
                        waiting_time += current_time - process.arrive_time
                    else:
                        waiting_time += current_time - process.last_scheduled_time

                    if process.burst_time > time_quantum:
                        temp_time = time_quantum
                    else: 
                        temp_time = process.burst_time
                    current_time += temp_time
                    flag = 1
                    process.last_scheduled_time = current_time
                    process.burst_time -= temp_time
                    if process.burst_time <= 0:
                        mymymy_process_list.remove(process)
        if flag == 0:
            current_time = mymymy_process_list[0].arrive_time

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time


def SRTF_scheduling(process_list):
    # Create deep copy to keep process_list intact
    mymy_process_list = copy.deepcopy(process_list)
    Done_q = queue.Queue()
    Run_q = queue.PriorityQueue()
    schedule = []
    previous = -1
    waiting_time = 0
    current_process = None

    for t in range(-1, 250):
        for process in mymy_process_list:
            if process.arrive_time == t:   
                process.compare = lambda x,y: x.burst_time < y.burst_time
                Run_q.put(process)

        if (not Run_q.empty()):
            current_process = Run_q.get_nowait()
            if previous != current_process.id:
                schedule.append((t, current_process.id))
            if current_process.first_call != None:
                current_process.first_call = t

        if current_process != None:
            current_process.burst_time -= 1
            if current_process.burst_time  == 0:
                current_process.finish_time = t
                Done_q.put(current_process)
            else:
                Run_q.put(current_process)
            previous = current_process.id
            current_process = None

    for process in mymy_process_list:
        waiting_time += process.amount_waited() + 1
    average_waiting_time = waiting_time / float(len(process_list))
    return (schedule, average_waiting_time)


def SJF_scheduling(process_list, alpha):
    # Create deep copy to keep process_list intact
    my_process_list = copy.deepcopy(process_list)
    Done_q = queue.Queue()
    Run_q = queue.PriorityQueue()
    current_process = None
    schedule = []
    waiting_time = 0
    process_pred = [5 ,5 ,5 ,5]

    for t in range(-1, 250):
        for process in my_process_list:
            if process.arrive_time == t:
                process.predicted_burst = process_pred[process.id]
                process_pred[process.id] = alpha * process.burst_time + (1 - alpha)* process_pred[process.id]
                process.compare = lambda x,y: x.predicted_burst < y.predicted_burst
                Run_q.put(process)
            
        if current_process != None and current_process.burst_time > 0:
            prev_id = current_process.id
            current_process.burst_time -= 1
        elif current_process != None:
            current_process.finish_time = t
            Done_q.put(current_process)
            current_process = None

        if (not Run_q.empty() and current_process == None):
            current_process = Run_q.get_nowait()
            schedule.append((t, current_process.id))
            current_process.burst_time -= 1

    for process in my_process_list:
        waiting_time += process.amount_waited()
    average_waiting_time = waiting_time / float(len(process_list))
    return (schedule,average_waiting_time)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 10)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )


if __name__ == '__main__':
    main(sys.argv[1:])
    