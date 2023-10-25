import itertools

from utils import parse_return,get_duplicate_idx
import psspy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Branch:
    def __init__(self,br_ID,bus_FROMNUMBER,bus_TONUMBER,br_idx):
        self.branch_ID=br_ID
        self.bus_TONUMBER=bus_TONUMBER
        self.bus_FROMNUMBER=bus_FROMNUMBER
        self.br_idx=br_idx # index of branch in lst returned by psspy
        self.info=dict(branch_ID=self.branch_ID,bus_FROMNUMBER=self.bus_FROMNUMBER,bus_TONUMBER=self.bus_TONUMBER)

class Scenario:
    '''captures grid network info for particular scenario of a change in the network;
    allows for computing aggregate metrics and plotting'''
    def __init__(self,upgrade_ele,nwk_branches):
        branch_table=self.create_branch_results(nwk_branches)
        bus_table=self.create_bus_results()
        xfmr_table=self.create_xfmr_results()
        sc_table=self.create_sc_results()
        self.upgrade_ele=upgrade_ele
        self.nwk_branches=nwk_branches
        self.branch_table=branch_table
        self.bus_table=bus_table
        self.xfmr_table=xfmr_table
    def plot_quantity(self,col_string):
        '''take associated column of branch or bus table and plot'''
        bus_options=('Vmag (pu)','Vmag (kV)', 'Vang (deg)')
        branch_options=('P (MW)','Q (MVar)', 'overload (%)')
        if col_string in bus_options:
            plt.plot(self.bus_table[col_string])
        elif col_string in branch_options:
            plt.plot(self.branch_table[col_string])

    def compute_metrics_on_nwk(self):
        br_overload_lst=self.branch_table['MVA overload (%)'].tolist()
        xfmr_overload_lst=self.xfmr_table['MVA overload (%)'].tolist()
        # shortcircuit_I_lst=
        # xfmr_overload_lst=
        # fault_I_lst=
        avg_metrics = {
            'line_overload': sum(br_overload_lst) / len(br_overload_lst),
            'xfmr_overload': sum(br_overload_lst) / len(br_overload_lst),
            'fault_currents': sum(br_overload_lst) / len(br_overload_lst)
        }
        # line congestion
        # xfmr overloading
        # fault currents
        return avg_metrics

    def create_bus_results(self):
        bus_info = parse_return('abusint', psspy.abusint(string=['NUMBER', 'TYPE']))
        bus_v = parse_return('abusreal', psspy.abusreal(string=['PU', 'KV', 'ANGLED']))
        bus_dict = {}
        bus_dict['type'] = bus_info[1]
        bus_dict['Vmag (pu)'] = bus_v[0]
        bus_dict['Vmag (kV)'] = bus_v[1]
        bus_dict['Vang (deg)'] = bus_v[2]
        bus_df = pd.DataFrame(data=bus_dict, index=bus_info[0])
        return bus_df

    def create_branch_results(self,branch_lst):
        '''we assume that all branches have an ID that isnt the default of 1'''
        unique_idx = [br.br_idx for br in branch_lst]
        branch_I = parse_return('aflowreal', psspy.aflowreal(string='PUCUR'))[0]
        flow = parse_return('aflowreal', psspy.aflowreal(string=['P', 'Q']))
        branch_ovd_percent = parse_return('aflowreal', psspy.aflowreal(string='PCTMVARATE'))[
            0]  # Percent from bus MVA of default rating set.
        # unique_idx=get_duplicate_idx(branch_I)
        # assert len(unique_idx) == len(branch_I) / 2 # remove half the currents
        # unique_idx=list(range(len(branch_from)))

        branch_dict = {}
        branch_dict['from'] = [br.bus_FROMNUMBER for br in branch_lst]
        branch_dict['to'] = [br.bus_TONUMBER for br in branch_lst]
        branch_dict['ID'] = [br.branch_ID for br in branch_lst]
        branch_dict['P (MW)'] = [flow[0][i] for i in unique_idx]
        branch_dict['Q (MVar)'] = [flow[1][i] for i in unique_idx]
        branch_dict['MVA overload (%)'] = [branch_ovd_percent[i] for i in unique_idx]
        branch_df = pd.DataFrame(data=branch_dict)
        return branch_df

    def create_xfmr_results(self):
        branch_from = parse_return('atrnint', psspy.atrnint(string=['FROMNUMBER']))[0]
        branch_to = parse_return('atrnint', psspy.atrnint(string=['TONUMBER']))[0]
        xfmr_name = parse_return('atrnchar', psspy.atrnchar(string=['XFRNAME']))[0]
        unique_idx = [i for i in range(len(xfmr_name))]
        branch_I = parse_return('atrnreal', psspy.atrnreal(string='PUCUR'))[0]
        flow = parse_return('atrnreal', psspy.atrnreal(string=['P', 'Q']))
        branch_ovd_percent = parse_return('atrnreal', psspy.atrnreal(string='PCTCORPRATE'))[
            0]  # Percent from bus current or MVA loading (according to the transformer percent loading units program option setting) of default rating set.
        xfmr_dict = {}
        xfmr_dict['name'] = [xfmr_name[i] for i in unique_idx]
        xfmr_dict['from'] = [branch_from[i] for i in unique_idx]
        xfmr_dict['to'] = [branch_to[i] for i in unique_idx]
        xfmr_dict['P (MW)'] = [flow[0][i] for i in unique_idx]
        xfmr_dict['Q (MVar)'] = [flow[1][i] for i in unique_idx]
        xfmr_dict['MVA overload (%)'] = [branch_ovd_percent[i] for i in unique_idx]
        xfmr_df = pd.DataFrame(data=xfmr_dict)
        return xfmr_df

    def create_sc_results(self):
        import pssarrays
        robj = pssarrays.ascc_currents(
            sid=0,  # this could be different for you
            flt3ph=1,  # you may wish to apply different faults
        )
        robj.fltbus
        robj.flt3ph.values()
        # _i, _f, _s, _o = psspy._i, psspy._f, psspy._s, psspy._o
        # code1=psspy.ascc_3(0, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], 1.0, "", "", "")
        # code2=psspy.setdiagresascc_3(2, 0, _i, _i, _i, 1, 0, _i, _i, _i, "") #set the ASCC short circuit analysis annotation options in the active Slider diagram
        # xfmr_dict = {}
        # xfmr_dict['from'] = [branch_from[i] for i in unique_idx]
        # if code1!=0 or code2!=0:
        #     raise Exception('error adding load')
        # return True
