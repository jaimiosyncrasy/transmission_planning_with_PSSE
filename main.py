import psse35 # this must come before 'import psspy' for psspy to be found!
import psspy

from algorithms import iteration_add_br
from assess_circuit import create_branch_lst
from utils import open_case, parse_return
import matplotlib.pyplot as plt
import random
import itertools

# --------- load transmission network case: ------------
# path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/3bus/"
# filename="3bus.sav"
path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/7bus/"
filename="7bus_with_xfmr_and_wind.sav"
psspy.psseinit()
open_case(path_to_cases+filename)

# automated routine 1:
# we add a transmission line to every possible bus pair and determine the line that
# -> reduces line overloading the most
# -> reduces xfmr overloading the most

# --------- setup -------------
random.seed(4) # so that get same random colors plotted each time
nwk_branches=create_branch_lst()
new_br_parms={'R':0.001,'X':0.005,'MAX_MVA':100}
metric_details={'line_overload':'MVA overload (%)',
                'xfmr_overload':'MVA overload (%)',
                'voltage':'Vmag (pu)'}
plot_bool=True

# --- add branch to all possible locations: ----
bus_info = parse_return('abusint', psspy.abusint(string=['NUMBER']))[0]
all_bus_pairs=itertools.combinations(bus_info, 2)
results_df, scenario_lst, lst_ordered_results=iteration_add_br(all_bus_pairs,nwk_branches,new_br_parms,metric_details,plot_bool)

# --- add branch to a single location: ----
# des_bus_pair=(670,673)
# results_df, scenario_lst, lst_ordered_results=iteration_add_br([des_bus_pair],nwk_branches,new_br_parms,metric_details,plot_bool)

print(lst_ordered_results[0])
if plot_bool:
    plt.show()