'''
Module to perform SSH operations
'''
import re
import socket
import paramiko

from comm import get_logger_instance

logger = get_logger_instance(__name__)

class RemoteExecution:
    '''
    SSH Methods definition
    '''
    def __init__(self):
        '''
        Initialized response variable
        '''
        self.output = dict()

    def validate_ssh(self, host_ip, port=22):
        '''
        Validation of given host reachability
        '''
        if host_ip:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host_ip, port))
            if result == 0:
                logger.debug("Port {} is open for instance {}".format(port, host_ip))
                return True
            else:
                logger.info("Unable to SSH to the host {} with {} port".format(host_ip, port))
                return False
        else:
            logger.warn("Host ip is empty")
            return False

    def remote_command_exec_passwd(self, host_ip, cmd,
                                  user_name='root',
                                  pswd='root', cust_port=22):
        '''
        Command execution by sshing to the given machine using password
        '''
        self.output['res'] = []
        self.output['err'] = []
        if cmd and host_ip:
            if self.validate_ssh(host_ip):
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(
                        paramiko.AutoAddPolicy())
                    client.connect(hostname=host_ip, port=int(cust_port),
                                   username=user_name, password=pswd)
                    stdin, stdout, stderr = client.exec_command(cmd)
                    err = stderr.readlines()
                    out = stdout.readlines()
                    self.output['res'] = out
                    self.output['err'] = err
                    logger.info(self.output['res'])
                    return self.output
                except Exception as e:
                    logger.warn("Error: %s" % e)
                    logger.info(
                        "Unable to ssh to the host ip %s with user: %s and password: %s ",
                        host_ip, user_name, pswd)
            else:
                logger.warn("Host is not reachable")
        else:
            logger.warn("Host IP or Command to be executed is empty")

    def remote_command_exec_pem(self, host_ip,
                            cmd, user_name='root',
                            pem_file='secret.pem', cust_port=22):
        '''
        Command execution by sshing to the given machine using pem file
        '''
        self.output['res'] = []
        self.output['res'] = []
        self.output['err'] = []
        if cmd and host_ip:
            if self.validate_ssh(host_ip, cust_port):
                try:
                    key = paramiko.RSAKey.from_private_key_file(pem_file)
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(
                        paramiko.AutoAddPolicy())
                    client.connect(hostname=host_ip, port=int(cust_port),
                                   username=user_name, pkey=key)
                    stdin, stdout, stderr = client.exec_command(cmd)
                    err = stderr.readlines()
                    out = stdout.readlines()
                    self.output['res'] = out
                    self.output['err'] = err
                    return self.output
                except Exception as e:
                    logger.warn("Error: %s" % e)
                    logger.info(
                        "Unable to ssh to the host ip %s with user: %s and pem key: %s",
                        host_ip, user_name, pem_file)
            logger.warn("Host is not reachable")
            return False
        logger.warn("Host IP or Command to be executed is empty")
        return False

