import math
import psspy

def parse_return(func_name,lst):
    '''interpret the items returned from func call'''
    if len(lst)!=2:
        print('func {} doesnt return 2 items; expected return of (ierr,iarrray)'.format(func_name))
    err,res=lst
    if err == 0:
        print('{} result={}'.format(func_name,res[0]))
        return res
    else:
        print('{} error code={}'.format(func_name,err))
        return None

def get_duplicate_idx(seq):
    idx_to_remove=[]
    seq_so_far=[]
    for i in range(len(seq)):
        if any([math.isclose(seq[i],a,abs_tol=1e-9) for a in seq_so_far]):
            idx_to_remove.append(i)
        seq_so_far.append(seq[i])
    return idx_to_remove

def bus_exists(bus_num):
    nwk_buses=psspy.abusint(string=['NUMBER'])[1][0]
    if bus_num not in nwk_buses:
        print('bus {} not in nwk {}'.format(bus_num,nwk_buses))
        return False
    else:
        return True

def open_case(path_and_file):
    err_code=psspy.case(path_and_file)
    if err_code== 0:
        return
    elif err_code== 1:
        raise Exception('error opening file: file is blank')
    elif err_code== 2:
        print('error reading the case file')
        raise Exception('error reading file')
    elif err_code== 3:
        raise Exception('error opening file: file not found')

