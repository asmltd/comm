import os

from comm import get_logger_instance
from comm.definitions import ROOT_DIR, TEST_FOLDER_PATH

logger = get_logger_instance(__name__)

class StringUtils():
    @staticmethod
    def is_not_empty(string_literal):
        if string_literal and not string_literal.isspace():
            return True
        else:
            return False

    @staticmethod
    def get_only_alpha_numeric_values(string_literal):
        import re
        return re.sub(r'\W+', '', string_literal)

    @staticmethod
    def convert_list_to_string(input_list):
        try:
            string_literal = ''.join(str(e) for e in input_list)
            return string_literal
        except:
            logger.error("Error while converting list to string")
            return input_list

class FileUtils():
    @staticmethod
    def get_test_data_file_name(module_name):
        """
        Gets a Python module name and traverses through TEST_Data folder to locate module.json file
        :param module_name:
        :return: .JSON file name
        """
        path_to_file = module_name.split('.')
        if path_to_file:
            if path_to_file[1] in ['tests', 'test']:
                path_to_file.pop(1)
                path_to_file.pop(0)
            path_to_file[-1] += '.json'
        logger.debug('Test Module Name:[%s] Resolved TestData location:%s',
                     module_name, path_to_file)
        path = os.path.join(ROOT_DIR, TEST_FOLDER_PATH, *path_to_file)
        logger.debug(
            'Trying to locate testdata file in sub-folder location: [%s]   Is present [%s]',
            path, os.path.isfile(path))
        if not os.path.isfile(path):
            logger.warn('Test data file not in sub-folder..')
            path = os.path.join(ROOT_DIR, TEST_FOLDER_PATH, path_to_file[-1])
            logger.debug('Test data file is present %s', os.path.isfile(path))
        # logger.info('Test Data:{}'.format(path))
        return path


class TestcaseLogger(object):
    def __init__(self, testcase_desc):
        self.testcase_desc = testcase_desc
        self.step_title = 'Testcase Description'
        self.log_lines = []
        self.failure_log_lines = []
        self.info(testcase_desc)

    def info(self, msg):
        msg = "[ {} ]: {}".format(self.step_title, msg)
        self.log_lines.append(msg)
        logger.info(msg)

    def error(self, msg):
        msg = "[ {} ]: {}".format(self.step_title, msg)
        self.log_lines.append(msg)
        logger.error(msg)

    def success(self, msg):
        msg = "[ {} ]: PASS : {}".format(self.step_title, msg)
        self.log_lines.append(msg)
        logger.info(msg)

    def fail(self, msg):
        msg = "[ {} ]: FAIL: {}".format(self.step_title, msg)
        self.log_lines.append(msg)
        self.failure_log_lines.append(msg)
        logger.error(msg)

    def print_summary(self):
        for line in self.log_lines:
            print line

    def print_failures(self):
        for line in self.failure_log_lines:
            print line

    def set_step_title(self, title):
        self.step_title = title
        self.log_lines.append("")
