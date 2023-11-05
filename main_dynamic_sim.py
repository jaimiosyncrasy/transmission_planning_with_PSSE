import psse35 # this must come before 'import psspy' for psspy to be found!
import psspy
from utils import open_case
psspy.set_fpcw_py() # for dyntools
import os, sys, collections # for dyntools
from dyntools_demo import test1_data_extraction
# File:"C:\Users\jaimi\Downloads\recording_dyn_sim.py", generated on SUN, NOV 05 2023  13:36, PSS(R)E Xplore release 35.05.03


path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/EXAMPLE/less_50_buses/"
sav_filename= "savnw.sav"
dyr_filename="savnw.dyr"""
output_filename= "savnw_out1.out"""
psspy.psseinit()

# psspy.lines_per_page_one_device(1, 10000000)
# outdir=path_to_cases
# prgfile  = os.path.join(outdir,'progress.txt')
# psspy.progress_output(2, prgfile, [0, 0])

open_case(path_to_cases + sav_filename)

# psspy.case(r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\less_50_buses\savnw.sav""")
psspy.dyre_new([1,1,1,1],path_to_cases+dyr_filename,"","","")
psspy.fdns([0,0,0,1,1,0,0,0]) # solve power flow
# convert loads and generators to prep for dynamic sim
psspy.cong(0)
psspy.conl(0,1,1,[0,0],[100.0,0.0,0.0,100.0])
psspy.conl(0,1,2,[0,0],[100.0,0.0,0.0,100.0])
psspy.conl(0,1,3,[0,0],[100.0,0.0,0.0,100.0])
# factorize admittance matrix
psspy.fact()
# perform a simplified low flow
psspy.tysl(0)
# define output channels
psspy.bsys(0,0,[13.8,500.],1,[1],0,[],0,[],0,[]) # define bus subsystem for channel outputs
psspy.chsb(0,0,[-1,-1,-1,1,12,0])
psspy.chsb(0,0,[-1,-1,-1,1,13,0])
psspy.chsb(0,0,[-1,-1,-1,1,16,0])
psspy.chsb(0,0,[-1,-1,-1,1,17,0])
# set reference generator
psspy.set_relang(1,101,r"""1""")
# initialize dynamic sim
outvrsn=0 # 0 for .out, 1 for .outx
err=psspy.set_chnfil_type(outvrsn)
psspy.strt_2([0,0], path_to_cases + output_filename)
# run dynamic sim (start, end, options)
psspy.run(0,1.0,0,1,1)
psspy.dist_3phase_bus_fault(151,0,1,500.0,[0.0,-0.2E+10])
psspy.run(0,1.1,0,1,1)
psspy.dist_clear_fault(1)
print('finishing dynamic sim...')
psspy.run(0,10.0,0,1,1)

# ------------------------------- save outputs -----------------------------------
# pssplot.plot_book("")
# pssplot.plot_page(r"""Plot Book 1""",0,"",[2,0,2,2],[1.,1.])
# pssplot.plot_plot(r"""Plot Book 1""",1,0,"",[0,0,1,1,0,2,0],[0.0,0.0,100.,100.])
# pssplot.plot_plot_chng(r"""Plot Book 1""",1,1,r"""
# """,[0,0,1,1,1,0,0],[0.0,0.0,0.0,0.0])
# pssplot.plot_trace_channel(r"""Plot Book 1""",1,1,0,r"""3 - FREQ    151 [NUCPANT     500.00] : savnw_out1.out""",1,r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\less_50_buses\savnw_out1.out""",
# r"""3 - FREQ    151 [NUCPANT     500.00]""",[-1,-1,-1,16777215])
# pssplot.plot_plot_chng(r"""Plot Book 1""",1,1,r"""
# """,[0,0,1,1,1,0,0],[0.0,0.0,0.0,0.0])
# pssplot.plot_trace_channel(r"""Plot Book 1""",1,1,0,r"""9 - VOLT    151 [NUCPANT     500.00] : savnw_out1.out""",1,r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\less_50_buses\savnw_out1.out""",
# r"""9 - VOLT    151 [NUCPANT     500.00]""",[-1,-1,-1,16777215])

# psspy.lines_per_page_one_device(2, 10000000)
# psspy.progress_output(1, "", [0, 0])

output_txt_folder = "output_data"
output_txt_filename="dyn_sim_savnw.txt"
outpath = os.path.join(os.getcwd(), output_txt_folder)
if not os.path.exists(outpath): os.mkdir(outpath)

test1_data_extraction(outpath=outpath, output_txt_filename=output_txt_filename,show=False, outvrsn=outvrsn, prg2file=True,outfile=path_to_cases+output_filename)

psspy.set_fpcw_psse() # for dyntools