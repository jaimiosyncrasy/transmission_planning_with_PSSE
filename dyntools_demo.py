#[dyntools_demo.py]  Demo for using functions from dyntools module
# ====================================================================================================
'''
'dyntools' module provide access to data in PSS(R)E Dynamic Simulation Channel Output file.
This module has functions:
- to get channel data in Python scripts for further processing
- to get channel information and their min/max range
- to export data to text files, excel spreadsheets
- to open multiple channel output files and post process their data using Python scripts
- to plot selected channels
- to plot and insert plots in word document

This is an example file showing how to use various functions available in dyntools module.

Other Python modules 'matplotlib', 'numpy' and 'python win32 extension' are required to be
able to use 'dyntools' module.
Self installation EXE files for these modules are available at:
   PSSE User Support Web Page and follow link 'Python Modules used by PSSE Python Utilities'.

- This version of the dyntools module is developed and tested using these open source modules.
  Python 3.7.3 [64 bit]
  matplotlib-3.1.1
  numpy-1.16.4
  pywin32-224

  Versions later than these may work.

---------------------------------------------------------------------------------
How to use this file?
- Open Python IDLE (or any Python Interpreter shell)
- Open this file
- run (F5)

Note: Do NOT run this file from PSS(R)E GUI. The 'xyplots' function from dyntools can
save plots to eps, png, pdf or ps files. However, creating only 'eps' files from inside
PSS(R)E GUI works. This is because different backends matplotlib uses to create different
plot types.
When run from any Python interpreter (outside PSS(R)E GUI) plots can be saved to any of
these four (eps, png, pdf or ps) file types.

Get information on functions available in dyntools as:
import dyntools
help(dyntools)

---------------------------------------------------------------------------------
How to use PSSE and Python modules like numpy, matplotlib together?
(a) In your python script, call following function before any of these modules are imported.
    psspy.set_fpcw_py()
(b) Call following function before exiting your python script.
    psspy.set_fpcw_psse()
To get details why this is needed, get help(..) on either of these functions.
Refer function test2_subplots_one_trace(..) in this script for usage of these functions.

'''

import os, sys, collections

# =============================================================================================
def get_demotest_file_names(outdir, outvrsn):
    '''sets the name of a 'process' txt file, and returns a set of .out filenames'''

    if outvrsn==0:
        extn = '.out'
        prgfile  = os.path.join(outdir,'progress.txt')
    else:
        extn = '.outx'
        prgfile  = os.path.join(outdir,'progressX.txt')

    outfile1 = os.path.join(outdir,'bus154_fault{}'.format(extn))
    outfile2 = os.path.join(outdir,'bus3018_gentrip{}'.format(extn))
    outfile3 = os.path.join(outdir,'brn3005_3007_trip{}'.format(extn))

    return outfile1, outfile2, outfile3, prgfile

# =============================================================================================
# PSSE version Example folder
def get_example_folder():
    import psspy
    pn = os.path.dirname(psspy.__file__) # dir where dyntools library sits (..PSSE35/35.5/PSSPYY39)
    p, jnk = os.path.split(pn)
    example_dir = os.path.join(p, 'Example')
    return example_dir

# =============================================================================================
# Run Dynamic simulation on SAVNW case to generate .out files

def run_savnw_simulation(datapath, outfile1, outfile2, outfile3, prgfile, outvrsn):

    import psspy
    psspy.psseinit()

    examdir = get_example_folder()

    savfile = 'savcnv.sav'
    snpfile = 'savnw.snp'

    if not datapath: datapath = get_example_folder() # datapath is the path to the case files (.snp,.sav,etc)

    savfile = os.path.join(datapath, savfile)
    snpfile = os.path.join(datapath, snpfile)

    psspy.lines_per_page_one_device(1,10000000)
    psspy.progress_output(2,prgfile,[0,0])

    ierr = psspy.case(savfile)
    if ierr:
        psspy.progress_output(1,"",[0,0])
        print(" psspy.case Error")
        return
    ierr = psspy.rstr(snpfile)
    if ierr:
        psspy.progress_output(1,"",[0,0])
        print(" psspy.rstr Error")
        return

    psspy.set_chnfil_type(outvrsn)

    psspy.strt(0,outfile1)
    psspy.run(0, 1.0,1000,1,0)
    psspy.dist_bus_fault(154,1, 230.0,[0.0,-0.2E+10])
    psspy.run(0, 1.05,1000,1,0)
    psspy.dist_clear_fault(1)
    psspy.run(0, 5.0,1000,1,0)

    psspy.case(savfile)
    psspy.rstr(snpfile)
    psspy.strt(0,outfile2)
    psspy.run(0, 1.0,1000,1,0)
    psspy.dist_machine_trip(3018,'1')
    psspy.run(0, 5.0,1000,1,0)

    psspy.case(savfile)
    psspy.rstr(snpfile)
    psspy.strt(0,outfile3)
    psspy.run(0, 1.0,1000,1,0)
    psspy.dist_branch_trip(3005,3007,'1')
    psspy.run(0, 5.0,1000,1,0)

    psspy.lines_per_page_one_device(2,10000000)
    psspy.progress_output(1,"",[0,0])

