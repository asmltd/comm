# import time
from ctypes import *
import os
import sys
# from sys import platform

SHARED_LIBRARY_PATH = "/usr/lib/webgui.so"
TEMP_DATA_FILE="./temp_data_spv"

class MO_TYPE():
    STRING = "6"
    INT = "7"
    UINT = "9"
    BOOLEAN = "18"
    DATETIME = "11"

param = []
# param = [
        # "Device.FAP.X_0005B9_BackupRestore.BackupState", "SUCCESS", MO_TYPE.STRING,
        # "Device.FAP.X_0005B9_BackupRestore.BackupState", "FAILED", MO_TYPE.STRING,
        # "Device.FAP.X_0005B9_BackupRestore.BackupFailReason", "Manual SPV triggered to recover from in-progress state", MO_TYPE.STRING,
        # "Device.FAP.X_0005B9_BackupRestore.BackupFileName", "DEVICEGUICONFIG", MO_TYPE.STRING

        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.1.FileCompressionType", "tar.gz", MO_TYPE.STRING,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.1.FileCompressionType", "tgz", MO_TYPE.STRING,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.1.FileCompressionType", "zip", MO_TYPE.STRING,

        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.7.FileCompressionType", "tar.gz", MO_TYPE.STRING
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.7.FileCompressionType", "tgz", MO_TYPE.STRING
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.7.FileCompressionType", "zip", MO_TYPE.STRING
        
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.1.FileCompressionType", "zip", MO_TYPE.STRING
        
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.1.Enable", "true", MO_TYPE.BOOLEAN
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.2.Enable", "false", MO_TYPE.BOOLEAN,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.3.Enable", "false", MO_TYPE.BOOLEAN,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.4.Enable", "false", MO_TYPE.BOOLEAN,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.5.Enable", "false", MO_TYPE.BOOLEAN,
        
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.ServerURL", "ftp://10.208.208.151", MO_TYPE.STRING
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.Username", "airvana", MO_TYPE.STRING
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.Password", "airvana", MO_TYPE.STRING

        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.1.TransferNow", "1", MO_TYPE.UINT
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.4.TransferNow", "1", MO_TYPE.UINT
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.6.TransferNow", "1", MO_TYPE.UINT
        # "Device.FAP.X_0005B9_FileTransfersEnh.2.FileDetails.1.TransferNow", "1", MO_TYPE.UINT
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.8.TransferNow", "1", MO_TYPE.UINT
		
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.2.TransferNow", "1", MO_TYPE.UINT
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.3.TransferNow", "1", MO_TYPE.UINT
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.5.TransferNow", "1", MO_TYPE.UINT
		
		# "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.2.FileName", "PERFORMANCEPERPLMNOM", MO_TYPE.STRING,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.5.FileName", "PERPLMNOM", MO_TYPE.STRING
		
		# "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.2.TransferWindowInterval", "3600", MO_TYPE.UINT,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.3.TransferWindowInterval", "3600", MO_TYPE.UINT,
        # "Device.FAP.X_0005B9_FileTransfersEnh.1.FileDetails.5.TransferWindowInterval", "3600", MO_TYPE.UINT
		
        # "Device.FAP.X_0005B9_RUWhiteList", "0005B951B7B8,0005B9519768,0005B951988C", MO_TYPE.STRING
        # ]

def call_moSet(param_list):
    arr = (c_char_p * len(param_list))()
    arr[:] = param_list
    return webapi.moSet(arr, len(param_list))

def call_moGet(param_list):
    arr = (c_char_p * len(param_list))()
    arr[:] = param_list
    return webapi.moGet(arr, len(param_list))

def free_mo_mem(count):
    return webapi.freeMOValueMemory(count)


def convertDatetimeToString(datetime):
    if not datetime:
        uptime = "NA"
        return uptime
        
    hh = int(datetime)/3600
    mn = (int(datetime)/60)%60
    sec = int(datetime)%60
    
    if hh/10 == 0:
        hour = "0%d Hrs" %hh
    else:
        hour = "%d Hrs" %hh
        
    if mn/10 == 0:
        minute = " 0%d Mins" %mn
    else:
        minute = " %d Mins" %mn
    
    if sec/10 == 0:
        second = " 0%d Secs" %sec
    else:
        second = " %d Secs" %sec
        
    uptime = hour+minute+second
    
    return uptime
    
def perform_spv(param):
    ret = call_moSet(param)

    if ret == 0:
        print "SPV Successful"
    else:
        print "SPV Failed with ret = " + str(ret)

    return ret

if __name__ == '__main__':
    webapi = CDLL(SHARED_LIBRARY_PATH)
    ret = webapi.webgui_initialize()
    if ret != 0:
        sys.exit()

    if len(sys.argv) == 1 :
        print "Error!!! Invalid argument..."
        print "Format: " + sys.argv[0] + " <MO Name> <MO value> <MO type>"
        sys.exit (1)
    
    if sys.argv[1] == "clean" :
        os.system("rm -f {}".format(TEMP_DATA_FILE))

    elif sys.argv[1] == "commit" :
        f = open (TEMP_DATA_FILE, "r")
        param_list = f.read().split(' ')
        print param_list
        f.close()

        ret = perform_spv(param_list)
        os.system("rm -f {}".format(TEMP_DATA_FILE))
        
        sys.exit (ret)

    else :
        empty_file = 0
        if os.path.exists(TEMP_DATA_FILE) :
            if os.stat(TEMP_DATA_FILE).st_size == 0 :
                empty_file = 1
        else :
            empty_file = 1

        f = open (TEMP_DATA_FILE, "a")
        if not empty_file :
            f.write(" ")
        f.write( "{} {} {}".format(sys.argv[1], sys.argv[2], sys.argv[3]))
        f.close()

        print "Data stored for following parameters:"
        os.system("cat {} | sed 's/Device/\\nDevice/g'".format(TEMP_DATA_FILE))
        print "\n\n#########################################"
        print "PERFORM COMMIT TO TRIGGER SPV"
        print "#########################################"
