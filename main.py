import psse35
import psspy

from modify_circuit import add_load, add_br
from process_results import process_bus_results, process_branch_results
from utils import parse_return, get_duplicate_idx

path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/3bus/"
filename="3bus.sav"
psspy.psseinit()
psspy.case(path_to_cases+filename)
psspy.fdns([0,0,0,1,1,0,99,0])
print('---------')
bus_df=process_bus_results()
branch_df=process_branch_results()

add_load(bus_num=670,loadP=50,loadQ=20)
# add_br(671,672,{'R':0.001,'X':0.005})
psspy.fdns([0,0,0,1,1,0,99,0])
print('---------')
bus_df=process_bus_results()
branch_df=process_branch_results()

# automated routine 1:
# add a transmission line to various buses and determine the bus that
# -> reduces line congestion the most
# -> reduced fault currents the most
# -> reduces line+xfmr overloading the most

# ^can add a load and check for the same thing