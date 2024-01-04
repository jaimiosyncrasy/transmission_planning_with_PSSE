import psse35 # this must come before 'import psspy' for psspy to be found!
import psspy
from utils import open_case
psspy.set_fpcw_py() # for dyntools
import os, sys, collections # for dyntools
from dyntools_demo import test1_data_extraction,test_sensitivity_mult_trace

def initialize_dyn_sim():
    # solve power flow
    psspy.fdns([0, 0, 0, 1, 1, 0, 0, 0])
    # convert loads and generators to prep for dynamic sim
    psspy.cong(0)
    psspy.conl(0, 1, 1, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, 0.0, 100.0])
    # factorize admittance matrix
    psspy.fact()
    # perform a simplified low flow
    psspy.tysl(0)
    # define output channels
    psspy.bsys(0, 0, [13.8, 500.], 1, [1], 0, [], 0, [], 0, [])  # define bus subsystem for channel outputs
    psspy.chsb(0, 0, [-1, -1, -1, 1, 12, 0])
    psspy.chsb(0, 0, [-1, -1, -1, 1, 13, 0])
    psspy.chsb(0, 0, [-1, -1, -1, 1, 16, 0])
    psspy.chsb(0, 0, [-1, -1, -1, 1, 17, 0])
    # set reference generator
    psspy.set_relang(1, 101, r"""1""")


def run_dyn_sim(parm_val, outfile_fullpath):
    '''paste parm changes, faults, and run commands from recording'''
    # when you paste the recording, you need to replace 2 hardcoded areas: (1) the parameter key+value, and (2) the output file name

    psspy.change_plmod_con(2,r"""1""",r"""SEXS""",3,parm_val) # change parms
    # psspy.strt_2([0,0],r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\2.Brazilian_7_bus_Equivalent_Model_V32_Files\PSSE\parms_35_and_13.out""")
    psspy.strt_2([0,0],+outfile_fullpath)
    psspy.run(0,1.0,0,1,1)
    psspy.dist_3phase_bus_fault(4,0,1,765.0,[0.0,-0.2E+10])
    psspy.run(0,1.1,0,1,1)
    psspy.dist_clear_fault(1)
    psspy.run(0,4.0,0,1,1)


def run_parm_sens_routine(path):
    parm_vals = [0.2, 0.3, 0.4]
    parm_name = 'Kp' # we assume this matches what you change in recording the dyn sim
    channels_lst = [3, 4]

    initialize_dyn_sim()
    outfile_lst = []
    for parm_val in parm_vals:
        outfile_name=parm_name + '_set_to_' + str(parm_val) + '.out'
        print("writing dyn sim output to: {}\n".format(outfile_name))
        outfile_fullpath = path + outfile_name
        outfile_lst.append(outfile_fullpath)
        run_dyn_sim(parm_val, outfile_fullpath)
    test_sensitivity_mult_trace(outfile_lst, channels_lst)  # plot

if __name__ == '__main__':
    import psse35

    path_to_case = "C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/EXAMPLE/less_50_buses/"
    sav_filename = "savnw.sav"
    dyr_filename = "savnw.dyr"""
    psspy.psseinit()

    # psspy.lines_per_page_one_device(1, 10000000)
    # outdir=path_to_cases
    # prgfile  = os.path.join(outdir,'progress.txt')
    # psspy.progress_output(2, prgfile, [0, 0])

    open_case(path_to_case + sav_filename)

    # psspy.case(r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\less_50_buses\savnw.sav""")
    psspy.dyre_new([1, 1, 1, 1], path_to_case + dyr_filename, "", "", "")
    psspy.fdns([0, 0, 0, 1, 1, 0, 0, 0])  # solve power flow

    run_parm_sens_routine(path_to_case)