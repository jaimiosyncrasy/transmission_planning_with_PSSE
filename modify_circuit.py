from utils import bus_exists
import psspy

def add_bus(type,num,base_kva):
    # bus_data_4(ibus, inode, intgar, realar, name)
    _i,_f,_s,_o=psspy._i,psspy._f,psspy._s,psspy._o
    psspy.bus_data_4(num, 0, [type, 1, 1, 1], [0.0, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], "")
    psspy.bus_chng_4(num, 0, [_i, _i, _i, _i], [base_kva, _f, _f, _f, _f, _f, _f], r"""MYNAME""")
    # psspy.bus_number(101, 676)

def add_load(bus_num,loadP,loadQ):
    '''adds load if doesnt already exist; or modifies existing load at the bus'''
    assert bus_exists(bus_num)
    _i,_f,_s,_o=psspy._i,psspy._f,psspy._s,psspy._o
    psspy.load_data_6(bus_num,r"""1""",[1,1,1,1,1,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    psspy.load_chng_6(bus_num,r"""1""",[_i,_i,_i,_i,_i,_i,_i],[loadP,loadQ,_f,_f,_f,_f,_f,_f],"")

def add_br(FROM_BR_NUM,TO_BR_NUM,parm_dict):
    X,R,MAX_MVA=parm_dict['X'],parm_dict['R'],parm_dict['MAX_MVA']
    assert bus_exists(FROM_BR_NUM)
    assert bus_exists(TO_BR_NUM)
    psspy.branch_data_3(FROM_BR_NUM,TO_BR_NUM,r"""3""",[1,FROM_BR_NUM,1,0,0,0],[0.0,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    _i,_f,_s,_o=psspy._i,psspy._f,psspy._s,psspy._o
    psspy.branch_chng_3(FROM_BR_NUM,TO_BR_NUM,r"""3""",[_i,_i,_i,_i,_i,_i],[R,X,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[MAX_MVA,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],_s)
    # loadP,loadQ=51,21
    # psspy.load_data_6(671,r"""1""",[1,1,1,1,1,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    # psspy.load_chng_6(671,r"""1""",[_i,_i,_i,_i,_i,_i,_i],[loadP,loadQ,_f,_f,_f,_f,_f,_f],"")
    #
