###################################################################
# (c) Copyright 2008 Wi-Fi Alliance.  All Rights Reserved
#
# Authors:
# Chandra Sekhar Duba;       Email: cduba@wi-fi.org
####################################################################
# LICENSE
####################################################################
#
#
# License is granted only to Wi-Fi Alliance members and is for use solely
# in testing Wi-Fi products. This license is not transferable or sublicensable,
# and it does not extend to and may not be used with non Wi-Fi applications.
#
# Commercial derivative works or applications that use the Wi-Fi
# scripts generated by this software are NOT AUTHORIZED without
# specific prior written permission from Wi-Fi Alliance
#
# Non-commercial derivative works for your own internal use are
# authorized and are limited by the same restrictions.
#
# Neither the name of the author nor "Wi-Fi Alliance"
# may be used to endorse or promote products that are derived
# from or that use this software without specific prior written
# permission from the author or Wi-Fi Alliance
#
# THIS SOFTWARE IS PROVIDED BY WI-FI ALLIANCE "AS IS" AND ANY
# EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY, NON-INFRINGEMENT AND FITNESS
# FOR A  PARTICULAR PURPOSE, ARE DISCLAIMED. IN NO EVENT SHALL WI-FI
# ALLIANCE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# THE COST OF PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###################################################################
# Change History
#       Date        Version          Comment 
#            
#        
###################################################################
#

import socket
import os, sys
from ftplib import FTP
from tms.TmsHeaders import *
import tms.TmsCommon as TmsCommon
import pysftp
import warnings
import _cffi_backend
from stat import S_ISDIR, S_ISREG
import subprocess


