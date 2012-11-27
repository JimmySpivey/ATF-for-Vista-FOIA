'''
Created on Sep 28, 2012

@author: jspivey
'''
import time
from Actions import Actions
import logging


class RCActions(Actions):
    '''
    classdocs
    '''

    def __init__(self, VistAconn, scheduling=None, user=None, code=None):
        Actions.__init__(self, VistAconn, scheduling, user, code)
        
    def signon (self):
        #self.VistA.wait('');
        #self.VistA.write('D ^ZU')
        self.VistA.wait("ACCESS CODE:");
        self.VistA.write(self.acode)
        self.VistA.wait('VERIFY CODE:');
        self.VistA.write(self.vcode)
        #self.VistA.wait('//');
        #self.VistA.write('')

    def signoff (self):
        self.VistA.write('^')
        #self.VistA.client.close()
        '''
        if self.acode is None:
            self.VistA.write('^\r^\r^\rh\r')
        else:
            self.VistA.write('^\r^\r^\r\r\r\r')
        '''