import math

import IO_Manager

x = {}


# this function will take an lox_input file and convert it to the dictionary
# once used all variables in dictionary x will be updated autonomously
# format for lox_input file
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
def combustion(file):
    c = read_input(file)
    #

    #Calculate fluid Velocity coefficient

    #Calculate Characteristic Length
    return ()


# This will calculate nozzle parameters
def nozzle(file):
    s = read_input(file)

    #Calculate Throat Area
    s['throat_area'] = (s['mass_flow_rate']/s['chamber_pressure'])*math.sqrt((s['Gas'])/())
    #

    return ()


# This will define cooling system
def cooling():
    return ()


def simple_inner_swirl(input):
    s = read_input(input)
    s['density'] = s['density']*1000000
    s['kinematic_viscosity'] = s['kinematic_viscosity']*10**(0-6)
    s['mass_flow_rate'] = s['mass_flow_rate']/1000
    f_name = 'Data/2a_A,l='
    f_name += str(s['nozzle_length_ratio'])
    s['geometric_characteristic'] = IO_Manager.graph_to_value(s['spray_angle'], f_name, 0)
    f_name = 'Data/A_mu,C='
    f_name += str(s['nozzle_contraction_coefficient'])
    s['flow_coefficient'] = IO_Manager.graph_to_value(s['geometric_characteristic'], f_name, 0)

    # Step 2
    s['nozzle_radius'] = 0.475 * math.sqrt(s['mass_flow_rate'] / (s['flow_coefficient'] * math.sqrt(s['density'] * s['pressure_drop'])))

    # step 3
    s['swirling_arm'] = s['nozzle_radius']
    s['inlet_radius'] = math.sqrt((s['swirling_arm'] * s['nozzle_radius']) / (s['inlet_quantity'] * s['geometric_characteristic']))

    # Step 5
    s['inlet_velocity'] = s['mass_flow_rate'] / (s['inlet_quantity'] * math.pi * (s['inlet_radius'] ** 2) * s['density'])
    s['reynolds_number'] = (s['inlet_velocity'] * s['inlet_radius'] * 2 * math.sqrt(s['inlet_quantity'])) / s['kinematic_viscosity']
    if s['reynolds_number'] < 10000:
        print("error, Reynolds Number too low")
        print(s['reynolds_number'], '<10000')

    s['vortex_radius'] = s['swirling_arm'] + s['inlet_radius']
    print('experimental approach ----------------------------------------------------')
    print('inlet_radius = ',s['inlet_radius']*1000)
    print('nozzle_radius = ', s['nozzle_radius']*1000)
    print('vortex_radius = ', s['vortex_radius']*1000)
    print('flow_coefficient = ', s['flow_coefficient'])

    # Step 6
    # s['nozzle_length'] = s['nozzle_radius'] * s['nozzle_length_ratio']

    # s['vortex_length'] = s['vortex_length_ratio'] * s['vortex_radius']
    # IO_Manager.write_output(s, lox_input, 1)


def generate_data():
    phi = 0.2
    a_g = {}
    g_m = {}
    while phi < 1:
        print('phi = ',phi)
        geometric = ((1 - phi) * math.sqrt(2)) / (phi * math.sqrt(phi))
        print('geometric = ', geometric)
        # flow_coefficient = (phi * math.sqrt(phi)) / math.sqrt(2 - phi)
        flow_coefficient = math.sqrt((phi ** 3) / (2 - phi))
        print('flow_coefficient = ', flow_coefficient)
        # Calculate Dimentionless Vortex Radius
        guess = 0
        d_vortex_radius = 1
        while round(guess,13) != round(d_vortex_radius,13):
            guess = d_vortex_radius
            f = ((math.sqrt(1 - (flow_coefficient ** 2) * (geometric ** 2)))
                 - (guess * math.sqrt((guess ** 2) - (flow_coefficient ** 2) * (geometric ** 2)))
                 - ((flow_coefficient ** 2) * (geometric ** 2) * math.log((1 + math.sqrt(1 - (flow_coefficient ** 2) * (geometric ** 2))) / (guess + math.sqrt((guess ** 2) - (flow_coefficient ** 2) * geometric ** 2)), math.e))
                 - flow_coefficient
                 )
            f_prime = (0 - 2) * math.sqrt((guess ** 2) - (flow_coefficient ** 2) * (geometric ** 2))
            d_vortex_radius = guess - (f / f_prime)
            print(phi)
        print('d_vortex_radius = ', d_vortex_radius)
        #calculate_spray_angle
        angle = 2 * math.degrees(math.atan((2 * flow_coefficient * geometric) / (math.sqrt(((1 + d_vortex_radius) ** 2) - 4 * (flow_coefficient ** 2) * (geometric ** 2)))))
        print('angle = ', angle)
        a_g[str(angle)] = str(geometric)
        g_m[str(geometric)] = str(flow_coefficient)
        phi=round(phi+0.001,5)
    print(a_g)
    IO_Manager.write_output(a_g,'a_g',1,',')
    print(g_m)
    IO_Manager.write_output(g_m,'g_m',1,',')

