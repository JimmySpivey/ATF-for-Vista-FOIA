'''
Created on Sep 28, 2012

@author: jspivey
'''
import sys
sys.path = ['./FunctionalTest/RAS/lib'] + ['./dataFiles'] + ['./lib/vista'] + sys.path

from RCActions import RCActions
import TestHelper

def dive_into_menus(test_suite_details):
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)

    try:
        vista = test_driver.connect_VistA(test_suite_details)
        rc = RCActions(vista, user='01vehu', code='vehu01')
        rc.signon()
        vista.wait('Select Training Menu Option:')
        vista.write('OE')
        vista.wait('Select CPRS Manager Menu Option:')
        vista.write('CL')
        vista.wait('Select Clinician Menu Option:')
        vista.write('RR')
        vista.wait('Select Patient:')
        #vista.write('0089')
        #vista.wait('CHOOSE 1-2:')
        #vista.write('1')
        #vista.wait('Select Item(s):')
        #vista.write('1')
        #vista.wait('Select Health Summary Type:')

        vista.write('^')
        vista.wait(':')
        vista.write('^')
        vista.wait(':')
        vista.write('^')
        vista.wait(':')
        rc.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)



def demo_screen_man(test_suite_details):
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)

    try:
        vista = test_driver.connect_VistA(test_suite_details)
        rc = RCActions(vista, user='1radiologist', code='radiologist1')
        rc.signon()
        vista.wait('Select TERMINAL TYPE NAME:')
        vista.write('')
        vista.wait('Select Clinician Menu Option:')
        vista.write('OE')
        vista.wait('Select Patient: Change View')
        vista.write('FD')
        vista.wait('Select PATIENT NAME:')
        vista.write('0849') #0849
        vista.wait('Select: Next Screen')
        vista.write('Q')
        vista.wait('Select Patient: Change View')
        vista.write('^')
        vista.wait('Select Clinician Menu Option:')
        rc.signoff()

        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

