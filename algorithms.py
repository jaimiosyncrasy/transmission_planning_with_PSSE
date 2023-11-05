import itertools

from assess_circuit import create_branch_lst, \
    determine_best_upgrades, Scenario
from utils import parse_return,get_duplicate_idx
import psspy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from more_itertools import unique_everseen
from modify_circuit import add_br


def iteration_add_br(nwk_branches,parm_dict,metric):
    '''iterate over different bus combos and add a branch, evaluating which scneario is best'''
    bus_info=parse_return('abusint',psspy.abusint(string=['NUMBER']))[0]
    data=[] # each ele is row of results table
    scenario_lst=[]
    count=0
    for bus_pair in itertools.combinations(bus_info, 2):
        # branch_df = create_branch_results(nwk_branches)
        count+=1
        ID=str(20+count) # todo: generalize this
        new_br=add_br(bus_pair[0], bus_pair[1], parm_dict,ID)
        if new_br is not None:
            nwk_branches=create_branch_lst()
            psspy.fdns([0, 0, 0, 1, 1, 0, 99, 0]) # solve power flow
            scen=Scenario(new_br, nwk_branches)
            scenario_lst.append(scen)
            if metric=='line_overload':
                scen.plot_quantity('MVA overload (%)')
                # plot_label='MVA overload (%)'
                # list(self.bus_table['ID'])
            avg_metrics_on_nwk=scen.compute_metrics_on_nwk()
            data.append(list(new_br.info.values())+list(avg_metrics_on_nwk.values()))
            nwk_branches.pop(0) # remove added branch
        psspy.purgbrn(bus_pair[0], bus_pair[1],ID)  # reset
    col_names=list(new_br.info.keys())+list(avg_metrics_on_nwk.keys())
    results_df=pd.DataFrame(data,columns=col_names)
    results_df_ordered=determine_best_upgrades(results_df,metric)
    return results_df, scenario_lst, results_df_ordered

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