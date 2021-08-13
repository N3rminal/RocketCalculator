# import Required addons
import csv
import math

# initiate dictionary
x = {}

# takes a line from an input file
#
# example:
# first_prime = 2
#
# returns:
# ["first_prime", "2"]
def format_input_line(line):
    split = (line.split(' = ')) # copy
    split[1] = split[1].strip('\n') # reformat
    return split

# this function will take an input file and convert it to the dictionary
# once used all variables in dictionary x will be updated autonomously
#
# format for input file:
# <variable> = <value>
#
# example:
# first_prime = 2
def read_input(file):
    with open(file) as f:
        global x
        for line in f:
            split = format_input_line(line)
            split[1] = float(split[1])
            # insert
            x.update({split[0]: split[1]})
    return ()

# THIS IS USEFUL DO NOT DELETE
def getkeys(dictionary):
    return [*dictionary]

# allows to write dictionary(data) to file(file). If clear is 1 then the previous data is not carried over, if 0 then it only overwrites what is in dictionary(data)
def write_output(data, file, clear):
    def write_to_file(data, file):
        with open(file, 'w') as f:
            for i in keys:
                text = f"{i} = {data[i]}\n"
                f.write(text)

    keys = getkeys(data)
    if clear == 1:
        write_to_file(data, file)
    else:
        # this is totally reused shitty code, will it cause unnecisary slowdowns? YES! do I care? HELL NO
        split = []
        with open(file) as f:
            for line in f:
                split = format_input_line(line)
                # insert
                # finding if the key in dictionary is occupied
                try:
                    unused = data[split[0]]
                except:
                    x.update({split[0]: split[1]})
                else:
                    continue
                data.update({split[0]: split[1]})
            print(data)

        write_to_file(data, file)
    return ()


# This function converts input csv file to a matrix (list of list)
# Input should be inserted to desending order (however asending should work but I am too lazy to verify that)
def graph_to_value(value, dataset):
    # Import Data points
    p = 0
    p2 = 0
    data = []
    f = open(dataset, 'r')
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

    # convert string to float
    n = 0
    while n < len(data):
        data[n][0] = float(data[n][0])
        data[n][1] = float(data[n][1])
        n = n + 1

    # close file
    f.close()

    # find closest datapoint
    for i in range(len(data)):
        if i > 0:
            if value > data[0][0]:
                print("error, X-Axis Too High")
                break
            if abs(value - data[i][0]) > abs(value - data[i - 1][0]):
                p = i - 1
                break
    # find second closest datapoint
    if value > data[p][0]:
        p2 = p - 1
    else:
        p2 = p + 1
    # calculate the line between points y=mx+b
    # m=(y2-y1)/(x2-x1)
    m = (data[p2][1] - data[p][1]) / (data[p2][0] - data[p][0])
    # b=y-m*x
    b = data[p][1] - (m * data[p][0])
    # plug in x
    return (m * value + b)


# This will calculate Tank parameters
def tank():
    return ()


# This will define plumbing and pipe size
def pipe():
    return ()


# This will calculate autogonous pressurization system
def auto_pressure():
    return ()


# This will calculate Combustion conditions
def combustion():
    return ()


# This will calculate nozzle parameters
def nozzle():
    return ()


# This will define cooling system
def cooling():
    return ()


# this will define swirl injuector\
def simpleswirl():
    spray_angle = x['spray_angle']
    mass_flow_rate = x['mass_flow_rate']
    density = x['density']
    pressure_drop = x['pressure_drop']
    inlet_quantity = x['inlet_quantity']
    kinematic_viscosity = x['kinematic_viscosity']
    geometric_characteristic = graph_to_value(spray_angle, '2a_A')
    flow_coefficient = graph_to_value(geometric_characteristic, 'A_mu')
    nozzle_radius = 0.475 * math.sqrt(mass_flow_rate / (flow_coefficient * math.sqrt(density * pressure_drop)))
    inlet_spacing_radius = nozzle_radius
    inlet_radius = math.sqrt((inlet_spacing_radius * nozzle_radius) / (inlet_quantity * geometric_characteristic))
    inlet_velocity = mass_flow_rate / (inlet_quantity * math.pi * (inlet_radius ** 2) * density)
    reynolds_number = (inlet_velocity * inlet_radius * 2 * math.sqrt(inlet_quantity)) / kinematic_viscosity
    if reynolds_number < 10000:
        print("error, Reynolds Number too low")
    nozzle_length = 2 * nozzle_radius
    inlet_length = 4 * inlet_radius
    vortex_length = 1.5 * inlet_spacing_radius
    vortex_radius = inlet_spacing_radius + inlet_radius
    print('nozzle radius = ', nozzle_radius * 100)
    print('inlet radius = ', inlet_radius * 100)
    print('inlet length', inlet_length * 100)
    print('vortex_lenght', vortex_length * 100)
    print('Vortex Radius', vortex_radius * 100)
    print('nozzle length = ', nozzle_length * 100)
    print('flow coefficient = ', flow_coefficient)
    return ()


# Main Script Goes here

