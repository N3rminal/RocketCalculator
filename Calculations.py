import math

import IO_Manager

x = {}


# this function will take an input file and convert it to the dictionary
# once used all variables in dictionary x will be updated autonomously
# format for input file
# variable = value
# variable2 = value
def read_input(file):
    with open(file) as f:
        dictionary = {}
        split = []
        for line in f:
            try:
                # copy
                split = (line.split(' = '))
                # reformat
                split[1] = split[1].strip('\n')
                split[1] = float(split[1])
                # insert
                dictionary.update({split[0]: split[1]})
            except:
                continue
    return dictionary


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

#this solves for needed spray angle and works bacwards
def regress_coaxswirl():
    # define dictionaries
    s1 = read_input('first_stage')
    s2 = read_input('second_stage')
    # 1.1 Determine Spray Geometric Characteristic and Flow coefficient
    f_name = 'Data/2a_A,l='
    f_name += str(s1['length_to_radius'])
    s1['geometric_characteristic'] = IO_Manager.graph_to_value(s1['spray_angle'], f_name, 0)
    f_name = 'Data/A_mu,C='
    f_name += str(s1['opening_coefficient'])
    s1['flow_coefficient'] = IO_Manager.graph_to_value(s1['geometric_characteristic'], f_name, 0)

    # 1.2 Calculate Nozzle Radius
    s1['nozzle_radius'] = 0.475 * math.sqrt(s1['mass_flow_rate'] / (s1['flow_coefficient'] * math.sqrt(s1['density'] * s1['pressure_drop'])))

    # 1.3 Determine Inlet dimentions
    s1['inlet_spacing_radius'] = s1['nozzle_radius']
    s1['inlet_radius'] = math.sqrt((s1['inlet_spacing_radius'] * s1['nozzle_radius']) / (s1['inlet_quantity'] * s1['geometric_characteristic']))
    s1['inlet_length'] = s1['inlet_ratio'] * s1['inlet_radius']

    # 1.4 Determine Essential flow characteristics such as renolds number
    s1['inlet_velocity'] = s1['mass_flow_rate'] / (s1['inlet_quantity'] * math.pi * (s1['inlet_radius'] ** 2) * s1['density'])
    print('inlet_velocity = ',s1['inlet_velocity'])
    s1['reynolds_number'] = (s1['inlet_velocity'] * s1['inlet_radius'] * 2 * math.sqrt(s1['inlet_quantity'])) / s1['kinematic_viscosity']
    if s1['reynolds_number'] < 10000:
        print("error, Reynolds Number too low")
        print(s1['reynolds_number'], '<10000')

    #determine outside nozzle radius
    s1['outside_radius'] = s1['wall_thickness'] + s1['nozzle_radius']
    s2['nozzle_spacing'] = 0.002
    s2['liquid_vortex_radius'] = 100000
    while s2['nozzle_spacing'] < s2['liquid_vortex_radius']:
        # determine Nozzle radius via iteration
        s2['nozzle_spacing'] += 0.001
        s2['nozzle_radius'] = s1['outside_radius'] + s2['nozzle_spacing']

        # 2.1 Determine flow coefficient required for specified pressure drop
        s2['flow_coefficient'] = (s2['mass_flow_rate']*math.sqrt(s2['density']*s2['pressure_drop'])*361)/((s2['density']*s2['pressure_drop'])*1600*s2['nozzle_radius']**2)

        # 2.2 Determine Geometric characteristic for given nozzle ratio
        f_name = 'Data/A_mu,C='
        f_name += str(s2['opening_coefficient'])
        s2['geometric_characteristic'] = IO_Manager.graph_to_value(s2['flow_coefficient'], f_name, 1)

        # 2.3 Determine Spray angle given Nozzle length coefficient
        f_name = 'Data/2a_A,l='
        f_name += str(s2['length_to_radius'])
        temp_spray = IO_Manager.graph_to_value(s2['geometric_characteristic'], f_name, 1)

        #2.4 Determine liquid vortex level
        f_name = 'Data/A_R,Rin='
        f_name += str(s2['opening_coefficient'])
        s2['liquid_vortex_radius'] = IO_Manager.graph_to_value(s2['geometric_characteristic'], f_name, 0)*s2['nozzle_radius']
    s2['spray_angle'] = temp_spray
    print(s2['spray_angle'])
    max_offset = (s2['nozzle_radius']-s1['nozzle_radius'])/(math.tan((s1['spray_angle']/2) * math.pi / 180))

    #finding inlet dimentions for second chamber
    s2['inlet_spacing_radius'] = s2['nozzle_radius']
    s2['inlet_radius'] = math.sqrt((s2['inlet_spacing_radius'] * s2['nozzle_radius']) / (s2['inlet_quantity'] * s2['geometric_characteristic']))
    s2['inlet_length'] = s2['inlet_ratio'] * s2['inlet_radius']

    # finding Chamber 2 dimentions
    s2['nozzle_length'] = s2['length_to_radius'] * s2['nozzle_radius']
    s2['vortex_length'] = s2['vortex_ratio'] * s2['inlet_spacing_radius']
    s2['vortex_radius'] = s2['inlet_radius']+s2['inlet_spacing_radius']
    s2['total_length'] =s2['vortex_length'] + s2['inlet_radius'] + s2['nozzle_length']
    print(s2['total_length'])

    #finding Chamber 1 Dimentions
    s1['nozzle_length'] = s1['length_to_radius'] * s1['nozzle_radius']
    print(s1['nozzle_length']+max_offset)
    return ()


