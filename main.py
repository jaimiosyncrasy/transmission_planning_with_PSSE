import psse35 # this must come before 'import psspy' for psspy to be found!
import psspy

from algorithms import iteration_add_br
from assess_circuit import create_branch_lst
from plot import plot_lines
from utils import open_case
import matplotlib.pyplot as plt

# path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/3bus/"
# filename="3bus.sav"
path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/7bus/"
filename="7bus_with_xfmr_and_wind.sav"
psspy.psseinit()
open_case(path_to_cases+filename)
psspy.fdns([0,0,0,1,1,0,99,0])

# bus_df1=create_bus_results()
# branch_df1=create_branch_results()
# xfmr_df=create_xfmr_results()
# print(xfmr_df)
#
# # add_load(bus_num=675,loadP=50,loadQ=20)
# add_bus(type=1,num=676,base_kva=200)
# add_br(676,674,{'R':0.001,'X':0.005,'MAX_MVA':100})
# psspy.fdns([0,0,0,1,1,0,99,0])
# bus_df2=create_bus_results()
# branch_df2=create_branch_results()
#
# print('---------')
# print('Bus types (1,2,3) = (load,generator,swing)')
# print(bus_df1)
# print('---------')
# print(bus_df2)
# print('---------')
# print(branch_df1)
# print('---------')
# print(branch_df2)

# automated routine 1:
# replace an xfmr with larger ampacity on various branches and determine the xfmr that
# -> reduces line congestion the most
# -> reduced fault currents the most
# -> reduces line+xfmr overloading the most

# automated routine 2:
# add a transmission line to various buses and determine the bus that
# -> reduces line congestion the most
# -> reduces fault currents the most
# -> reduces line+xfmr overloading the most

# routine 3:
# given a bus of interest,
# add a transmission line and return summary of changes to congestion, fault currents, and line+xfmr loading

nwk_branches=create_branch_lst()
new_br_parms={'R':0.001,'X':0.005,'MAX_MVA':100}
metric = 'line_overload'  # you choose metric to determine best upgrade
ax = plt.figure().add_subplot(111)
results_df, scenario_lst, results_df_ordered=iteration_add_br(nwk_branches,new_br_parms,metric)
print(results_df_ordered)
plt.legend(loc="upper left")
metric_details={'line_overload':'MVA overload (%)','xfmr_overload':'MVA overload (%)'}
plt.xlabel('branch '+metric_details[metric])
plt.show()