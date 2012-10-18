'''
Created on Mar 1, 2012
@author: pbradley
This is the main test script that calls the underlying PL functional tests
located in PL_Suite001.
'''
import os
import sys
sys.path = ['./RAS/lib'] + ['./dataFiles'] + ['../lib/vista'] + sys.path
import PL_Suite001
import TestHelper

def main():
    test_suite_name = os.path.basename(__file__).split('.')[0]
    test_suite_driver = TestHelper.TestSuiteDriver()
    test_suite_details = test_suite_driver.generate_test_suite_details(test_suite_name)

    try:
        test_suite_driver.pre_test_suite_run(test_suite_details)

        #Begin Tests
        PL_Suite001.startmon(test_suite_details)
        PL_Suite001.pl_test001(test_suite_details)
        PL_Suite001.pl_test002(test_suite_details)
        PL_Suite001.pl_test003(test_suite_details)
        PL_Suite001.pl_test010(test_suite_details)
        PL_Suite001.pl_test011(test_suite_details)
        PL_Suite001.pl_test004(test_suite_details)
        PL_Suite001.pl_test005(test_suite_details)
        PL_Suite001.pl_test006(test_suite_details)
        PL_Suite001.pl_test007(test_suite_details)
        PL_Suite001.pl_test008(test_suite_details)
        PL_Suite001.pl_test009(test_suite_details)
        PL_Suite001.pl_test012(test_suite_details)
        PL_Suite001.pl_test013(test_suite_details)
        PL_Suite001.stopmon(test_suite_details)
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