class TmsFtpClient:
    def __init__(self,_logobj):
        #logger object
        self.logobj = _logobj
        self.logobj.LogMsg("TmsFtpClient - Object Created",WFA_INFO)
        #Read the config file and configure the class propoerties
        #the FTP  server IP address or domain name
        #the FTP server path

        #Read the config file and configure the username and password

    def TestServerLink(self):
        self.logobj.LogMsg("Entry TestServerLink function",WFA_DEBUG)
        print("The system command", "ping -n 1 " + TmsCommon.FtpServerIp)
        tmp_pingRes = os.system("ping -n 1 " + TmsCommon.FtpServerIp)
        if tmp_pingRes == 0:
            print("Ping responses ", tmp_pingRes)
            self.logobj.LogMsg("Exit Test Bulk Storage Server Link function",WFA_DEBUG)
            return True
        else:
            self.logobj.LogMsg("Exit Test Bulk Storage Server Link function",WFA_DEBUG)
            return False

    def PostZipLogFile(self,_inputFile,_inputFilePath):
        self.logobj.LogMsg("Entry PostZipLogFile function",WFA_DEBUG)   
        InputZipfileName=_inputFile
        InputZipfilePath=_inputFilePath

        #use the username and password as part of the ftp connection
        print("The ftp credentials",TmsCommon.FtpServerIpAddress,TmsCommon.FtpServerUN,TmsCommon.FtpServerPS)
        try:
            warnings.filterwarnings("ignore")
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            sftp_obj = pysftp.Connection(TmsCommon.FtpServerIpAddress, username=TmsCommon.FtpServerUN, password=TmsCommon.FtpServerPS, cnopts=cnopts)
        except Exception as e:  #you can specify type of Exception also
            # print(str(e))
            print("Error in connecting to ftp server")
            sys.exit(1)
            
        tmp1=InputZipfileName.split("&&")
        tmp1_length=len(tmp1)
        ########create the path / folders on the ftp
        ########put the zip file to the server
        ret=sftp_obj.pwd
        ret=sftp_obj.listdir()
        print("Current working dir",ret)
        if tmp1_length > 4:
            ZipfileName=tmp1[4]
            TestCase=tmp1[3]
            TestBeddeviceID=tmp1[2]
            DutDeviceID=tmp1[1]
            EventID=tmp1[0]
            tmp=EventID+"/"+DutDeviceID+"/"+TestBeddeviceID+"/"+TestCase
            print("The folders to be created on ftp",tmp)
            try:
                sftp_obj.mkdir(EventID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(EventID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(DutDeviceID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(DutDeviceID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(TestBeddeviceID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(TestBeddeviceID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(TestCase)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(TestCase)
            except:
                print("could not change directory")
                sys.exit(1)

            ret=sftp_obj.pwd
            print("Current working dir",ret)
            zip_file = InputZipfilePath + ZipfileName
            print("Upload file A: ",ZipfileName)
            ret=sftp_obj.put(zip_file, ZipfileName)
            print("the return after file upload",ret)
        else:
            ZipfileName=tmp1[3]
            TestCase=tmp1[2]
            DutDeviceID=tmp1[1]
            EventID=tmp1[0]
            tmp=EventID+"/"+DutDeviceID+"/"+TestCase
            print("The folders to be created on ftp",tmp)
            try:
                sftp_obj.mkdir(EventID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(EventID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(DutDeviceID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(DutDeviceID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(TestCase)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(TestCase)
            except:
                print("could not change directory")
                sys.exit(1)

            ret=sftp_obj.pwd
            print("Current working dir",ret)
            zip_file = InputZipfilePath + ZipfileName
            print("Upload file B: ",ZipfileName)
            ret=sftp_obj.put(zip_file, ZipfileName)
            print("the return after file upload",ret)
        
        #check the status of the response
        sftp_obj.close()            

        #return
        self.logobj.LogMsg("Exit PostZipLogFile function",WFA_DEBUG)		

    def PostZipLogFile_from_UCC(self,_inputFile,_localstoragepath, _target_filename):
        self.logobj.LogMsg("Entry PostZipLogFile function",WFA_DEBUG)   
        InputZipfileName=_inputFile
        InputTargetFileName= _target_filename
        InputLocalStoragePath = _localstoragepath

        #use the username and password as part of the ftp connection
        print("The ftp credentials",TmsCommon.FtpServerIpAddress,TmsCommon.FtpServerUN,TmsCommon.FtpServerPS)
        try:
            warnings.filterwarnings("ignore")
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            sftp_obj = pysftp.Connection(TmsCommon.FtpServerIpAddress, username=TmsCommon.FtpServerUN, password=TmsCommon.FtpServerPS, cnopts=cnopts)
        except Exception as e:  #you can specify type of Exception also
            print(str(e))        
            print("Error in connecting to ftp server")
            sys.exit(1)
            
        tmp1=InputZipfileName.split("&&")
        tmp1_length=len(tmp1)
        ########create the path / folders on the ftp
        ########put the zip file to the server
        ret=sftp_obj.pwd
        ret=sftp_obj.listdir()
        print("Current working dir",ret)
        if tmp1_length > 4:
            ZipfileName=tmp1[4]
            TestCase=tmp1[3]
            TestBeddeviceID=tmp1[2]
            DutDeviceID=tmp1[1]
            EventID=tmp1[0]
            tmp=EventID+"/"+DutDeviceID+"/"+TestBeddeviceID+"/"+TestCase
            print("The folders to be created on ftp",tmp)
            try:
                sftp_obj.mkdir(EventID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(EventID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(DutDeviceID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(DutDeviceID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(TestBeddeviceID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(TestBeddeviceID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(TestCase)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(TestCase)
            except:
                print("could not change directory")
                sys.exit(1)

            ret=sftp_obj.pwd
            print("Current working dir",ret)            

            if os.path.isfile('.\\localstorage\\' + InputTargetFileName + '.zip'):
                zip_file= '.\\localstorage\\' + InputTargetFileName + '.zip'
                print("Upload file C: ",ZipfileName)
                ret=sftp_obj.put(zip_file, ZipfileName)
            print("the return after file upload",ret)
        else:
            ZipfileName=tmp1[3]
            TestCase=tmp1[2]
            DutDeviceID=tmp1[1]
            EventID=tmp1[0]
            tmp=EventID+"/"+DutDeviceID+"/"+TestCase
            print("The folders to be created on ftp",tmp)
            try:
                sftp_obj.mkdir(EventID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(EventID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(DutDeviceID)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(DutDeviceID)
            except:
                print("could not change directory")
                sys.exit(1)
            try:
                sftp_obj.mkdir(TestCase)
            except:
                print("folder exist")
            try:
                sftp_obj.cwd(TestCase)
            except:
                print("could not change directory")
                sys.exit(1)

            ret=sftp_obj.pwd
            print("Current working dir",ret)
            zip_file = InputZipfilePath + ZipfileName
            print("Upload file D: ",ZipfileName)
            ret=sftp_obj.put(zip_file, ZipfileName)
            print("the return after file upload",ret)
        
        #check the status of the response
        sftp_obj.close()            

        #return
        self.logobj.LogMsg("Exit PostZipLogFile function",WFA_DEBUG)		

    def get_r_portable(self, sftp, remotedir, localdir, preserve_mtime=False):
        for entry in sftp.listdir_attr(remotedir):
            remotepath = remotedir + "/" + entry.filename
            localpath = os.path.join(localdir, entry.filename)
            mode = entry.st_mode
            if S_ISDIR(mode):
                try:
                    os.mkdir(localpath)
                except OSError:     
                    pass
                self.get_r_portable(sftp, remotepath, localpath, preserve_mtime)
            elif S_ISREG(mode):
                sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)

    def GetZipLogFile_to_UCC(self, _remote_path, _local_dir):
        #use the username and password as part of the ftp connection
        print("The ftp credentials",TmsCommon.FtpServerIpAddress,TmsCommon.FtpServerUN,TmsCommon.FtpServerPS)
        
        try:
            warnings.filterwarnings("ignore")
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            sftp_obj = pysftp.Connection(TmsCommon.FtpServerIpAddress, username=TmsCommon.FtpServerUN, password=TmsCommon.FtpServerPS, cnopts=cnopts)
        except Exception as e:  #you can specify type of Exception also
            print(str(e))        
            print("Error in connecting to ftp server")
            sys.exit(1)

        CurrentDir=os.getcwd() 
        localdir = CurrentDir + _local_dir + "\\" + TmsCommon.TmsEventId
        remotedir  = _remote_path

        # We create the local_dir folder in case it's not there
        cmd="mkdir download_backup" + "\\" + TmsCommon.TmsEventId
        print("the command", cmd)
        
        try:
            cmd_output=subprocess.check_output(cmd, shell=True)
        except:
            print("Error in running the command ", cmd)
            return 0
        
        ret=sftp_obj.pwd
        ret=sftp_obj.listdir()
        print("Current working dir",ret)

        # Please refer to the known issue of pysftp module and the proposed solution at https://stackoverflow.com/questions/50118919/python-pysftp-get-r-from-linux-works-fine-on-linux-but-not-on-windows
        # And, it seems that the local path should be given by the complete absolute path...
        self.get_r_portable(sftp_obj, remotedir, localdir, preserve_mtime=False) 

        sftp_obj.close() 