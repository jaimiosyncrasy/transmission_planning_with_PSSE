from assess_circuit import Branch
from utils import bus_exists, parse_return
import psspy

def add_bus(type,num,base_kva):
    # bus_data_4(ibus, inode, intgar, realar, name)
    _i,_f,_s,_o=psspy._i,psspy._f,psspy._s,psspy._o
    code1=psspy.bus_data_4(num, 0, [type, 1, 1, 1], [0.0, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], "")
    code2=psspy.bus_chng_4(num, 0, [_i, _i, _i, _i], [base_kva, _f, _f, _f, _f, _f, _f], r"""MYNAME""")
    # psspy.bus_number(101, 676)
    if code1!=0 or code2!=0:
        raise Exception('error adding load')
    return True

def add_load(bus_num,loadP,loadQ):
    '''adds load if doesnt already exist; or modifies existing load at the bus'''
    assert bus_exists(bus_num)
    _i,_f,_s,_o=psspy._i,psspy._f,psspy._s,psspy._o
    code1=psspy.load_data_6(bus_num,r"""1""",[1,1,1,1,1,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    code2=psspy.load_chng_6(bus_num,r"""1""",[_i,_i,_i,_i,_i,_i,_i],[loadP,loadQ,_f,_f,_f,_f,_f,_f],"")
    if code1!=0 or code2!=0:
        raise Exception('error adding load')
    return True
def add_br(FROM_BR_NUM,TO_BR_NUM,parm_dict):
    X,R,MAX_MVA=parm_dict['X'],parm_dict['R'],parm_dict['MAX_MVA']
    assert bus_exists(FROM_BR_NUM)
    assert bus_exists(TO_BR_NUM)
    ID='19' # todo: generalize this
    _i,_f,_s,_o=psspy._i,psspy._f,psspy._s,psspy._o
    code1=psspy.branch_data_3(FROM_BR_NUM,TO_BR_NUM,ID,[1,FROM_BR_NUM,1,_i,_i,_i],[R,X,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[MAX_MVA,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"")
    # code2=psspy.branch_chng_3(FROM_BR_NUM,TO_BR_NUM,r"""19""",[_i,_i,_i,_i,_i,_i],[R,X,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[MAX_MVA,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""MYNAME""")
    code2=0
    # note: r"""1""" is equivalent to '1'
    # loadP,loadQ=51,21
    # psspy.load_data_6(671,r"""1""",[1,1,1,1,1,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    # psspy.load_chng_6(671,r"""1""",[_i,_i,_i,_i,_i,_i,_i],[loadP,loadQ,_f,_f,_f,_f,_f,_f],"")
    #
    if code1!=0 or code2!=0:
        print('error adding branch. add br err={},change br err={}'.format(code1,code2))
        psspy.purgbrn(FROM_BR_NUM,TO_BR_NUM,ID) # remove incorrectly added branch
        return None
    else:
        len_br_lst=len(parse_return('aflowint', psspy.aflowint(string=['FROMNUMBER']))[0])
        return Branch(ID,FROM_BR_NUM,TO_BR_NUM,len_br_lst-1)