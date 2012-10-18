'''
Created on Jun 14, 2012

@author: bcaine
This is the main Scheduling script that calls the underlying
scheduling functional tests located in SC_Suite001
'''
import os
import sys
sys.path = ['./RAS/lib'] + ['./dataFiles'] + ['../lib/vista'] + sys.path
import SC_Suite001
import TestHelper

def main():
    test_suite_name = os.path.basename(__file__).split('.')[0]
    test_suite_driver = TestHelper.TestSuiteDriver()
    test_suite_details = test_suite_driver.generate_test_suite_details(test_suite_name)

    try:
        test_suite_driver.pre_test_suite_run(test_suite_details)

        #Begin Tests
        SC_Suite001.startmon(test_suite_details)
        SC_Suite001.sc_test001(test_suite_details)
        SC_Suite001.sc_test002(test_suite_details)
        SC_Suite001.sc_test003(test_suite_details)
        SC_Suite001.sc_test004(test_suite_details)
        SC_Suite001.sc_test005(test_suite_details)
        SC_Suite001.sc_test006(test_suite_details)
        SC_Suite001.stopmon(test_suite_details)
        #End Tests

        test_suite_driver.post_test_suite_run(test_suite_details)
    except Exception, e:
        test_suite_driver.exception_handling(test_suite_details, e)
    else:
        test_suite_driver.try_else_handling(test_suite_details)
    finally:
        test_suite_driver.finally_handling(test_suite_details)

    test_suite_driver.end_method_handling(test_suite_details)

if __name__ == '__main__':
  main()
