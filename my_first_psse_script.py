import psse35
import psspy
import pandas as pd
import math

def parse_return(func_name,lst):
    '''interpret the items returned from func call'''
    if len(lst)!=2:
        print('func {} doesnt return 2 items; expected return of (ierr,iarrray)'.format(func_name))
    err,res=lst
    if err == 0:
        print('{} result={}'.format(func_name,res[0]))
        return res
    else:
        print('{} error code={}'.format(func_name,err))
        return None

path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/3bus/"
filename="3bus.sav"
psspy.psseinit()
psspy.case(path_to_cases+filename)
psspy.fdns([0,0,0,1,1,0,99,0])
print('---------')

bus_info=parse_return('abusint',psspy.abusint(string=['NUMBER','TYPE']))
bus_v=parse_return('abusreal',psspy.abusreal(string='PU'))[0]
bus_dict={}
bus_dict['type'] = bus_info[1]
bus_dict['Vpu'] = bus_v
bus_df= pd.DataFrame(data=bus_dict,index=bus_info[0])
print(bus_df)

branch_from=parse_return('aflowint',psspy.aflowint(string=['FROMNUMBER']))[0]
branch_to=parse_return('aflowint',psspy.aflowint(string=['TONUMBER']))[0]
branch_I=parse_return('aflowreal', psspy.aflowreal(string='PUCUR'))[0]

def get_duplocate_idx(seq):
    idx_to_remove=[]
    seq_so_far=[]
    for i in range(len(seq)):
        if any([math.isclose(seq[i],a,abs_tol=1e-5) for a in seq_so_far]):
            idx_to_remove.append(i)
        seq_so_far.append(seq[i])
    return idx_to_remove
dup_idx=get_duplocate_idx(branch_I)
assert len(dup_idx) == len(branch_I) / 2 # remove half the currents
branch_dict={}
branch_dict['from'] = [branch_from[i] for i in dup_idx]
branch_dict['to'] = [branch_to[i] for i in dup_idx]
branch_dict['Ipu'] = [branch_I[i] for i in dup_idx]
branch_df= pd.DataFrame(data=branch_dict)
print(branch_df)