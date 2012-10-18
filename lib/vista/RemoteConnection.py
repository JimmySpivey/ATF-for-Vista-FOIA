'''
Created on Sep 12, 2012

@author: jspivey
'''

class RemoteConnectionDetails(object):
    '''
    classdocs
    '''


    def __init__(self, remote_address, username, password):
        '''
        Constructor
        '''
        self.remote_address = remote_address
        #self.remote_os = remote_os

        self.username = username
        self.password = password