# =============================================================================================
# 0. Run savnw dynamics simulation to create .out files

def test0_run_simulation(datapath=None, outpath=None, outvrsn=0):

    outfile1, outfile2, outfile3, prgfile = get_demotest_file_names(outpath, outvrsn)
    run_savnw_simulation(datapath, outfile1, outfile2, outfile3, prgfile, outvrsn)

    print(" Test0:Done SAVNW dynamics simulation")

# =============================================================================================
# 1. Data extraction/information

def test1_data_extraction(outpath=None, output_txt_filename='test1_dyntools.txt',show=True, outvrsn=0, prg2file=True, outfile=None):
    '''extracts data from .out and puts it into a table in a .txt, .csv, and .xlsx files'''
    import psspy
    import dyntools

    outfile1, outfile2, outfile3, prgfile = get_demotest_file_names(outpath, outvrsn)
    outfile=outfile1 # read just first .out file

    # create object
    chnfobj = dyntools.CHNF(outfile, outvrsn=outvrsn) # read just first .out file

    if chnfobj.ierr: return # if failed to access output file, return and print error

    if prg2file:
        p, nx = os.path.split(outfile)
        n, x  = os.path.split(nx)
        rptnam = output_txt_filename.format(n)
        if outpath:
            rptfile = os.path.join(outpath, rptnam)
        else:
            rptfile = os.path.join(p, rptnam)
        rptfile_h = open(rptfile,'w')
        report = rptfile_h.write
    else:
        report = sys.stdout.write

    report('\n Test1:Testing call to get_data\n')
    #sh_ttl, ch_id, ch_data = chnfobj.get_data()
    sh_ttl, ch_id, ch_data = chnfobj.get_data(['time', 4, 5, 55])
    #sh_ttl, ch_id, ch_data = chnfobj.get_data('')
    #sh_ttl, ch_id, ch_data = chnfobj.get_data([4, 5, 55])
    s_in = [str(ch) for ch in ch_data.keys()]
    s_ch = ', '.join(s_in)
    report(sh_ttl)
    report("{}".format(ch_id))
    report(" Test1:Data extracted for Channels = {}\n".format(s_ch))

    report('\n Test1:Testing call to get_id\n')
    sh_ttl, ch_id = chnfobj.get_id()
    report(sh_ttl)
    report("{}".format(ch_id))
    report('\n')

    report('\n Test1:Testing call to get_range\n')
    ch_range = chnfobj.get_range()
    report("{}".format(ch_range))
    report('\n')

    report('\n Test1:Testing call to get_scale\n')
    ch_scale = chnfobj.get_scale()
    report("{}".format(ch_scale))
    report('\n')

    if not prg2file:
        report('\n Test1:Testing call to print_scale\n')
        chnfobj.print_scale()
        report('\n')

    pn, x = os.path.splitext(outfile)

    report('\n Test1:Testing call to txtout\n')
    chnfobj.txtout(channels=[1,4], txtfile=pn)
    report('\n')

    report('\n Test1:Testing call to csvout\n')
    chnfobj.csvout(channels=[1,4,41,5], csvfile=pn)
    report('\n')

    report('\n Test1:Testing call to xlsout\n')
    try:
        chnfobj.xlsout(channels=[2,3,4,7,8,10], show=show, xlsfile=pn)
    except:
        pass

    if prg2file:
        rptfile_h.close()
        txt = ' Test1_data_extraction report saved to file:\n    {}\n'.format(rptfile)
        print(txt)

# =============================================================================================
# 2. Multiple subplots in a figure, but one trace in each subplot
#    Channels specified with normal dictionary

# See how "set_plot_legend_options" method can be used to place and format legends

