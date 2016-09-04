# -*- coding: utf-8 -*-
env = {
    'process': None,  # process for streaming
    'auth': False,    # authentication status
    'operator': None, # current operator ('None' means idle)
    'mode': 'digital',

    'buttons': 0x0,   # buttons status
    'switches': 0x0   # switches status

    # Following fields will be set after authentication
    # 
    # 'rtmp_host': 'xx.xx.xx.xx'
    # 'rtmp_port': xxxx
    # 'rtmp_app': 'xxx'
    # 'rtmp_stream': 'xxx'
    # 
    # 'file_url': 'xxx.xxx.xxx/xxx/xxx'
    
    # After downloading bit file
    # 'bit_file': '/xxx/xxx'
}
