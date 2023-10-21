import psse35
import psspy

from modify_circuit import add_load, add_br, add_bus
from process_results import process_bus_results, process_branch_results
from utils import parse_return, get_duplicate_idx

path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/3bus/"
filename="3bus.sav"
psspy.psseinit()
psspy.case(path_to_cases+filename)
psspy.fdns([0,0,0,1,1,0,99,0])
bus_df1=process_bus_results()
branch_df1=process_branch_results()

# add_load(bus_num=675,loadP=50,loadQ=20)
add_bus(type=1,num=676,base_kva=200)
add_br(676,674,{'R':0.001,'X':0.005,'MAX_MVA':100})
psspy.fdns([0,0,0,1,1,0,99,0])
bus_df2=process_bus_results()
branch_df2=process_branch_results()

print('---------')
print('Bus types (1,2,3) = (load,generator,swing)')
print(bus_df1)
print('---------')
print(bus_df2)
print('---------')
print(branch_df1)
print('---------')
print(branch_df2)

# automated routine 1:
# add a transmission line to various buses and determine the bus that
# -> reduces line congestion the most
# -> reduced fault currents the most
# -> reduces line+xfmr overloading the most

# ^can add a load and check for the same thing