def test2_subplots_one_trace(outpath=None, show=True, outvrsn=0):
    '''for each .out, plots multiple suplots in 1 figure'''
    import psspy
    import dyntools
    psspy.set_fpcw_py()     # To use PSSE, numpy and matplotlib, this is needed.

    outfile1, outfile2, outfile3, prgfile = get_demotest_file_names(outpath, outvrsn)

    chnfobj = dyntools.CHNF(outfile1, outfile2, outvrsn=outvrsn)

    chnfobj.set_plot_page_options(size='letter', orientation='portrait')
    chnfobj.set_plot_markers('square', 'triangle_up', 'thin_diamond', 'plus', 'x',
                             'circle', 'star', 'hexagon1')
    chnfobj.set_plot_line_styles('solid', 'dashed', 'dashdot', 'dotted')
    chnfobj.set_plot_line_colors('blue', 'red', 'black', 'green', 'cyan', 'magenta', 'pink', 'purple')

    optnfmt  = {'rows':2,'columns':2,'dpi':300,'showttl':True, 'showoutfnam':True, 'showlogo':True,
                'legendtype':1, 'addmarker':True}

    optnchn1 = {1:{'chns':6,                'title':'Ch#6,bus154_fault, P(pu)'},
                2:{'chns':[6, 'v*100'],     'title':'Ch#6,bus154_fault, P(MW)'},
                3:{'chns':11,               'title':'Ch#11,bus154_fault'},
                4:{'chns':40,               'title':'Ch#40,bus154_fault'},
                5:{'chns':26,               'title':'Ch#26,bus154_fault, Frequency (pu)'},
                6:{'chns':[26, '(1+v)*60'], 'title':'Ch#26,bus154_fault, Frequency (Hz)'},
                }
    pn,x     = os.path.splitext(outfile1)
    pltfile1 = pn+'.pdf'

    optnchn2 = {1:{'chns':{outfile2:6},                'title':'Channel 6 from bus3018_gentrip, P(pu)'},
                2:{'chns':{outfile2:[6, 'v*100']},     'title':'Channel 6 from bus3018_gentrip, P(MW)'},
                3:{'chns':{outfile2:11}},
                4:{'chns':{outfile2:16}},
                5:{'chns':{outfile2:26},               'title':'Ch#26,bus3018_gentrip, Frequency (pu)'},
                6:{'chns':{outfile2:[26, '(1+v)*60']}, 'title':'Ch#26,bus3018_gentrip, Frequency (Hz)'},
                }
    pn,x     = os.path.splitext(outfile2)
    pltfile2 = pn+'.png'

    figfiles1 = chnfobj.xyplots(optnchn1,optnfmt,pltfile1)

    chnfobj.set_plot_legend_options(loc='lower center', borderpad=0.2, labelspacing=0.5,
                                    handlelength=1.5, handletextpad=0.5, fontsize=8, frame=False)

    optnfmt  = {'rows':3,'columns':1,'dpi':300,'showttl':False, 'showoutfnam':True, 'showlogo':False,
                'legendtype':2, 'addmarker':False}

    figfiles2 = chnfobj.xyplots(optnchn2,optnfmt,pltfile2)

    if figfiles1 or figfiles2:
        txt = ' Test2:Plot files saved:\n'
        if figfiles1: txt += "     {}\n".format(figfiles1[0])
        if figfiles2: txt += "     {}\n".format(figfiles2[0])
        print(txt)

    if show:
        chnfobj.plots_show()
    else:
        chnfobj.plots_close()

    psspy.set_fpcw_psse()   # To use PSSE, numpy and matplotlib, this is needed.

# =============================================================================================
# 3. Multiple subplots in a figure and more than one trace in each subplot
#    Channels specified with normal dictionary

