from datetime import datetime

DEBUG = True

def log(msg, status='info'):
    if not DEBUG:
        return    
    if status == 'ok':
        prefix = '[\033[92m  OK  \033[0m] '
    if status == 'error':
        prefix = '[\033[91m EROR \033[0m] '
    if status == 'info':
        prefix = '[\033[94m INFO \033[0m] '

    print('{}[{}] {}\n'.format(prefix,datetime.now().time(),msg))


def log_with_file(msg, status, **kwargs):
    log(msg,status)
    if kwargs.get('log_file') is not None:
        kwargs.get('log_file').write('[{}] {}\n'.format(datetime.now().time(), msg))



# A customized logging function, expands dictionary vertically. Feel free to add more customized functions yourselves.
def vlog(data: dict):
    content = '\n'
    for key in data.keys():
        content += f'{key} : {data[key]}\n'
    log(content)