# this will define swirl injuector
def simpleswirl(input, output):
    x = read_input(input)
    spray_angle = x['spray_angle']
    mass_flow_rate = x['mass_flow_rate']
    density = x['density']
    pressure_drop = x['pressure_drop']
    inlet_quantity = x['inlet_quantity']
    kinematic_viscosity = x['kinematic_viscosity']
    # Geometry Coefficients
    inlet_ratio = x['inlet_ratio']  # typically 3-6 (d=4) Larger means Thicker inlet passages
    vortex_length_ratio = x['vortex_ratio']  # typically ls>2Rin (d=2) smaller the shorter
    length_to_radius = x['length_to_radius']  # data with 0.5 or 2 the larger this value, the longer the chamber
    # Step 1
    # this method is not infinitely expandable, I Hate It !!!
    f_name = 'Data/2a_A,l='
    f_name += str(length_to_radius)
    geometric_characteristic = IO_Manager.graph_to_value(spray_angle, f_name)
    flow_coefficient = IO_Manager.graph_to_value(geometric_characteristic, 'Data/A_mu')
    # Step 2
    nozzle_radius = 0.475 * math.sqrt(mass_flow_rate / (flow_coefficient * math.sqrt(density * pressure_drop)))
    # step 3
    inlet_spacing_radius = nozzle_radius
    inlet_radius = math.sqrt((inlet_spacing_radius * nozzle_radius) / (inlet_quantity * geometric_characteristic))
    # Step 5
    inlet_velocity = mass_flow_rate / (inlet_quantity * math.pi * (inlet_radius ** 2) * density)
    reynolds_number = (inlet_velocity * inlet_radius * 2 * math.sqrt(inlet_quantity)) / kinematic_viscosity
    if reynolds_number < 10000:
        print("error, Reynolds Number too low")
        print(reynolds_number, '<10000')
    # Step 5
    swirloutput = {}
    swirloutput['reynolds_number'] = reynolds_number
    swirloutput['nozzle_radius'] = nozzle_radius * 100
    swirloutput['inlet_radius'] = inlet_radius * 100
    swirloutput['inlet_length'] = inlet_ratio * inlet_radius * 100
    swirloutput['vortex_length'] = vortex_length_ratio * inlet_spacing_radius * 100
    swirloutput['vortex_radius'] = (inlet_spacing_radius + inlet_radius) * 100
    swirloutput['nozzle_length'] = length_to_radius * 2 * nozzle_radius * 100
    swirloutput['inlet_velocity'] = inlet_velocity
    swirloutput['flow_coefficient'] = flow_coefficient
    swirloutput['geometric_characteristic'] = geometric_characteristic
    IO_Manager.write_output(swirloutput, output, 0)
    return ()