def test3_subplots_mult_trace(outpath=None, show=True, outvrsn=0):

    import psspy
    import dyntools
    psspy.set_fpcw_py()     # To use PSSE, numpy and matplotlib, this is needed.

    outfile1, outfile2, outfile3, prgfile = get_demotest_file_names(outpath, outvrsn)

    chnfobj = dyntools.CHNF(outfile1, outfile2, outfile3, outvrsn=outvrsn)

    chnfobj.set_plot_page_options(size='letter', orientation='portrait')
    chnfobj.set_plot_markers('square', 'triangle_up', 'thin_diamond', 'plus', 'x',
                             'circle', 'star', 'hexagon1')
    chnfobj.set_plot_line_styles('solid', 'dashed', 'dashdot', 'dotted')
    chnfobj.set_plot_line_colors('blue', 'red', 'black', 'green', 'cyan', 'magenta', 'pink', 'purple')

    optnfmt  = {'rows':2,'columns':2,'dpi':300,'showttl':False, 'showoutfnam':True, 'showlogo':False,
                'legendtype':2, 'addmarker':True}

    optnchn1 = {1:{'chns':[1]},2:{'chns':[2]},3:{'chns':[3]},4:{'chns':[4]},5:{'chns':[5]}}
    pn,x     = os.path.splitext(outfile1)
    pltfile1 = pn+'.png'

    optnchn2 = {1:{'chns':{outfile2:1}},
                2:{'chns':{'v82_test1_bus_fault.out':3}},
                3:{'chns':4},
                4:{'chns':[5]}
               }
    pn,x     = os.path.splitext(outfile2)
    pltfile2 = pn+'.pdf'

    optnchn3 = {1:{'chns':{outfile1:1}},
                2:{'chns':{outfile2:[1,5]}},
                3:{'chns':{outfile3:3}},
                4:{'chns':[4,'v-v0',5,'v-v0']},  # arbitrary function
               }
    pn,x     = os.path.splitext(outfile3)
    pltfile3 = pn+'.png'

    figfiles1 = chnfobj.xyplots(optnchn1,optnfmt,pltfile1)
    figfiles2 = chnfobj.xyplots(optnchn2,optnfmt,pltfile2)
    figfiles3 = chnfobj.xyplots(optnchn3,optnfmt,pltfile3)

    figfiles = figfiles1[:]
    figfiles.extend(figfiles2)
    figfiles.extend(figfiles3)
    if figfiles:
        txt = ' Test3:Plot files saved:\n'
        for f in figfiles:
            txt += "    {}\n".format(f)
        print(txt)

    if show:
        chnfobj.plots_show()
    else:
        chnfobj.plots_close()

    psspy.set_fpcw_psse()   # To use PSSE, numpy and matplotlib, this is needed.

# =============================================================================================
# 4. Multiple subplots in a figure, but one trace in each subplot
#    Channels specified with Ordered dictionary

def test4_subplots_mult_trace_OrderedDict(outpath=None, show=True, outvrsn=0):

    import psspy
    import dyntools
    psspy.set_fpcw_py()     # To use PSSE, numpy and matplotlib, this is needed.

    outfile1, outfile2, outfile3, prgfile = get_demotest_file_names(outpath, outvrsn)

    chnfobj = dyntools.CHNF(outfile1, outfile2, outfile3, outvrsn=outvrsn)

    chnfobj.set_plot_page_options(size='letter', orientation='portrait')
    chnfobj.set_plot_markers('square', 'triangle_up', 'thin_diamond', 'plus', 'x',
                             'circle', 'star', 'hexagon1')
    chnfobj.set_plot_line_styles('solid', 'dashed', 'dashdot', 'dotted')
    chnfobj.set_plot_line_colors('blue', 'red', 'black', 'green', 'cyan', 'magenta', 'pink', 'purple')

    optnfmt  = {'rows':2,'columns':1,'dpi':300,'showttl':False, 'showoutfnam':True, 'showlogo':False,
                'legendtype':2, 'addmarker':True}

    optnchn  = {1:{'chns':collections.OrderedDict([(outfile1,26), (outfile2,26), (outfile3,26)]),
                   'title':'Frequency(pu)'},
                2:{'chns':collections.OrderedDict([(outfile1,[26, '(1+v)*60']),
                                                   (outfile2,[26, '(1+v)*60']),
                                                   (outfile3,[26, '(1+v)*60'])]),
                   'title':'Frequency(Hz)'}
               }
    p,nx     = os.path.split(outfile1)
    pltfile  = os.path.join(p, 'plot_chns_ordereddict.png')

    figfiles = chnfobj.xyplots(optnchn,optnfmt,pltfile)

    if figfiles:
        txt = ' Test4:Plot files saved:\n'
        for f in figfiles:
            txt += "    {}\n".format(f)
        print(txt)

    if show:
        chnfobj.plots_show()
    else:
        chnfobj.plots_close()

    psspy.set_fpcw_psse()   # To use PSSE, numpy and matplotlib, this is needed.

# =============================================================================================
# 5. Do XY plots and insert them into word file
# Does not work because win32 API to Word does not work.

