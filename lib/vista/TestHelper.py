'''
Created on Mar 2, 2012

@author: pbradley
'''
import csv
import logging
import argparse
import os
import errno
import datetime
import getpass
import ConfigParser

import RemoteConnection

LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}

class TestError(Exception):
    ''' Unexpected test result exception '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class CSVFileReader(object):
    '''
    classdocs
    '''

    def getfiledata (self, fname, fhkey, getrow=None):
        infile = open(fname)
        csvreader = csv.DictReader(infile, delimiter='|')
        table = {}
        for rowdata in csvreader:
            key = rowdata.pop(fhkey)
            table[key] = rowdata
        if getrow is None:
            return table
        else:
            row = {getrow: table[getrow]}
            return row

class TestSuiteDriver(object):
    '''
    classdocs

    Created on Oct 11, 2012

    Reusable code to handle driver the tests located in /tests directory. This is to prevent
    the RAS Recorder from generating code which may later need to be revised.
    @author: jspivey
    '''

    def __init__(self, test_file):
        '''
        Constructor
        '''
        self.test_file = test_file

    def generate_test_suite_details(self):
        test_suite_name = os.path.basename(self.test_file).split('_test.')[0]

        usage = "usage: %prog [options] arg"
        parser = argparse.ArgumentParser()
        parser.add_argument('resultdir', help='Result Directory')
        '''
        parser.add_argument('-s', '--remote-server', help='remote server address')
        parser.add_argument('-u', '--remote-username', help='remote ssh username')
        parser.add_argument('-p', '--remote-password', help='remote ssh password')
        '''
        parser.add_argument('-l', '--logging-level', help='Logging level', required=True)
        parser.add_argument('-f', '--logging-file', help='Logging file name')
        #TODO: edit ctest to refer to these parms below
        parser.add_argument('-i', '--instance', help='cache instance type', choices=["TRYCACHE", "GTM"], default='')
        parser.add_argument('-n', '--namespace', help='cache namespace', default='')
        args = parser.parse_args()

        logging_level = LOGGING_LEVELS.get(args.logging_level, logging.NOTSET)
        logging.basicConfig(level=logging_level, filename=args.logging_file, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.info('RESULT DIR arg: ' + str(args.resultdir))
        logging.info('LOGGING FILE arg: ' + str(args.logging_file))
        logging.info('LOGGING LEVEL arg:   ' + str(args.logging_level))
        logging.info('INSTANCE arg:   ' + str(args.instance))
        logging.info('NAMESPACE arg:   ' + str(args.namespace))

        config = ConfigParser.RawConfigParser()

        read_files = config.read(os.path.join(os.path.dirname(self.test_file), test_suite_name + '.cfg'))
        if read_files.__len__() != 1:
            raise IOError
        if config.getboolean('RemoteDetails', 'RemoteConnect'):
            remote_server = config.get('RemoteDetails', 'ServerLocation')
            '''
            uid = getpass.getpass(prompt="SSH username:") #prints to stderr if stdout isn't present, this causes ctest to fail
            pwd = getpass.getpass(prompt="SSH password:")
            '''
            uid = config.get('RemoteDetails', 'SSHUsername')
            pwd = config.get('RemoteDetails', 'SSHPassword')
            default_namespace = config.getboolean('RemoteDetails', 'UseDefaultNamespace')
            instance = config.get('RemoteDetails', 'Instance')
            if not default_namespace:
                namespace = config.get('RemoteDetails', 'Namespace')
            else:
                namespace = ''

            logging.info('Using REMOTE SERVER from config: ' + str(remote_server))
            logging.info('Using INSTANCE from config: ' + str(instance))
            logging.info('Using NAMESPACE from config: ' + str(namespace))
            remote_conn_details = RemoteConnection.RemoteConnectionDetails(remote_server,
                uid,
                pwd,
                default_namespace)
        else:
            remote_conn_details = None
            if args.instance == 'TRYCACHE':
                instance = 'cache'
            else:
                instance = args.instance
            namespace = args.namespace

        if not os.path.isdir(args.resultdir):
            try:
                os.makedirs(args.resultdir)
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise
        resfile = args.resultdir + '/' + test_suite_name + '.txt'
        if not os.path.isabs(args.resultdir):
            logging.error('EXCEPTION: Absolute Path Required for Result Directory')
            raise
        result_log = file(resfile, 'w')

        return test_suite_details(test_suite_name, result_log, args.resultdir, instance,
                           namespace, remote_conn_details)

    def pre_test_suite_run(self, test_suite_details):
        logging.info('ATF Version: ' + ATF.GIT_TAG)
        logging.info('Start ATF Test Suite \'' + test_suite_details.test_suite_name + '\'')


    def post_test_suite_run(self, test_suite_details):
        logging.info('End ATF Test Suite \'' + test_suite_details.test_suite_name + '\'')

    def exception_handling(self, test_suite_details, e):
        test_suite_details.result_log.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*******exception*******' + str(e))

    def try_else_handling(self, test_suite_details):
        outstr = 'All tests in test suite \'' + test_suite_details.test_suite_name + '\'' + ' completed without exception.'
        logging.info(outstr)
        test_suite_details.result_log.write(outstr + '\n')

    def finally_handling(self, test_suite_details):
        test_suite_details.result_log.write('finished')

    def end_method_handling(self, test_suite_details):
        pass

class TestDriver(object):
    '''
    classdocs

    Created on Oct 11, 2012

    Reusable code to handle each test run. This is to prevent the ATF Recorder
    from generating code which may later need to be revised.
    @author: jspivey
    '''

    def __init__(self, testname):
        self.testname = testname

    def pre_test_run(self, test_suite_details):
        '''
        Ran before each test.
        '''
        test_suite_details.result_log.write('\n' + self.testname + ', ' + str(datetime.datetime.today()) + ': ')
        logging.debug('\n' + self.testname + ', ' + str(datetime.datetime.today()) + ': ')

    def post_test_run(self, test_suite_details):
        pass

    def exception_handling(self, test_suite_details, e):
        test_suite_details.result_log.write(e.value)
        logging.error(self.testname + ' EXCEPTION ERROR: Unexpected test result')

    def try_else_handling(self, test_suite_details):
        outstr = 'Test ' + self.testname + ' Passed'
        logging.debug(outstr)
        test_suite_details.result_log.write(outstr + '\n')

    def finally_handling(self, test_suite_details):
        pass

    def end_method_handling(self, test_suite_details):
        pass

    def connect_VistA(self, test_suite_details):
        '''
        Generic method to connect to VistA. Inteded to be reused by the ATF
        Recorder.
        '''
        if test_suite_details.remote_conn_details:
            location = test_suite_details.remote_conn_details.remote_address
        else:
            location = '127.0.0.1'
        from OSEHRAHelper import ConnectToMUMPS, PROMPT
        VistA = ConnectToMUMPS(logfile=test_suite_details.result_dir + '/' + self.testname + '.txt',
                               instance=test_suite_details.instance, namespace=test_suite_details.namespace,
                               location=location,
                               remote_conn_details=test_suite_details.remote_conn_details)

        if not test_suite_details.remote_conn_details or not test_suite_details.remote_conn_details.default_namespace:
            try:
                VistA.ZN(VistA.namespace)
            except IndexError, no_namechange:
                pass
            VistA.wait(PROMPT)
        return VistA

class test_suite_details(object):
    '''
    A single parameter which is passed into each test. Allows for flexibility
    with parameters (adding and removing new ones without having to refactor
    existing tests).
    '''

    def __init__(self, test_suite_name, result_log, result_dir, instance,
                 namespace, remote_conn_details):
        '''
        Constructor
        '''
        self.test_suite_name = test_suite_name
        self.result_log = result_log
        self.result_dir = result_dir
        self.instance = instance
        self.namespace = namespace
        self.remote_conn_details = remote_conn_details
        

def read_suite_config_file():
    #move to a module for parsing cfg values
    config = ConfigParser.RawConfigParser() 
    from os.path import expanduser
    read_files = config.read(expanduser("~/.ATF/roles.cfg"))
    if read_files.__len__() != 1:
        raise IOError
    return config
    #move to a module for parsing cfg values
        
def fetch_access_code(test_suite_name, testname):
    config = read_suite_config_file()
    return config.get(test_suite_name+'-'+testname, 'aCode')
    
    
    '''
    from os.path import expanduser
    in_test_suite = False
    for line in  open(expanduser("~/.ATF/roles.cfg"), 'r'):
        line = line.strip()
        in_test_suite = line == test_suite_name or in_test_suite
        if line.startswith('aCode') and in_test_suite:
            return line[line.strip().rfind("="):].strip()
    '''
        
def fetch_verify_code(test_suite_name, testname):
    config = read_suite_config_file()
    return config.get(test_suite_name+'-'+testname, 'vCode')
    

#TODO: consider moving these classes/refactoring modules in general at some point
class ATF(object):
    '''
    Currently just holds version constants. These should be referred to by
    the logger so that we know what version of the ATF was ran. This will also
    require updating these constants for each release. Each time a release is
    staged, a GIT tag must be created.
    '''

    GIT_TAG = '.0' #not yet released via a git tag
    CURRENT_GIT_REPO = 'https://github.com/JimDeanSpivey/ATF-RASR'
