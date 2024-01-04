# File:"C:\Users\jaimi\Downloads\recording5.py", generated on THU, JAN 04 2024  11:59, PSS(R)E Xplore release 35.05.03
psspy.change_plmod_con(2,r"""1""",r"""SEXS""",3,28.0)
psspy.fdns([0,0,0,1,1,0,99,0])
psspy.fdns([0,0,0,1,1,0,99,0])
psspy.fdns([0,0,0,1,1,0,99,0])
psspy.opendiagfile(r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\2.Brazilian_7_bus_Equivalent_Model_V32_Files\PSSE\Brazilian_7_bus_Equiv_Model.sld""")
psspy.closediagfile()
psspy.opendiagfile(r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\2.Brazilian_7_bus_Equivalent_Model_V32_Files\PSSE\Brazilian_7_bus_Equiv_Model.sld""")

psspy.fdns([0,0,0,1,1,0,99,0])
psspy.conl(0,1,1,[0,0],[100.0,0.0,0.0,100.0])
psspy.conl(0,1,2,[0,0],[100.0,0.0,0.0,100.0])
psspy.conl(0,1,3,[0,0],[100.0,0.0,0.0,100.0])
psspy.fact()
psspy.tysl(0)

psspy.change_plmod_con(2,r"""1""",r"""SEXS""",3,29.0) # change parms
psspy.change_plmod_con(2,r"""1""",r"""IEEEST""",13,11.0) # change parms
psspy.chsb(0,1,[-1,-1,-1,1,12,0])
psspy.chsb(0,1,[-1,-1,-1,1,13,0])
psspy.chsb(0,1,[-1,-1,-1,1,16,0])
psspy.strt_2([0,0],r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\2.Brazilian_7_bus_Equivalent_Model_V32_Files\PSSE\parms_29_and_11.out""")
psspy.run(0,1.0,0,1,1)
psspy.dist_3phase_bus_fault(4,0,1,765.0,[0.0,-0.2E+10])
psspy.run(0,1.1,0,1,1)
psspy.dist_clear_fault(1)
psspy.run(0,4.0,0,1,1)

psspy.change_plmod_con(2,r"""1""",r"""SEXS""",3,25.0) # change parms
psspy.change_plmod_con(2,r"""1""",r"""IEEEST""",13,8.0) # change parms
psspy.strt_2([0,0],r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\2.Brazilian_7_bus_Equivalent_Model_V32_Files\PSSE\parms_25_and_8.out""")
psspy.run(0,1.0,0,1,1)
psspy.dist_3phase_bus_fault(4,0,1,765.0,[0.0,-0.2E+10])
psspy.run(0,1.1,0,1,1)
psspy.dist_clear_fault(1)
psspy.run(0,4.0,0,1,1)

psspy.change_plmod_con(2,r"""1""",r"""SEXS""",3,35.0) # change parms
psspy.change_plmod_con(2,r"""1""",r"""IEEEST""",13,13.0) # change parms
psspy.strt_2([0,0],r"""C:\Users\jaimi\OneDrive\Documents\PTI\PSSE35\EXAMPLE\2.Brazilian_7_bus_Equivalent_Model_V32_Files\PSSE\parms_35_and_13.out""")
psspy.run(0,1.0,0,1,1)
psspy.dist_3phase_bus_fault(4,0,1,765.0,[0.0,-0.2E+10])
psspy.run(0,1.1,0,1,1)
psspy.dist_clear_fault(1)
psspy.run(0,4.0,0,1,1)