def test5_plots2word(outpath=None, show=True, outvrsn=0):

    import psspy
    import dyntools
    psspy.set_fpcw_py()     # To use PSSE, numpy and matplotlib, this is needed.

    outfile1, outfile2, outfile3, prgfile = get_demotest_file_names(outpath, outvrsn)

    chnfobj = dyntools.CHNF(outfile1, outfile2, outfile3, outvrsn=outvrsn)

    p,nx       = os.path.split(outfile1)
    docfile    = os.path.join(p,'savnw_response')
    overwrite  = True
    caption    = True
    align      = 'center'
    captionpos = 'below'
    height     = 0.0
    width      = 0.0
    rotate     = 0.0

    optnfmt  = {'rows':3,'columns':1,'dpi':300,'showttl':True}

    optnchn  = {1:{'chns':{outfile1:1,  outfile2:1,  outfile3:1} },
                2:{'chns':{outfile1:[7,'v*100'],  outfile2:[7,'v*100'],  outfile3:[7,'v*100']} },
                3:{'chns':{outfile1:17, outfile2:17, outfile3:17} },
                4:{'chns':[1,2,3,4,5]},
                5:{'chns':{outfile2:[26,'(1+v)*60',27,'(1+v)*60',28,'(1+v)*60',29,'(1+v)*60']},
                   'title':'Frequency(Hz)'},
                6:{'chns':{outfile3:[1,2,3,4,5]} },
               }
    ierr, docfile = chnfobj.xyplots2doc(optnchn,optnfmt,docfile,show,overwrite,caption,align,
                        captionpos,height,width,rotate)

    if not ierr:
        txt  = ' Test5:Plots saved to file:\n    {}'.format(docfile)
        print(txt)
    else:
        txt  = ' Test5:Error saving plots to Word = {}'.format(ierr)
        print(txt)

    psspy.set_fpcw_psse()   # To use PSSE, numpy and matplotlib, this is needed.

# =============================================================================================
# Run all tests and save plot and report files.

def run_all_tests(outvrsn, datapath=None, prg2file=True):

    show = False

    run_tests('all', outvrsn, show, datapath=datapath, prg2file=prg2file)

# =============================================================================================

def run_tests(which, outvrsn, show, datapath=None, prg2file=True):

    import psspy

    datapath = datapath # path to the case files (.snp,.sav,etc)

    folder_of_outputs  = "dyntools_demo_output_outvrn{}".format(outvrsn)
    outpath = os.path.join(os.getcwd(), folder_of_outputs)
    if not os.path.exists(outpath): os.mkdir(outpath)

    if which in [0, 'all']:
        print(" <<<<<< Begin TEST=0 >>>>>>")
        test0_run_simulation(datapath, outpath, outvrsn)
        print(" Output files folder:{}".format(outpath))

    if which in [1, 'all']:
        print(" <<<<<< Begin TEST=1 >>>>>>")
        test1_data_extraction(outpath=outpath, show=show, outvrsn=outvrsn, prg2file=prg2file)

    if which in [2, 'all']:
        print(" <<<<<< Begin TEST=2 >>>>>>")
        test2_subplots_one_trace(outpath, show, outvrsn)

    if which in [3, 'all']:
        print(" <<<<<< Begin TEST=3 >>>>>>")
        test3_subplots_mult_trace(outpath, show, outvrsn)

    if which in [4, 'all']:
        print(" <<<<<< Begin TEST=4 >>>>>>")
        test4_subplots_mult_trace_OrderedDict(outpath, show, outvrsn)

    if which in [5, 'all']:
        print(" <<<<<< Begin TEST=5 >>>>>>")
        try:
            test5_plots2word(outpath, show, outvrsn)
        except:
            pass

# =============================================================================================

if __name__ == '__main__':

    import psse35

    show = True     # True  --> create, save and show Excel spreadsheets and Plots when done
                    # False --> create, save but do not show Excel spreadsheets and Plots when done

                    # Channel file format
    outvrsn = 0     # =0, for no Extended Channel output file type (.out)
                    # =1, for Extended Channel output file type (.outx) (default)

    prg2file = False

    #(a) Run one test a time
    #
    # 1) which=0
    # Need to run "test0_run_simulation(..)" before running other tests.
    #
    # 2)
    # which = 1 or 2 or 3 or 4 or 5
    # After running "test0_run_simulation(..)", run other tests one at a time with

    # which = 0
    # run_tests(which, outvrsn, show, prg2file)

    #(b) Run all tests
    #    Just uncomment next line to run all tests in this file.
    run_all_tests(outvrsn)

# =============================================================================================
