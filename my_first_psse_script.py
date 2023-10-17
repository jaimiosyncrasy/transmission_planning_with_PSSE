import psse35
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

path_to_cases="C:/Users/jaimi/OneDrive/Documents/PTI/PSSE35/my_cases/3bus/"
filename="3bus.sav"
psspy.psseinit()
psspy.case(path_to_cases+filename)
psspy.fdns([0,0,0,1,1,0,99,0])
print('---------')
parse_return('abusreal',psspy.abusreal(string='KV'))
parse_return('aflowreal',psspy.aflowreal(string='TONUMBER'))
