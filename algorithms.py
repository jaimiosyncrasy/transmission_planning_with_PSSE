import itertools

from assess_circuit import create_branch_lst, \
    determine_best_upgrades, Scenario
from plot import setup_plotting, format_plots
from utils import parse_return,get_duplicate_idx
import psspy
import pandas as pd
from modify_circuit import add_br


def assess_added_ele(bus_pair,parm_dict,ID,nwk_branches,metric_details,ax_lst,plot_bool):
    '''inner computational function for adding & assessing an added branch'''
    new_br = add_br(bus_pair[0], bus_pair[1], parm_dict, ID)
    scen,avg_metrics_on_nwk=None,None
    if new_br is not None:
        nwk_branches = create_branch_lst()
        psspy.fdns([0, 0, 0, 1, 1, 0, 99, 0])  # solve power flow
        scen = Scenario(new_br, nwk_branches)
        if plot_bool:
            for metric_name, metric_detail in metric_details.items():
                i = list(metric_details.keys()).index(metric_name)
                scen.plot_quantity(ax_lst[i], metric_name, metric_detail)
        avg_metrics_on_nwk = scen.compute_metrics_on_nwk()
        nwk_branches.pop(0)  # remove added branch
    psspy.purgbrn(bus_pair[0], bus_pair[1], ID)  # reset

    return nwk_branches,new_br,avg_metrics_on_nwk,scen

def iteration_add_br(bus_pairs,nwk_branches,parm_dict,metric_details,plot_bool):
    '''iterate over different bus combos and add a branch,
    call assess_added_ele, then summarize which scenario is best'''

    data=[] # each ele is row of results table
    scenario_lst,count=[],0

    if plot_bool:
        ax_lst=setup_plotting(len(metric_details.keys()))

    for bus_pair in bus_pairs:
        # branch_df = create_branch_results(nwk_branches)
        ID=str(20+count) # todo: generalize this
        nwk_branches,new_br,avg_metrics_on_nwk,scen=assess_added_ele(bus_pair,parm_dict,ID,nwk_branches,metric_details,ax_lst,plot_bool)
        if new_br is not None:
            scenario_lst.append(scen)
            data.append(list(new_br.info.values()) + list(avg_metrics_on_nwk.values()))
        count += 1

    col_names=list(new_br.info.keys())+list(avg_metrics_on_nwk.keys())
    results_df=pd.DataFrame(data,columns=col_names)
    lst_ordered_results=determine_best_upgrades(results_df,metric_details)

    if plot_bool:
        format_plots(ax_lst,metric_details)

    return results_df, scenario_lst, lst_ordered_results



def iteration_add_wind(nwk_branches,parm_dict,metric_details,plot_bool):
    pass