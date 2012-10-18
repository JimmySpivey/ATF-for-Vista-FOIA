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

    def __init__(self):
        '''
        Constructor
        '''

    def generate_test_suite_details(self, test_suite_name):
        usage = "usage: %prog [options] arg"
        parser = argparse.ArgumentParser()
        parser.add_argument('resultdir', help='Result Directory')
        parser.add_argument('-s', '--remote-server', help='remote server address')
        '''
        parser.add_argument('-u', '--remote-username', help='remote ssh username') #TODO: should SSH args be required
        parser.add_argument('-p', '--remote-password', help='remote ssh password')
        '''
        parser.add_argument('-l', '--logging-level', help='Logging level', required=True)
        parser.add_argument('-f', '--logging-file', help='Logging file name')
        #TODO: edit ctest to refer to these parms below
        parser.add_argument('-i', '--instance', help='cache instance type', choices=["CACHE", "GTM"], default='')
        parser.add_argument('-n', '--namespace', help='cache namespace', default='')
        args = parser.parse_args()

        logging_level = LOGGING_LEVELS.get(args.logging_level, logging.NOTSET)
        logging.basicConfig(level=logging_level, filename=args.logging_file, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        if args.remote_server and args.remote_server.__len__() != 1:
            remote_server = args.remote_server[1:] #remove first char, workaround for ctest
            uid = getpass.getpass(prompt="SSH username:") #prints to stderr if stdout isn't present, this causes ctest to fail
            pwd = getpass.getpass(prompt="SSH password:")
        else:
            remote_server = None

        logging.info('RESULT DIR: ' + str(args.resultdir))
        logging.info('LOGGING FILE: ' + str(args.logging_file))
        logging.info('LOGGING LEVEL:   ' + str(args.logging_level))
        logging.info('REMOTE SERVER: ' + remote_server)
        logging.info('INSTANCE: ' + str(args.instance))
        logging.info('NAMESPACE: ' + str(args.namespace))

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

        if remote_server:
            remote_conn_details = RemoteConnection.RemoteConnectionDetails(remote_server,
                uid,
                pwd)
        else:
            remote_conn_details = None

        return test_suite_details(test_suite_name, result_log, args.resultdir, args.instance,
                           args.namespace, remote_conn_details)

    def pre_test_suite_run(self, test_suite_details):
        logging.info('ATF Version: ' + ATF.GIT_TAG)
        logging.info('Start ATF Test Suite \'' + test_suite_details.test_suite_name + '\'')


    def post_test_suite_run(self, test_suite_details):
        logging.info('End ATF Test Suite \'' + test_suite_details.test_suite_name + '\'')

    def exception_handling(self, test_suite_details, e):
        test_suite_details.result_log.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*******exception*******' + str(e))

    def try_else_handling(self, test_suite_details):
        test_suite_details.result_log.write(
            'All tests in test suite \'' + test_suite_details.test_suite_name + '\'' +
            ' completed without exception.\n')

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
        test_suite_details.result_log.write('Pass\n')

    def finally_handling(self, test_suite_details):
        pass

    def end_method_handling(self, test_suite_details):
        pass

    def connect_VistA(self, test_suite_details):
        '''
        Generic method to connect to VistA. Inteded to be reused by the ATF
        Recorder.
        '''
        from OSEHRAHelper import ConnectToMUMPS
        VistA = ConnectToMUMPS(logfile=test_suite_details.result_dir + '/' + self.testname + '.txt',
                               instance=test_suite_details.instance, namespace=test_suite_details.namespace,
                               location=test_suite_details.remote_conn_details.remote_address,
                               remote_conn_details=test_suite_details.remote_conn_details)


        #TODO: implement special handling for changing namespace here.
        #all special handling should be placed here, and be driven by 
        #parameters, such as namespace
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