def plot_double_bar():
    '''plot overlapping bar plots'''
    x_lst = [np.array([1, 2, 3, 4]),[2, 4, 6, 8]]
    y_lst = [x * 2,[3, 5, 7, 9]]

    for i in range(len(x)):
        plt.plot(x, y)

    plt.xlabel("X-axis data")
    plt.ylabel("Y-axis data")
    plt.title('multiple plots')
    plt.show()



def determine_best_upgrades(results_df):
    '''returns a dict where keys are category, and value is the scenario index'''
    pass


def create_branch_lst():
    branch_from = parse_return('aflowint', psspy.aflowint(string=['FROMNUMBER']))[0]
    branch_to = parse_return('aflowint', psspy.aflowint(string=['TONUMBER']))[0]
    branch_ID = parse_return('aflowchar', psspy.aflowchar(string=['ID']))[0]
    unique_idx,branch_lst=[],[]
    for i in range(len(branch_ID)):
        if branch_ID[i] not in unique_idx and branch_ID[i] != '1 ':
            unique_idx.append(branch_ID[i])
            branch_lst.append(Branch(branch_ID[i], branch_from[i], branch_to[i], i))
    # unique_idx=[i for i in range(len(branch_ID)) if branch_ID[i] != '1 '] # ID=1 is assigned to extra branches not in the SLD
    return branch_lst