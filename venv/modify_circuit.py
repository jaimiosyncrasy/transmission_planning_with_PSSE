from utils import check_bus_exists
import psspy


def add_load(bus_num,loadP,loadQ):
    check_bus_exists(bus_num)
    psspy.load_data_6(bus_num,r"""1""",[1,1,1,1,1,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    psspy.load_chng_6(bus_num,r"""1""",[_i,_i,_i,_i,_i,_i,_i],[loadP,loadQ,_f,_f,_f,_f,_f,_f],"")

def add_br(FROM_BR_NUM,TO_BR_NUM,parm_dict):
    X,R=parm_dict['X'],parm_dict['R']
    check_bus_exists(FROM_BR_NUM)
    check_bus_exists(TO_BR_NUM)
    psspy.branch_data_3(FROM_BR_NUM,TO_BR_NUM,r"""3""",[1,FROM_BR_NUM,1,0,0,0],[0.0,0.0001,0.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    psspy.branch_chng_3(FROM_BR_NUM,TO_BR_NUM,r"""3""",[_i,_i,_i,_i,_i,_i],[R,X,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],_s)
    # loadP,loadQ=51,21
    # psspy.load_data_6(671,r"""1""",[1,1,1,1,1,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],"")
    # psspy.load_chng_6(671,r"""1""",[_i,_i,_i,_i,_i,_i,_i],[loadP,loadQ,_f,_f,_f,_f,_f,_f],"")
    #
