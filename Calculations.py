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
    s1 = read_input('central_coax_chamber_output')
    s2 = read_input('outside_coax_chamber_output')
    # 1.1 Determine Spray Geometric Characteristic and Flow coefficient
    f_name = 'Data/2a_A,l='
    f_name += str(s1['length_to_radius'])
    s1['geometric_characteristic'] = IO_Manager.graph_to_value(s1['spray_angle'], f_name, 0)
    f_name = 'Data/A_mu,C='
    f_name += str(s1['opening_coefficient'])
    s1['flow_coefficient'] = IO_Manager.graph_to_value(s1['geometric_characteristic'], f_name, 0)

    # 1.2 Calculate Nozzle Radius
    s1['nozzle_radius'] = 0.475 * math.sqrt(s1['mass_flow_rate'] / (s1['flow_coefficient'] * math.sqrt(s1['density'] * s1['pressure_drop'])))

    # finding Chamber 1 Dimentions
    s1['nozzle_length'] = s1['length_to_radius'] * s1['nozzle_radius']
    s1['vortex_length'] = s1['vortex_ratio'] * s1['swiling_arm']
    s1['vortex_radius'] = s1['inlet_radius'] + s1['swiling_arm']
    s1['total_length'] = s1['vortex_length'] + s1['inlet_radius'] + s1['nozzle_length']
    s1['nozzle_radius'] = s1['nozzle_radius']

    # 1.3 Determine Inlet dimentions
    s1['swiling_arm'] = s1['nozzle_radius']
    s1['inlet_radius'] = math.sqrt((s1['swiling_arm'] * s1['nozzle_radius']) / (s1['inlet_quantity'] * s1['geometric_characteristic']))
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
    s2['liquid_vortex_radius'] = 0
    s2['minimum_chamber_dradius'] = 1
    s2['reynolds_number'] = 0
    s2['nozzle_radius'] = 0
    s2['flow_coefficient'] = 0
    s2['geometric_characteristic'] = 0
    s2['swiling_arm'] = 0
    s2['inlet_radius'] = 0
    s2['inlet_length'] = 0

    # finding Chamber 2 dimentions
    s2['nozzle_length'] = s2['length_to_radius'] * s2['nozzle_radius']
    s2['vortex_length'] = s2['vortex_ratio'] * s2['swiling_arm']
    s2['vortex_radius'] = s2['inlet_radius'] + s2['swiling_arm']
    s2['total_length'] = s2['vortex_length'] + s2['inlet_radius'] + s2['nozzle_length']
    s2['nozzle_radius'] = s2['nozzle_radius']
    while s2['liquid_vortex_radius'] < (s1['vortex_radius']+s1['wall_thickness']) or s2['reynolds_number'] < 10000:
        # determine Nozzle radius via iteration
        s2['nozzle_spacing'] += 0.001
        s2['nozzle_radius'] = s1['outside_radius'] + s2['nozzle_spacing']

        # 2.1 Determine flow coefficient required for specified pressure drop
        s2['flow_coefficient'] = (s2['mass_flow_rate']*math.sqrt(s2['density']*s2['pressure_drop'])*361)/((s2['density']*s2['pressure_drop'])*1600*s2['nozzle_radius']**2)

        # 2.2 Determine Geometric characteristic for given nozzle ratio
        f_name = 'Data/A_mu,C='
        f_name += str(s2['opening_coefficient'])
        s2['geometric_characteristic'] = IO_Manager.graph_to_value(s2['flow_coefficient'], f_name, 1)

        # finding inlet dimentions for second chamber
        s2['swiling_arm'] = s2['nozzle_radius']
        s2['inlet_radius'] = math.sqrt((s2['swiling_arm'] * s2['nozzle_radius']) / (s2['inlet_quantity'] * s2['geometric_characteristic']))
        s2['inlet_length'] = s2['inlet_ratio'] * s2['inlet_radius']

        # finding Chamber 2 dimentions
        s2['nozzle_length'] = s2['length_to_radius'] * s2['nozzle_radius']
        s2['vortex_length'] = s2['vortex_ratio'] * s2['swiling_arm']
        s2['vortex_radius'] = s2['inlet_radius'] + s2['swiling_arm']
        s2['total_length'] = s2['vortex_length'] + s2['inlet_radius'] + s2['nozzle_length']
        s2['nozzle_radius'] = s2['nozzle_radius']

        # 2.3 Determine Spray angle given Nozzle length coefficient
        f_name = 'Data/2a_A,l='
        f_name += str(s2['length_to_radius'])
        s2['spray_angle'] = IO_Manager.graph_to_value(s2['geometric_characteristic'], f_name, 1)

        #2.4 Determine liquid vortex level
        f_name = 'Data/A_R,Rin='
        f_name += str(s2['opening_coefficient'])
        s2['liquid_vortex_radius'] = IO_Manager.graph_to_value(s2['geometric_characteristic'], f_name, 0)*s2['nozzle_radius']

        s2['max_offset'] = (s1['wall_thickness']+s2['nozzle_spacing'])*math.tan((90-(s1['spray_angle']/2))*math.pi/180)*.95
        #determine minimum vortex cross section
        if s2['max_offset']+s1['nozzle_length'] >= s2['nozzle_length']:
            s2['minimum_chamber_dradius'] = (s1['vortex_radius']+s1['wall_thickness'])-s2['vortex_radius']
        else:
            if s2['max_offset']+s1['nozzle_length'] >= s2['nozzle_length']+(s2['vortex_radius']-s2['nozzle_radius']):
                s2['minimum_chamber_dradius'] = (s1['vortex_radius']+s1['wall_thickness'])-s2['nozzle_radius']
            else:
                s2['minimum_chamber_dradius'] = ((s1['vortex_radius']+s1['wall_thickness'])-s2['vortex_radius'])-(s2['nozzle_length']-(s2['max_offset']+s1['nozzle_length']))
        #determine reynolds number
        s2['inlet_velocity'] = s2['mass_flow_rate'] / (s2['inlet_quantity'] * math.pi * (s2['inlet_radius'] ** 2) * s2['density'])
        s2['reynolds_number'] = (s2['inlet_velocity'] * s2['inlet_radius'] * 2 * math.sqrt(s2['inlet_quantity'])) / s2['kinematic_viscosity']
        if s2['reynolds_number'] < 10000:
            print("error, Reynolds Number too low")
            print(s2['reynolds_number'], '< 10000')
        if s2['liquid_vortex_radius'] < (s1['vortex_radius']+s1['wall_thickness']):
            print('liquid vortex level too low')



    # s1['max_usable_length'] = s1['total_length'] - (2*s1['inlet_radius']) + (s2['max_offset']-s1['film_thickness']*1.25)
    print('S1 dimenttions---------------------------------------')
    print('s1_nozzle_radius = ',s1['nozzle_radius']*100)
    print('s1_nozzle_length = ',s1['nozzle_length'] * 100)
    print('s1_vortex_radius = ',s1['vortex_radius'] * 100)
    print('s1_vortex_length = ',s1['vortex_length'] * 100)
    print('s1_inlet_radius = ',s1['inlet_radius'] * 100)
    print('s2 dimenttions---------------------------------------')
    print('s2_nozzle_radius = ', s2['nozzle_radius'] * 100)
    print('s2_nozzle_length = ', s2['nozzle_length'] * 100)
    print('s2_vortex_radius = ', s2['vortex_radius'] * 100)
    print('s2_vortex_length = ', s2['vortex_length'] * 100)
    print('s2_inlet_radius = ', s2['inlet_radius'] * 100)

    IO_Manager.write_output(s1, 'central_coax_chamber_output', 1)
    IO_Manager.write_output(s2, 'outside_coax_chamber_output', 1)
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
    vortex_length_ratio = x['vortex_length_ratio']  # typically ls>2Rin (d=2) smaller the shorter
    length_to_radius = x['nozzle_length_ratio']  # data with 0.5 or 2 the larger this value, the longer the chamber
    # Step 1
    # this method is not infinitely expandable, I Hate It !!!
    f_name = 'Data/2a_A,l='
    f_name += str(length_to_radius)
    geometric_characteristic = IO_Manager.graph_to_value(spray_angle, f_name, 0)
    f_name = 'Data/A_mu,C='
    f_name += str(x['opening_coefficient'])
    flow_coefficient = IO_Manager.graph_to_value(geometric_characteristic, f_name, 0)
    # Step 2
    nozzle_radius = 0.475 * math.sqrt(mass_flow_rate / (flow_coefficient * math.sqrt(density * pressure_drop)))
    # step 3
    swiling_arm = nozzle_radius
    inlet_radius = math.sqrt((swiling_arm * nozzle_radius) / (inlet_quantity * geometric_characteristic))
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
    swirloutput['vortex_length'] = vortex_length_ratio * swiling_arm * 100
    swirloutput['vortex_radius'] = (swiling_arm + inlet_radius) * 100
    swirloutput['nozzle_length'] = length_to_radius * 2 * nozzle_radius * 100
    swirloutput['inlet_velocity'] = inlet_velocity
    swirloutput['flow_coefficient'] = flow_coefficient
    swirloutput['geometric_characteristic'] = geometric_characteristic
    IO_Manager.write_output(swirloutput, output, 1)
    return ()