def borodin_approach(file):
    s = read_input(file)
    #Elementary calculation --------------------------------------------------------------
    # s['geometric_characteristic'] = IO_Manager.graph_to_value(s['spray_angle'], 'a_g', 0)
    # print('geometric_characteristic = ',s['geometric_characteristic'])
    # s['flow_coefficient'] = IO_Manager.graph_to_value(s['geometric_characteristic'],'g_m',0)
    # print('INNITIAL flow_coefficient = ', s['flow_coefficient'])
    s['geometric_characteristic'] = 0.9
    s['flow_coefficient'] = 0.462

    s['nozzle_radius'] = math.sqrt((4*s['mass_flow_rate'])/(math.pi*s['flow_coefficient']*math.sqrt(2*s['density']*s['pressure_drop'])))/2
    print('test diameter = ', (0.475*math.sqrt(s['mass_flow_rate']/(s['flow_coefficient']*math.sqrt(s['density']*s['pressure_drop']))))*2 )

    s['swirling_arm'] = s['nozzle_contraction_coefficient']*s['nozzle_radius']
    s['inlet_radius'] = math.sqrt((s['swirling_arm']*s['nozzle_radius'])/(s['inlet_quantity']*s['geometric_characteristic']))
    #Viscous Calculation---------------------------------------------------------------------
    s['equivalent_geometric_characteristic'] = s['geometric_characteristic']+1
    while round(s['equivalent_geometric_characteristic'],5) != round(s['geometric_characteristic'],5):
        s['reynolds_number'] = (4 * s['mass_flow_rate']) / (s['density'] * s['kinematic_viscosity'] * math.pi * 0.02 * s['inlet_radius'] * math.sqrt(s['inlet_quantity']))
        s['friction_coefficient'] = 10 ** ((25.8 / (math.log(s['reynolds_number'], 10) ** 2.58)) - 2)
        s['equivalent_geometric_characteristic'] = (s['swirling_arm']*s['nozzle_radius'])/((s['inlet_quantity']*s['inlet_radius']**2)+(s['friction_coefficient']/2)*s['swirling_arm']*(s['swirling_arm']-s['nozzle_radius']))
        if round(s['equivalent_geometric_characteristic'],5) == round(s['geometric_characteristic'],5):
            continue
        else:
            # print(((s['swirling_arm'] * s['nozzle_radius']) / (s['inlet_quantity'] * s['geometric_characteristic'])) - (s['friction_coefficient'] / (2 * s['inlet_quantity'])) * s['swirling_arm'] * (s['swirling_arm'] - s['nozzle_radius']))
            s['inlet_radius'] = math.sqrt(((s['swirling_arm'] * s['nozzle_radius']) / (s['inlet_quantity'] * s['geometric_characteristic'])) - (s['friction_coefficient'] / (2 * s['inlet_quantity'])) * s['swirling_arm'] * (s['swirling_arm'] - s['nozzle_radius']))

    # Flow contraction compensation
    s['inlet_radius'] = math.sqrt(((1/s['inlet_contraction_factor'])*math.pi*s['inlet_radius']**2)/math.pi)
    # print('Theoretical Approach/First Iteration ----------------------------------------------')
    print('inlet_radius = ',s['inlet_radius'])
    print('nozzle_radius = ',s['nozzle_radius'])
    # print('vortex_radius =',s['swirling_arm']+s['inlet_radius'])
    # print('flow_coefficient = ',s['flow_coefficient'])


def testy(phi):
    print('phi = ', phi)
    geometric = ((1 - phi) * math.sqrt(2)) / (phi * math.sqrt(phi))
    print('geometric = ',geometric)
    # flow_coefficient = (phi*math.sqrt(phi))/math.sqrt(2-phi)
    flow_coefficient = math.sqrt((phi ** 3) / (2 - phi))
    print('flow_coefficient = ',flow_coefficient)
    # Calculate Dimentionless Vortex Radius
    guess = 0
    d_vortex_radius = 1
    while guess != d_vortex_radius:
        guess = d_vortex_radius
        f = ((math.sqrt(1 - (flow_coefficient ** 2) * (geometric ** 2)))
             - (guess * math.sqrt((guess ** 2) - (flow_coefficient ** 2) * (geometric ** 2)))
             - ((flow_coefficient ** 2) * (geometric ** 2) * math.log((1 + math.sqrt(1 - (flow_coefficient ** 2) * (geometric ** 2))) / (guess + math.sqrt((guess ** 2) - (flow_coefficient ** 2) * geometric ** 2)), math.e))
             - flow_coefficient
             )
        f_prime = (0 - 2) * math.sqrt((guess ** 2) - (flow_coefficient ** 2) * (geometric ** 2))
        d_vortex_radius = guess - (f / f_prime)
    print('d_vortex_radius = ',d_vortex_radius)
    angle = 2*math.degrees(math.atan((2*flow_coefficient*geometric)/(math.sqrt(((1+d_vortex_radius)**2)-4*(flow_coefficient**2)*(geometric**2)))))
    print('angle = ',angle)