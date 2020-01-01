import sys
import pytest
from comm import get_logger_instance
from comm.utils import json_parser

sys.stdout = sys.stderr
logger = get_logger_instance(__name__)

def pytest_generate_tests(metafunc):
    """
    Main Pytest hook called to set up test data for test execution
    This method is called before each pytest method is invoked
    """
    logger.debug("\nExecution Started\n")
    logger.debug('#####'*10)
    module_name = metafunc.module.__name__
    if 'jsontestdata' in metafunc.fixturenames:
        data_set_for_execution = json_parser.get_test_data_for(module_name, metafunc.function.__name__)
        if not data_set_for_execution:
            logger.error("No test data for :Mod[%s]  Method[%s]", module_name, metafunc.function.__name__)
        metafunc.parametrize('json_data_parse', data_set_for_execution, 
                ids=_generate_param_ids(data_set_for_execution), scope='function')

def _generate_param_ids(data_set_for_execution):
    """
    @param values:
    @return: Unique ID for each data set to be executed
    """
    id_list = list()
    try:
        for param in data_set_for_execution:
            if param.get('_case_id'):
                id_list.append(param.get('_case_id'))
            else:
                id_list.append('')
    except Exception as e:
        logger.error(e.message)
        logger.error('Exception while generate_param_ids.')
    return id_list                

@pytest.yield_fixture(scope='function')
def jsontestdata(request, json_data_parse):
    """
    @param request: This is a pytest module
    @param json_data_parse: This fixture gets the parsed JSON test data from input file and feeds all tests
    """
    print '\n||     #######################  {} ######################   ||'.format(request.node.name)
    print '#####'*20
    yield json_data_parse
    
