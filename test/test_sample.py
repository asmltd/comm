'''
To run test cases on BC/CU 
'''
import re
from comm import get_logger_instance
from comm.utils.ssh_api import RemoteExecution
from comm.definitions import CU_IP, CU_USER, CU_PASSWD

log = get_logger_instance(__name__)
remote_execution = RemoteExecution()

class TestBC(object):
    '''
    Collection of CU test Cases
    '''
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
                if re.search(test["expected_result"], result['res'][0]):
                    log.debug("Expected result: {} is matched with actual result: {}"\
                        .format(test["expected_result"], result['res'][0]))
                    log.info("TestCase Passed")
                else:
                    log.error("Expected result: {} is NOT matched in actual result: {}"\
                        .format(test["expected_result"], result['res'][0]))
                    assert False
            else:
                log.error("Received unexpected output: {}".format(str(result)))
                assert False
