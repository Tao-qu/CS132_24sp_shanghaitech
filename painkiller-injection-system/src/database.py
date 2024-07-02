import time
bolus_amount = 0.2
baseline_amount = 0.01
baseline_timeline_list = []
bolus_timeline_list = []
initial_time = 0
current_time = 0
time_speed = 0

# injection_enable = 1

switch_on = 0


def calculate_1_h(baseline_list, bolus_list, time_):
    current_time = time_
    sum_ = 0
    ex_time = current_time-24
    if (len(baseline_list) == 0):
        pass
    elif (len(baseline_list) == 1):
        sum_ += 150*min(float(24), current_time -
                        baseline_list[0][0])*baseline_list[0][1]/60
    else:
        for i in range(len(baseline_list)-1):
            if (i == len(baseline_list)-2):
                if (baseline_list[i][0] < ex_time and baseline_list[i+1][0] < ex_time):
                    sum_ += 150*baseline_list[i][1] * \
                        (baseline_list[i+1][0]-ex_time)/60
                    sum_ += 150*float(24)*baseline_list[i+1][1]/60
                elif (baseline_list[i][0] < ex_time):
                    sum_ += 150*baseline_list[i][1]*(
                        baseline_list[i+1][0]-ex_time)/60
                    sum_ += 150*(current_time -
                                 baseline_list[i+1][0])*baseline_list[i+1][1]/60
                else:
                    sum_ += 150*baseline_list[i][1]*(
                        baseline_list[i+1][0]-baseline_list[i][0])/60
                    sum_ += 150*(current_time -
                                 baseline_list[i+1][0])*baseline_list[i+1][1]/60
            elif (baseline_list[i+1][0] < ex_time):
                continue

            elif (baseline_list[i][0] < ex_time):
                sum_ += 150*baseline_list[i][1] * \
                    (baseline_list[i+1][0]-ex_time)/60
            else:
                sum_ += 150*baseline_list[i][1]*(
                    baseline_list[i+1][0]-baseline_list[i][0])/60

    for i in range(len(bolus_list)):
        if (bolus_list[i][0] < ex_time):
            continue
        else:
            sum_ += bolus_list[i][1]

    return sum_


def calculate_24_h(baseline_list, bolus_list, time_):
    current_time = time_
    sum_ = 0
    ex_time = current_time-24*24
    if (len(baseline_list) == 0):
        pass
    elif (len(baseline_list) == 1):
        sum_ += 150*min(float(24*24), current_time -
                        baseline_list[0][0])*baseline_list[0][1]/60
    else:
        for i in range(len(baseline_list)-1):
            if (i == len(baseline_list)-2):
                if (baseline_list[i][0] < ex_time and baseline_list[i+1][0] < ex_time):
                    sum_ += 150*baseline_list[i][1] * \
                        (baseline_list[i+1][0]-ex_time)/60
                    sum_ += 150*float(24*24)*baseline_list[i+1][1]/60
                elif (baseline_list[i][0] < ex_time):
                    sum_ += 150*baseline_list[i][1]*(
                        baseline_list[i+1][0]-ex_time)/60
                    sum_ += 150*(current_time -
                                 baseline_list[i+1][0])*baseline_list[i+1][1]/60
                else:
                    sum_ += 150*baseline_list[i][1]*(
                        baseline_list[i+1][0]-baseline_list[i][0])/60
                    sum_ += 150*(current_time -
                                 baseline_list[i+1][0])*baseline_list[i+1][1]/60
            elif (baseline_list[i+1][0] < ex_time):
                continue

            elif (baseline_list[i][0] < ex_time):
                sum_ += 150*baseline_list[i][1] * \
                    (baseline_list[i+1][0]-ex_time)/60
            else:
                sum_ += 150*baseline_list[i][1]*(
                    baseline_list[i+1][0]-baseline_list[i][0])/60

    for i in range(len(bolus_list)):
        if (bolus_list[i][0] < ex_time):
            continue
        else:
            sum_ += bolus_list[i][1]

    return sum_