#this currently DOES NOT WORK!!!!
#geometric characteristic has a horrible habit of walking to 0.5 for some damn reason
def complex_swirl(input):
    # 1. Prescribe spray cone angle
    s = read_input(input)
    # 2. Determine Geometric Characteristic
    s['geometric_characteristic'] = IO_Manager.graph_to_value(s['spray_angle'],'Data/f2a_A')
    # 3. Determine Flow coefficient
    s['flow_coefficient'] = IO_Manager.graph_to_value(s['geometric_characteristic'], 'Data/fA_mu')
    temp_nozzle = 1
    s['nozzle_radius'] = 0.475 * math.sqrt(s['mass_flow_rate'] / (s['flow_coefficient'] * math.sqrt(s['density'] * s['pressure_drop'])))
    s['inlet_spacing_radius'] = s['nozzle_radius']
    # 5. Determine Inlet conditions
    s['inlet_radius'] = math.sqrt((s['inlet_spacing_radius'] * s['nozzle_radius']) / (s['inlet_quantity'] * s['geometric_characteristic']))
    while temp_nozzle != s['nozzle_radius']:
        # 4. Determine Nozzle and coefficient of opening
        temp_nozzle = s['nozzle_radius']
        s['inlet_radius'] = math.sqrt((s['inlet_spacing_radius'] * s['nozzle_radius']) / (s['inlet_quantity'] * s['geometric_characteristic']))
        # 6. Revise Chamber parameters
        s['inlet_length'] = s['inlet_ratio'] * s['inlet_radius']
        s['nozzle_length'] = s['length_to_radius']* s['nozzle_radius']
        s['vortex_length'] = s['vortex_ratio']*s['inlet_spacing_radius']
        s['vortex_radius'] = s['inlet_spacing_radius']+s['inlet_radius']
        # 7. Find Reynolds Number and friction coefficient
        s['inlet_Reynolds_number'] = 0.637 * (s['mass_flow_rate']/(math.sqrt(s['inlet_quantity'])*s['inlet_radius']*s['density']*s['kinematic_viscosity']))
        s['friction_coefficient'] = 0.3164/(s['inlet_Reynolds_number']**0.25)
        # 8. Determine Equivalents
        s['geometric_equivalent'] = (s['inlet_spacing_radius'] * s['nozzle_radius']) / ((s['inlet_quantity'] * (s['inlet_radius'] ** 2)) + ((s['friction_coefficient'] / 2) * s['inlet_spacing_radius']  * (s['inlet_radius'] - s['nozzle_radius'])))
        s['flow_equivalent'] = IO_Manager.graph_to_value(s['geometric_equivalent'], 'Data/fA_mu')
        s['spray_equivalent'] = IO_Manager.graph_to_value(s['geometric_equivalent'], 'Data/fA_2a')
        # 8. Calculate inlet losses
        s['internal_tilt_angle'] = 90-math.degrees(math.atan(s['vortex_radius']/s['inlet_length']))
        s['inlet_loss'] = (s['internal_tilt_angle'] / (0 - 150)) + 1.1
        # Calculate Hydrolic Loss
        s['hydrolic_loss'] = s['inlet_loss'] + (s['friction_coefficient']*(s['inlet_length']/(2*s['inlet_radius'])))
        # 9. Calculate Actual Flow Coefficient and area/repeat
        s['flow_coefficient'] = s['flow_equivalent']/math.sqrt(1+(s['hydrolic_loss']*(s['flow_coefficient']**2)*((s['geometric_characteristic']**2)/((s['inlet_spacing_radius']/s['nozzle_radius'])**2))))
        s['nozzle_radius'] = 0.475 * math.sqrt(s['mass_flow_rate'] / (s['flow_coefficient'] * math.sqrt(s['density'] * s['pressure_drop'])))
        # 5. Determine Inlet conditions
        s['geometric_characteristic'] = IO_Manager.graph_to_value(s['spray_equivalent'],'Data/f2a_A')
        #s['geometric_characteristic'] = (s['inlet_radius'] * s['nozzle_radius']) / (s['inlet_quantity'] * s['inlet_radius'] ** 2)
        print(s['geometric_characteristic'])
    print('results')
    print('nozzle_radius = ',s['nozzle_radius']*100)
    print('inlet_radius = ',s['inlet_radius']*100)
    print('inlet_length = ',s['inlet_length']*100)
    print('vortex_length = ',s['vortex_length']*100)
    print('vortex_radius = ',s['vortex_radius']*100)
    print('nozzle_length = ',s['nozzle_length']*100)
    print('flow_coefficient = ',s['flow_coefficient'])
    print('geometric_characteristic = ',s['geometric_characteristic'])
