#
# Darwin Robotics, 2020
#

'''
This module provides printing utilities.
'''

from datetime import datetime

DEBUG = True

def log(msg, status='info'):
    '''
    log is a customized print function.
    
    :param data: the data to and print.
    '''
    if not DEBUG:
        return    
    if status == 'ok':
        prefix = '[\033[92m  OK  \033[0m] '
    if status == 'error':
        prefix = '[\033[91m EROR \033[0m] '
    if status == 'info':
        prefix = '[\033[94m INFO \033[0m] '

    print('{}[{}] {}\n'.format(prefix,datetime.now().time(),msg))

def debug(msg):
    '''
    debug prints message if the program is in debug mode.
    
    :param msg: the message to print when in debug mode.
    '''
    if DEBUG:
        prefix = '[\033[36m DBUG \033[0m] '
        print('{}[{}] {}\n'.format(prefix,datetime.now().time(),msg))

def vlog(data: dict):
    '''
    vlog is a customized print function that vertically expands a dictionary and prints it.
    Useful for tradebots, stock data, etc.
    
    :param data: the data to vertically expand and print.
    '''
    content = '\n'
    for key in data.keys():
        content += f'{key} : {data[key]}\n'
    log(content)
