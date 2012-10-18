'''
Created on Sept 28, 2012
@author: jspivey
Simple demo which will connect via ssh to vista.vainnovation.us
'''
import os
import sys
#apparently these are not needed... at least not on windows. Will need to retest this on linux
#sys.path = ['./FunctionalTest/RAS/lib'] + ['./lib/vista'] + sys.path
#sys.path = ['./'] + ['../lib/vista'] + sys.path

import RC_Suite001
import TestHelper

def main():
    test_suite_name = os.path.basename(__file__).split('.')[0]
    test_suite_driver = TestHelper.TestSuiteDriver()
    test_suite_details = test_suite_driver.generate_test_suite_details(test_suite_name)

    try:
        test_suite_driver.pre_test_suite_run(test_suite_details)

        #Begin Tests
        RC_Suite001.dive_into_menus(test_suite_details)
        RC_Suite001.demo_screen_man(test_suite_details)
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
