'''
To run test cases on BC/CU 
'''
import os
import re
import time
import datetime
import pytest
from comm import get_logger_instance
from comm.utils.ssh_api import RemoteExecution
from comm.definitions import CU_IP, CU_USER, CU_PASSWD, SCRIPT_FOLDER_PATH

log = get_logger_instance(__name__)
remote_execution = RemoteExecution()

class TestBC(object):
    '''
    Collection of CU test Cases
    '''
    def setup_class(self):
        '''
        Prerequisite execution to make the device ready for testcase execution
        command: executed the given command in the CU device
        num_greater: The value to be compared as greater than with result of above command
        return_code: The exit status to be matched after the above command execution
        '''
        flag = True
        test_commands = [{"command":"cat /proc/uptime | cut -d'.' -f1",
                          "num_greater": 600},
                         {"cmd":"ls /conf_files/isActive &>/dev/null; echo $?",
                          "return_code": 0}
                        ]
        files_to_be_copied = ["spv.py"]
        for test in test_commands:
            result = remote_execution.remote_command_exec_passwd(
                host_ip=CU_IP,
                cmd=test["command"],
                user_name=CU_USER,
                pswd=CU_PASSWD)
            if result.get('res'):
                if test.get("num_greater") and test["num_greater"] > int(result['res'][0]):
                    flag = False
                if test.get("return_code") and test["return_code"] != int(result['res'][0]):
                    flag = False
        pytest.skip("Noticed failure in Prerequisite commands execution") if not flag
        log.debug("Prerequite commands execution passed. Copying the files to CU unit")
        for fname in files_to_be_copied:
            if remote_execution.copy_local_file_remote(
                    host_ip=CU_IP,
                    file_name=os.path.join(ROOT_DIR, SCRIPT_FOLDER_PATH, fname),
                    remote_file_name="/root/{}".format(fname),
                    user_name=CU_USER,
                    pswd=CU_PASSWD):
                log.debug("Copied the file {} successfully to {}"\
                        .format(fname, CU_IP))

    def test_sample_case(self, jsontestdata):
        '''
        Test Case to run Commands on CU
        '''
        test_commands = jsontestdata.get("test_cmds")
        for test in test_commands:
            result = remote_execution.remote_command_exec_passwd(
                host_ip=CU_IP,
                cmd=test["command"],
                user_name=CU_USER,
                pswd=CU_PASSWD)
            if result.get('res'):
                if re.search(test["match_result"], result['res'][0]):
                    log.debug("Expected result: {} is matched with actual result: {}"\
                        .format(test["match_result"], result['res'][0]))
                    log.info("TestCase Passed")
                else:
                    log.error("Expected result: {} is NOT matched in actual result: {}"\
                        .format(test["match_result"], result['res'][0]))
                    assert False
            else:
                log.error("Received unexpected output: {}".format(str(result)))
                assert False

    def test_change_device_timezone(self, jsontestdata):
        '''
        Test Case to change device time zone and validate the same
        '''
        flag = True
        test_commands = jsontestdata.get("test_cmds")
        case_descr = jsontestdata.get("description")
        for test in test_commands:
            result = remote_execution.remote_command_exec_passwd(
                host_ip=CU_IP,
                cmd=test["command"],
                user_name=CU_USER,
                pswd=CU_PASSWD)
            if result.get('res'):
                if test.get("match_result") and re.search(test["match_result"], result['res'][0]):
                    flag = False
                    log.error("Unexpected result. Actual content {}, but expected content is {}"\
                        .format(result['res'][0], test["match_result"]))
                else:
                    log.debug("Actual content {} is matched with expected content {}"\
                        .format(result['res'][0], test["match_result"]))
                
                if test.get("return_code") and test["return_code"] != int(result['res'][0]):
                    flag = False
                    log.error("Unexpected result. Actual return code {}, but expected return code is {}"\
                        .format(result['res'][0], test["return_code"]))
                else:
                    log.debug("Actual content {} is matched with expected content {}"\
                        .format(result['res'][0], test["match_result"]))
            else:
                log.error("Received unexpected output: {}".format(str(result)))
                flag = False
        if flag:
            log.info("case: {} - Passed".format(case_descr))
        else:
            log.error("case: {} - Failed".format(case_descr))
            assert False

    def test_device_reboot(self, jsontestdata):
        '''
        Test Case to validate device reboot
        '''
        flag = True
        test_commands = jsontestdata.get("test_cmds")
        case_descr = jsontestdata.get("description")
        for test in test_commands:
            result = remote_execution.remote_command_exec_passwd(
                host_ip=CU_IP,
                cmd=test["command"],
                user_name=CU_USER,
                pswd=CU_PASSWD)
            if result.get('res'):
                if test.get("num_greater") and test["num_greater"] > int(result['res'][0]):
                    flag = False
                    log.error("Unexpected result. Actual number {}, but expected number is {}"\
                        .format(result['res'][0], test["num_greater"]))
                else:
                    log.debug("Actual number {} is greater than expected number {}"\
                        .format(result['res'][0], test["num_greater"]))

                if test.get("exception") and re.search(test["exception"], "reboot", re.IGNORECASE):
                    start_time = int(datetime.datetime.now().strftime('%s'))
                    while True:
                        if remote_execution.validate_ssh(host_ip=CU_IP):
                            break
                        time.sleep(10)
                        current_time = int(datetime.datetime.now().strftime('%s'))
                        elapsed_time = current_time - start_time
                        if elapsed_time >= 1800: #Waits for 30 Mins
                            log.error("Waited too long for device reachability check")
                            assert False
                        else:
                            log.debug("Still waiting for device {} online, It's been {} sec"\
                                    .format(CU_IP, elapsed_time))
            else:
                log.error("Received unexpected output: {}".format(str(result)))
                flag = False
        if flag:
            log.info("case: {} - Passed".format(case_descr))
        else:
            log.error("case: {} - Failed".format(case_descr))
            assert False
