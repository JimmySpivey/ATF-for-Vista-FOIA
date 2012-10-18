'''
Created on Jun 14, 2012

@author: bcaine
'''
import sys
sys.path = ['./FunctionalTest/RAS/lib'] + ['./dataFiles'] + ['./lib/vista'] + sys.path
from SCActions import SCActions
import TestHelper

def sc_test001(test_suite_details):
    '''Basic appointment managment options
    Make an Appointment, Check in, Check Out'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA = test_driver.connect_VistA(test_suite_details)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        SC.makeapp(patient='333224444', datetime=time)
        time = SC.schtime(plushour=1)
        now = datetime.datetime.now()
        hour = now.hour + 1
        SC.signon()
        SC.checkin(vlist=['Three', str(hour), 'CHECKED-IN:'])
        SC.signon()
        SC.checkout(vlist1=['Three', str(hour), 'Checked In'], vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91')
        SC.signoff()
        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

def sc_test002(test_suite_details):
    '''Basic appointment managment options
    Make an Appointment (Scheduled and Unscheduled),
    record a No-Show, Cancel an appointment and change patients'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA = test_driver.connect_VistA(test_suite_details)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        SC.makeapp(patient='655447777', datetime=time)
        time = SC.schtime(plushour=1)
        SC.signon()
        SC.unschvisit(patient='345678233', patientname='Twelve')
        SC.signon()
        SC.noshow(appnum='3')
        SC.signon()
        SC.canapp(mult='1')
        SC.signon()
        SC.chgpatient(patient1='345678233', patient2='345238901', patientname1='Twelve', patientname2='Ten')
        SC.signoff()
        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

def sc_test003(test_suite_details):
    '''This tests clinic features such as change clinic, change daterange,
     expand the entry, add and edit, and Patient demographics'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA = test_driver.connect_VistA(test_suite_details)
        SC = SCActions(VistA, scheduling='Scheduling')
        SC.signon()
        SC.chgclinic()
        SC.signon()
        SC.chgdaterange()
        SC.signon()
        SC.teaminfo()
        SC.signoff()
        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

def sc_test004(test_suite_details):
    '''This tests clinic features such as expand the entry, add and edit, and Patient demographics'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA = test_driver.connect_VistA(test_suite_details)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime(plushour=1)
        SC.signon()
        SC.makeapp(patient='345238901', datetime=time)
        SC.signon()
        SC.patdem(name='Ten', mult='2')
        SC.signon()
        SC.expandentry(vlist1=['TEN', 'SCHEDULED', '30'], vlist2=['Event', 'Date', 'User', 'TESTMASTER'],
                       vlist3=['NEXT AVAILABLE', 'NO', '0'], vlist4=['1933', 'MALE', 'UNANSWERED'],
                       vlist5=['Combat Veteran:', 'No check out information'], mult='2')
        SC.signon()
        SC.addedit(name='345623902', icd='305.91')
        SC.signoff()
        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

def sc_test005(test_suite_details):
    '''This test checks a patient into a clinic, then discharges him, then deletes his checkout'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA = test_driver.connect_VistA(test_suite_details)
        SC = SCActions(VistA)
        SC.signon()
        SC.enroll(patient='543236666')
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime(plushour=1)
        SC.signon()
        SC.makeapp(patient='543236666', datetime=time)
        SC.signon()
        SC.discharge(patient='543236666', appnum='3')
        SC.signon()
        SC.checkout(vlist1=['One', 'No Action'], vlist2=['305.91', 'RESULTING'], icd='305.91', mult='3')
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        SC.deletecheckout(appnum='3')
        SC.signoff()
        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

def sc_test006(test_suite_details):
    '''This test will exercise the wait list functionality'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA = test_driver.connect_VistA(test_suite_details)
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        SC.waitlistentry(patient='323554545')
        SC.waitlistdisposition(patient='323554545')
        SC.signoff()
        test_driver.post_test_run(test_suite_details)
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

def startmon(test_suite_details):
    '''Starts Coverage Monitor'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        VistA1 = test_driver.connect_VistA(test_suite_details)
        VistA1.startCoverage(routines=['SC*', 'SD*'])
        test_driver.post_test_run(test_suite_details)
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)

def stopmon (test_suite_details):
    ''' STOP MONITOR'''
    testname = sys._getframe().f_code.co_name
    test_driver = TestHelper.TestDriver(testname)

    test_driver.pre_test_run(test_suite_details)
    try:
        # Connect to VistA
        VistA1 = test_driver.connect_VistA(test_suite_details)
        VistA1.stopCoverage(path=(test_suite_details.result_dir + '/' + 'Scheduling_coverage.txt'))
        test_driver.post_test_run(test_suite_details)
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')
    except TestHelper.TestError, e:
        test_driver.exception_handling(test_suite_details, e)
    else:
        test_driver.try_else_handling(test_suite_details)
    finally:
        test_driver.finally_handling(test_suite_details)
    test_driver.end_method_handling(test_suite_details)


'''
def connect_VistA(testname, result_dir):
    # Connect to VistA
    from OSEHRAHelper import ConnectToMUMPS, PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + testname + '.txt', instance='', namespace='')
    if VistA.type == 'cache':
        try:
            VistA.ZN('VISTA')
        except IndexError, no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA
'''
