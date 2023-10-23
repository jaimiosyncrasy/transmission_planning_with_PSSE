import itertools

from assess_circuit import create_branch_results, compute_metrics_on_nwk, create_bus_results, create_branch_lst
from utils import parse_return,get_duplicate_idx
import psspy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from more_itertools import unique_everseen
from modify_circuit import add_br


def iteration_add_br(nwk_branches,parm_dict):
    bus_info=parse_return('abusint',psspy.abusint(string=['NUMBER']))[0]
    data=[] # each ele is row of results table
    for bus_pair in itertools.combinations(bus_info, 2):
        # branch_df = create_branch_results(nwk_branches)
        new_br=add_br(bus_pair[0], bus_pair[1], parm_dict)
        if new_br is not None:
            nwk_branches=create_branch_lst()
            psspy.fdns([0, 0, 0, 1, 1, 0, 99, 0])
            branch_df=create_branch_results(nwk_branches)
            bus_df=create_bus_results()
            metrics_dict=compute_metrics_on_nwk(branch_df,bus_df)
            data.append(list(new_br.info.values())+list(metrics_dict.values()))
            nwk_branches.pop() # remove added branch
            psspy.remove_br

    col_names=list(new_br.info.keys())+list(metrics_dict.keys())
    results_df=pd.DataFrame(data,columns=col_names)
    return results_df

def iteration_add_load(assess_func,parms):
    bus_info=parse_return('abusint',psspy.abusint(string=['NUMBER','TYPE']))
    data=[] # each ele is row of results table
    for bus in itertools.combinations(bus_info, 2):
        add_br(bus_pair[0], bus_pair[1], parm_dict)
        metrics_dict=compute_metrics_on_nwk()
        data.append(list(bus_pair)+list(metrics_dict.values()))

    col_names=['bus num']+list(metrics_dict.keys())
    results_df=pd.DataFrame(data,columns=col_names)
    return results_df