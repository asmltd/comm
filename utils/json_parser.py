"""
Created on 01-Jan-2020
@author: Madhu
"""
import ast
import json
import os
import numbers

from comm import get_logger_instance
from comm.utils.common_utils import FileUtils

logger = get_logger_instance(__name__)


def load_json_data_from_file(file_name):
    """
    :param file_name: File name to be read
    :return:
    """
    try:
        with open(file_name) as data_file:
            if data_file:
                data = json.load(data_file)
                return data
            else:
                logger.error('No file found at location:{%s}', file_name)
    except (IOError, ValueError) as error:
        logger.exception(error)
    return None


def get_test_data_for(module_name, method_name):
    '''
    Read Data as per the custom input file format
    '''
    logger.debug('<Test data Set-up> For Module:[%s],Method:[%s]', module_name,
                 method_name)
    list_of_test_data = list()
    count = 0
    negative_count = 0
    if module_name:
        file_path = FileUtils.get_test_data_file_name(module_name)
        logger.debug('Test data File location:%s', file_path)
        loaded_data = load_json_data_from_file(os.path.join(file_path))
        if loaded_data:

            for module, module_child_nodes in loaded_data.iteritems():
                logger.debug(module_name.split('.')[-1])

                if module == module_name.split('.')[-1]:
                    logger.debug(
                        'Validate module/file_name:[{}] with root-node key:[{}] --> Passed'.
                        format(module_name, module))

                    if method_name in module_child_nodes.keys():
                        logger.debug('method in module {} in {}'.format(
                            method_name, module_child_nodes.keys()))

                        try:
                            module_child_nodes = ast.literal_eval(
                                json.dumps(module_child_nodes))
                        except Exception:
                            pass

                        if 'test_data_set' in module_child_nodes.get(
                                method_name).keys():
                            for key, test_data in module_child_nodes.get(
                                    method_name).get(
                                        'test_data_set').iteritems():
                                if (key == 'positive'
                                        or key == 'negative') and isinstance(
                                            test_data, list):
                                    for data_entry in test_data:
                                        try:
                                            data_entry = ast.literal_eval(
                                                json.dumps(data_entry))
                                        except:
                                            pass

                                        count = count + 1
                                        if key == 'negative':
                                            negative_count = negative_count + 1
                                            data_entry[
                                                'negative_scenario'] = 'True'

                                        list_of_test_data.append(data_entry)
                                else:
                                    logger.debug(
                                        'Ignoring unknown key:[%s] in \'test_data-set \' node...',
                                        key)
                        else:
                            logger.debug('No data found under node:%s',
                                         'test_data_set')
                        logger.debug('Found entry for test_method:%s ',
                                     method_name)
                    else:
                        logger.exception(
                            'Method node:[%s] not found in input file:[%s]',
                            method_name, file_path)
                else:
                    logger.exception(
                        'JSON validation failed: Module Name:[{}] is not'
                        ' the root element input file:[{}]'.format(
                            module_name, module))
        else:
            logger.exception('No data found for input [Module_name=%s]',
                             module_name)
    else:
        logger.exception('Module_name:[%s] Method_name:[%s] are mandatory!!',
                         module_name, method_name)

    logger.debug('From file,No of executions for test:[%s] = %s', module_name,
                 len(list_of_test_data))
    logger.debug('Negative count:%s', negative_count)
    logger.debug('Size of Resolved test data set : {}'.format(count))
    if list_of_test_data:
        # logger.info('No of executions [%s] ', len(list_of_test_data))
        test_data_entry_size = 1
        for test_data_entry in list_of_test_data:
            logger.debug(
                ' ========== Test data for method : [%s] at index : [%s] ==============',
                method_name, str(test_data_entry_size))
            logger.debug(test_data_entry)
    else:
        logger.info('Skipping execution for test: [%s]..', method_name)
    logger.debug('========= End of Data generation =========')

    return list_of_test_data
