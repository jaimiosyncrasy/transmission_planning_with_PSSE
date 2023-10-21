from utils import parse_return,get_duplicate_idx
import psspy
import pandas as pd

def process_bus_results():
    bus_info=parse_return('abusint',psspy.abusint(string=['NUMBER','TYPE']))
    bus_v=parse_return('abusreal',psspy.abusreal(string=['PU','KV','ANGLED']))
    bus_dict={}
    bus_dict['type'] = bus_info[1]
    bus_dict['Vmag (pu)'] = bus_v[0]
    bus_dict['Vmag (kV)'] = bus_v[1]
    bus_dict['Vang (deg)'] = bus_v[2]
    bus_df= pd.DataFrame(data=bus_dict,index=bus_info[0])
    return bus_df

def process_branch_results():
    branch_from=parse_return('aflowint',psspy.aflowint(string=['FROMNUMBER']))[0]
    branch_to=parse_return('aflowint',psspy.aflowint(string=['TONUMBER']))[0]
    branch_I=parse_return('aflowreal', psspy.aflowreal(string='PUCUR'))[0]
    flow=parse_return('aflowreal', psspy.aflowreal(string=['P','Q']))
    branch_ovd_percent=parse_return('aflowreal', psspy.aflowreal(string='PCTMVARATE'))[0] # Percent from bus MVA of default rating set.
    dup_idx=get_duplicate_idx(branch_I)
    assert len(dup_idx) == len(branch_I) / 2 # remove half the currents
    branch_dict={}
    branch_dict['from'] = [branch_from[i] for i in dup_idx]
    branch_dict['to'] = [branch_to[i] for i in dup_idx]
    branch_dict['P (MW)'] = [flow[0][i] for i in dup_idx]
    branch_dict['Q (MVar)'] = [flow[1][i] for i in dup_idx]
    branch_dict['overload (%)'] = [branch_ovd_percent[i] for i in dup_idx]
    branch_df= pd.DataFrame(data=branch_dict)
    return branch_df