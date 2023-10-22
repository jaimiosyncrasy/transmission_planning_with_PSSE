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

def compute_metrics_on_nwk(bus_df, branch_df):
    avg_metrics={
        'line_congestion':0,
        'xfmr_overload':0,
        'fault_currents':0
    }
    # line congestion
    # xfmr overloading
    # fault currents
    return avg_metrics

def create_bus_results():
    bus_info=parse_return('abusint',psspy.abusint(string=['NUMBER','TYPE']))
    bus_v=parse_return('abusreal',psspy.abusreal(string=['PU','KV','ANGLED']))
    bus_dict={}
    bus_dict['type'] = bus_info[1]
    bus_dict['Vmag (pu)'] = bus_v[0]
    bus_dict['Vmag (kV)'] = bus_v[1]
    bus_dict['Vang (deg)'] = bus_v[2]
    bus_df= pd.DataFrame(data=bus_dict,index=bus_info[0])
    return bus_df

def create_branch_lst():
    branch_from = parse_return('aflowint', psspy.aflowint(string=['FROMNUMBER']))[0]
    branch_to = parse_return('aflowint', psspy.aflowint(string=['TONUMBER']))[0]
    branch_ID = parse_return('aflowchar', psspy.aflowchar(string=['ID']))[0]
    unique_idx=[i for i in range(len(branch_ID)) if branch_ID[i] != '1 '] # ID=1 is assigned to extra branches not in the SLD
    branch_lst=[]
    for i in unique_idx:
        branch_lst.append(Branch(branch_ID[i],branch_from[i],branch_to[i],i))
    return branch_lst
def create_branch_results(branch_lst):
    '''we assume that all branches have an ID that isnt the default of 1'''
    unique_idx=[br.br_idx for br in branch_lst]
    branch_I=parse_return('aflowreal', psspy.aflowreal(string='PUCUR'))[0]
    flow=parse_return('aflowreal', psspy.aflowreal(string=['P','Q']))
    branch_ovd_percent=parse_return('aflowreal', psspy.aflowreal(string='PCTMVARATE'))[0] # Percent from bus MVA of default rating set.
    # unique_idx=get_duplicate_idx(branch_I)
    # assert len(unique_idx) == len(branch_I) / 2 # remove half the currents
    # unique_idx=list(range(len(branch_from)))

    branch_dict={}
    branch_dict['from'] = [br.bus_FROMNUMBER for br in branch_lst]
    branch_dict['to'] = [br.bus_TONUMBER for br in branch_lst]
    branch_dict['ID'] = [br.branchID for br in branch_lst]
    branch_dict['P (MW)'] = [flow[0][i] for i in unique_idx]
    branch_dict['Q (MVar)'] = [flow[1][i] for i in unique_idx]
    branch_dict['overload (%)'] = [branch_ovd_percent[i] for i in unique_idx]
    branch_df= pd.DataFrame(data=branch_dict)
    return branch_df

def create_xfmr_results():
    branch_from = parse_return('atrnint', psspy.atrnint(string=['FROMNUMBER']))[0]
    branch_to = parse_return('atrnint', psspy.atrnint(string=['TONUMBER']))[0]
    branch_ID=parse_return('atrnchar',psspy.aflowchar(string=['ID']))[0]
    unique_idx=[i for i in range(len(branch_ID)) if branch_ID[i] != '1 ']
    branch_I = parse_return('atrnreal', psspy.atrnreal(string='PUCUR'))[0]
    flow = parse_return('atrnreal', psspy.atrnreal(string=['P', 'Q']))
    branch_ovd_percent = parse_return('atrnreal', psspy.atrnreal(string='PCTCORPRATE'))[
        0]  # Percent from bus current or MVA loading (according to the transformer percent loading units program option setting) of default rating set.
    # unique_idx = get_duplicate_idx(branch_I)
    # assert len(unique_idx) == len(branch_I) / 2  # remove half the currents
    xfmr_dict = {}
    xfmr_dict['from'] = [branch_from[i] for i in unique_idx]
    xfmr_dict['to'] = [branch_to[i] for i in unique_idx]
    xfmr_dict['P (MW)'] = [flow[0][i] for i in unique_idx]
    xfmr_dict['Q (MVar)'] = [flow[1][i] for i in unique_idx]
    xfmr_dict['overload (%)'] = [branch_ovd_percent[i] for i in unique_idx]
    xfmr_df = pd.DataFrame(data=xfmr_dict)
    return xfmr_df