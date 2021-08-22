import math

import IO_Manager

x = {}
# takes input file, and puts it in the variable "x" above
# once used all variables in dictionary x will be updated autonomously
# format for input file
# variable = value
# variable2 = value
def read_input(file):
    with open(file) as f:
        global x
        split = []
        for line in f:
            try:
                # copy
                split = (line.split(' = '))
                # reformat
                split[1] = split[1].strip('\n')
                split[1] = float(split[1])
                # insert
                x.update({split[0]: split[1]})
            except Exception as error:
                print(error) # I tried main.py and there was no error???
                continue


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


# this will define swirl injuector
def simpleswirl(output):
    global value
    spray_angle = x['spray_angle']
    mass_flow_rate = x['mass_flow_rate']
    density = x['density']
    pressure_drop = x['pressure_drop']
    inlet_quantity = x['inlet_quantity']
    kinematic_viscosity = x['kinematic_viscosity']
    #Geometry Coefficients
    inlet_ratio = x['inlet_ratio'] #typically 3-6 (d=4) Larger means Thicker inlet passages
    vortex_length_ratio = x['vortex_ratio'] #typically ls>2Rin (d=2) smaller the shorter
    length_to_diameter = x['length_to_diameter']
    #Step 1
    #this method is not infinitely expandable, I Hate It !!!
    if (length_to_diameter == float(2.0)):
        geometric_characteristic = IO_Manager.graph_to_value(spray_angle, '2a_A,l=2')
    elif (length_to_diameter == float(0.5)):
        geometric_characteristic = IO_Manager.graph_to_value(spray_angle, '2a_A,l=0.5')
    else:
        print('error, Length to diameter is outside dataset')
    flow_coefficient = IO_Manager.graph_to_value(geometric_characteristic, 'A_mu')
    #Step 2
    nozzle_radius = 0.475 * math.sqrt(mass_flow_rate / (flow_coefficient * math.sqrt(density * pressure_drop)))
    #step 3
    inlet_spacing_radius = nozzle_radius
    inlet_radius = math.sqrt((inlet_spacing_radius * nozzle_radius) / (inlet_quantity * geometric_characteristic))
    #Step 5
    inlet_velocity = mass_flow_rate / (inlet_quantity * math.pi * (inlet_radius ** 2) * density)
    reynolds_number = (inlet_velocity * inlet_radius * 2 * math.sqrt(inlet_quantity)) / kinematic_viscosity
    if reynolds_number < 10000:
        print("error, Reynolds Number too low")
        print(f"{reynolds_number} < 10000")
    #Step 5
    swirloutput = {}
    swirloutput['reynolds_number'] = reynolds_number
    swirloutput['nozzle_radius'] = nozzle_radius * 100
    swirloutput['inlet_radius'] = inlet_radius*100
    swirloutput['inlet_length'] = inlet_ratio * inlet_radius*100
    swirloutput['vortex_length'] = vortex_length_ratio * inlet_spacing_radius*100
    swirloutput['vortex_radius'] = (inlet_spacing_radius + inlet_radius)*100
    swirloutput['nozzle_length'] = length_to_diameter * 2 * nozzle_radius*100
    swirloutput['inlet_velocity']= inlet_velocity
    swirloutput['flow_coefficient'] = flow_coefficient
    swirloutput['geometric_characteristic'] = geometric_characteristic
    IO_Manager.write_output(swirloutput, output, False)
    return ()