#this currently DOES NOT WORK!!!!
#geometric characteristic has a horrible habit of walking to 0.5 for some damn reason
def complex_swirl(input):
    # 1. Prescribe spray cone angle
    s = read_input(input)
    # Prescribe spray angle and beggining parameter
    # Calculate Geometric characteristic
    s['geometric_characteristic'] = IO_Manager.graph_to_value(s['spray_angle'], 'Data/f2a_A', 0)
    # Calculate flow Coefficient
    s['flow_coefficient'] = IO_Manager.graph_to_value(s['geometric_characteristic'], 'Data/fA_mu', 0)

    s['equivalent_spray_angle'] = 0
    oldspray = 1
    while oldspray != s['equivalent_spray_angle']:
        oldspray = s['equivalent_spray_angle']
        # Calculate Nozzle Radius
        s['nozzle_radius'] = 0.475 * math.sqrt(s['mass_flow_rate'] / (s['flow_coefficient'] * math.sqrt(s['density'] * s['pressure_drop'])))
        # Calculate Swirling Arm
        s['swirling_arm'] = s['vortex_expansion_coefficient']*s['nozzle_radius']
        # Calculate Inlet Radius
        s['inlet_radius'] = math.sqrt((s['swirling_arm'] * s['nozzle_radius']) / (s['inlet_quantity'] * s['geometric_characteristic']))
        s['inlet_length'] = s['inlet_ratio'] * s['inlet_radius']
        # Revise Other Parameter
        s['nozzle_length'] = s['nozzle_length_ratio']*s['nozzle_radius']
        s['vortex_radius'] = s['swirling_arm']+s['inlet_radius']
        s['vortex_length'] = s['vortex_length_ratio']*s['swirling_arm']
        # Calculate inlet reynolds number
        s['inlet_reynold'] = 0.637 * (s['mass_flow_rate']/(math.sqrt(s['inlet_quantity'])*s['inlet_radius']*s['density']*s['kinematic_viscosity']))
        # Calculate friction coefficient
        s['friction_coefficient'] = 0.3164/(s['inlet_reynold']**.25)
        # Determine Equivalent Geometric Characteristic
        s['equivalent_geometric_characteristic'] = (s['swirling_arm']*s['nozzle_radius'])/((s['inlet_quantity']*(s['inlet_radius']**2))+(s['friction_coefficient']/2)*s['swirling_arm']*(s['swirling_arm']-s['nozzle_radius']))
        # Determine Equivalent Flow Coeffient
        s['equivalent_flow_coefficient'] = IO_Manager.graph_to_value(s['equivalent_geometric_characteristic'], 'Data/fA_mu', 0)
        print('equivalent_geometric_characteristic = ', s['equivalent_geometric_characteristic'])
        # Determine Equivalent Angle
        s['equivalent_spray_angle'] = IO_Manager.graph_to_value(s['geometric_characteristic'], 'Data/fA_2a', 0)
        print('equivalent_spray_angle = ', s['equivalent_spray_angle'])
        # Calculate tilting angle
        s['internal_tilt_angle'] = 90 - math.degrees(math.atan(s['vortex_radius'] / s['inlet_length']))
        # Calculate Inlet losses
        s['inlet_loss'] = (s['internal_tilt_angle'] / (0 - 150)) + 1.1
        # Calculate hydraulic-loss
        s['hydraulic_loss'] = s['inlet_loss'] + (s['friction_coefficient'] * (s['inlet_length'] / (2 * s['inlet_radius'])))
        # Determine actual flow coefficient
        s['flow_coefficient'] = (s['equivalent_flow_coefficient']/math.sqrt(1+s['hydraulic_loss']*(s['equivalent_flow_coefficient']**2)*((s['geometric_characteristic']**2)/(s['opening_coefficient']**2))))
        # Calculate nozzle with new approximation
        s['nozzle_radius'] = 0.475 * math.sqrt(s['mass_flow_rate'] / (s['flow_coefficient'] * math.sqrt(s['density'] * s['pressure_drop'])))
        # Calculate new geometric characteristic
        s['geometric_characteristic'] = (s['swirling_arm']*s['nozzle_radius'])/(s['inlet_quantity']*(s['inlet_radius']**2))
        print('spray_angle = ',s['spray_angle'])
    IO_Manager.write_output(s, 'central_coax_chamber_output', 1)
    print('results---------------------')
    print('s_nozzle_radius = ', s['nozzle_radius'] * 100)
    print('s_nozzle_length = ', s['nozzle_length'] * 100)
    print('s_vortex_radius = ', s['vortex_radius'] * 100)
    print('s_vortex_length = ', s['vortex_length'] * 100)
    print('s_inlet_radius = ', s['inlet_radius'] * 100)
    print('geometric_characteristic=',s['geometric_characteristic'])