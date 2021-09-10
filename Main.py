# import Required addons
import math

import Calculations
import IO_Manager

# Main Script Goes here
Calculations.complex_swirl('central_coax_chamber_output')
# Calculations.coax_final_plz()
# Calculations.complex_swirl('outside_coax_chamber_output')
# Calculations.coaxswirl()
Calculations.simpleswirl('central_coax_chamber_output','outputs')
# Calculations.complex_swirl('first_stage')