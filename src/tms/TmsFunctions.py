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

import os, sys
# import commands
import subprocess
from tms.TmsHeaders import *
#from TmsCommon import *
import tms.TmsCommon as TmsCommon
import json
import re
import shutil
import zipfile

class TmsFunctions:
    def __init__(self,_logobj):
        #logger object
        self.logobj = _logobj       
        self.logobj.LogMsg("TmsFunctions - Object Created",WFA_INFO)
        
        
    def CheckStatus(self,_RestclientObj,_LocalStorageObj,_BulkStorageObj):
        global ConfigFile
        self.logobj.LogMsg("Entry CheckStatus function",WFA_DEBUG)
        #Check the connection status with Tms Server
        linkStatus = _RestclientObj.TestServerLink()
        if linkStatus == False:
            print("\n TMS Server Link is DOWN!!!! ")
            self.logobj.LogMsg("Link to TMS Server is not active",WFA_DEBUG)
        else :
            self.logobj.LogMsg("Link to TMS Server is active",WFA_DEBUG)
            print("\n TMS Server Link is UP!!!! ")

        #Check the connection status with Bulk Storage 
        linkStatus = _BulkStorageObj.TestServerLink()           # TED: it would ping the SFTP server IP "54.241.136.209", however it may not support ICMP feature 
        if linkStatus == False:
            self.logobj.LogMsg("Link to Bulk Storage Server is not active",WFA_DEBUG)
            print("\n Bulk Storage Server Link is DOWN!!!! ")
        else :
            self.logobj.LogMsg("Link to Bulk Storage Server is active",WFA_DEBUG)
            print("\n Bulk Storage Link is UP!!!! ")

        #Check the buffered or local storage for queue size
        localStorageStatus=_LocalStorageObj.GetLocalStorageStatus()
        msg="Bulk Storage Offline items %d", localStorageStatus
        self.logobj.LogMsg(msg,WFA_DEBUG)
        print("\n Bulk Storage Offline items:  ",localStorageStatus)

        #Check the config file presence
        CurrentDir=os.getcwd()
        print("current working directory", CurrentDir)
        ConfFile=".\\config\\"+ConfigFile
        print("config file directory %s", ConfFile)
        ret=os.path.isfile(ConfFile) 
        if(ret == False):
            print("\n TMS Config file does not exist!!!")
            self.logobj.LogMsg("TMS Config file does not exist",WFA_DEBUG)
        else:
            print("\n TMS Config file exist!!!")
            self.logobj.LogMsg("TMS Config file exist",WFA_DEBUG)		

        #Check the UCC presence
        UccFile=TmsCommon.UccPath+"\\"+"bin"+"\\"+"wfa_ucc.exe" #  TED: the new WTS executive binary is wts.exe and it's reasonalbe to see the error msg at this step
        print("UCC file directory %s", UccFile)
        ret=os.path.isfile(UccFile) 
        if(ret == False):
            print("\n UCC does not exist!!!")
            self.logobj.LogMsg("UCC does not exist",WFA_DEBUG)
        else:
            print("\n UCC exist!!!")
            self.logobj.LogMsg("UCC exist",WFA_DEBUG)		

        self.logobj.LogMsg("Exit CheckStatus function",WFA_DEBUG)
        return 1

    def PrintConfig(self):
        self.logobj.LogMsg("Entry printConfig function",WFA_DEBUG)
        #print "First Name",param1,"Last Name",param2
        print("TMS Server UN ", TmsCommon.TmsServerUN)
        print("TMS TmsServerPS ", TmsCommon.TmsServerPS)
        print("TMS TmsServerHostName ", TmsCommon.TmsServerHostName)
        print("TMS Server UN ", TmsCommon.TmsServerURL)
        print("TMS FtpServerUN ", TmsCommon.FtpServerUN)
        print("TMS FtpServerPS ", TmsCommon.FtpServerPS)
        print("TMS FtpServerIp ", TmsCommon.FtpServerIp)
        print("TMS UccPath ", TmsCommon.UccPath)
        print("TMS TmsEventId ", TmsCommon.TmsEventId)
        print("TMS DutParticipantName", TmsCommon.DutParticipantName)
        print("TMS TestbedParticipantName", TmsCommon.TestbedParticipantName)
        print("TMS TmsLocalStoragePath", TmsCommon.TmsLocalStoragePath)
        self.logobj.LogMsg("Exit printConfig function",WFA_DEBUG)
        return 1
        
    def TmsPostOffline(self,_RestclientObj,_LocalStorageObj,_order="older"):
        restClient = _RestclientObj
        localStorage = _LocalStorageObj
        self.logobj.LogMsg("Entry TmsPostOffline function",WFA_DEBUG)
        #check the server link before posting to server
        linkStatus = restClient.TestServerLink()
        if linkStatus == False:
            self.logobj.LogMsg("Link to TMS Server is not active",WFA_DEBUG)
            print("Link to TMS Server is not active")
            sys.exit(1)		

        #Pick from the local stored files 
        #fetch the JSON file contents
        self.logobj.LogMsg("try to get JSON file",WFA_DEBUG)
        if _order == "older" :
            JsonInput,JsonFile=localStorage.GetJsonFile()
        else:
            JsonInput,JsonFile=localStorage.GetJsonFile("latest")        
        if JsonInput == 0:
            print("Error in getting JSON file contents")
            sys.exit(1)		
        self.logobj.LogMsg("The Json contents"+JsonInput,WFA_DEBUG)
        #print "The Json contents",JsonInput
        #Post the JSON file
        ret=restClient.PostJsonFile(JsonInput)
        if ret == 0:
            print("Error in posting JSON file contents to server")
            sys.exit(1)
        else: 
            #successful posting so remove the file
            os.system("del " + JsonFile)
            ret=os.path.isfile(JsonFile) 
            if(ret == True):
                print("!!! Could not delete the JSON file which was posted!!!")
                
        #Post the Log Zip file
        #restClinet.PostJsonFile()
        self.logobj.LogMsg("Exit TmsPostOffline function",WFA_DEBUG)
        return 1

        
        
        
    def TmsRunOneTest(self,_RestclientObj,_LocalStorageObj,_ProgName,_testID,_BulkStorageObj):
        restClient = _RestclientObj
        localStorage = _LocalStorageObj
        testCaseId = _testID
        progName = _ProgName
        bulkStorage=_BulkStorageObj
        self.logobj.LogMsg("Entry TmsRunOneTest function",WFA_DEBUG)

        #Get the UCC path
        SigmaTmsConfFile=TmsCommon.UccPath+SigmaTmsConfigFile
        #print " Sigma Tms config file  %s", SigmaTmsConfFile
        msg=" Sigma Tms config file  %s", SigmaTmsConfFile
        self.logobj.LogMsg(msg,WFA_DEBUG)

        ret=os.path.isfile(SigmaTmsConfFile) 
        if(ret == False):
            print("!!! Sigma Tms Config file does not exist, Please Check the Sigma !!!")
            sys.exit(0)

        ########Update the variables
        fo = open(SigmaTmsConfFile,"r+")
        tmp_fc = fo.readlines()
        fo.seek(0)
        for line in tmp_fc:
            #print "The line read", line
            if "TmsEventId=" in line:
                fo.write("TmsEventId"+"="+TmsCommon.TmsEventId+"\n")
            elif "DutParticipantName=" in line:
                fo.write("DutParticipantName"+"="+TmsCommon.DutParticipantName+"\n")
            elif "BulkStorageServer=" in line:
                fo.write("BulkStorageServer"+"="+TmsCommon.FtpServerIp+"\n")
            elif "TestbedParticipantName=" in line:
                fo.write("TestbedParticipantName"+"="+TmsCommon.TestbedParticipantName+"\n")
            else:
                fo.write(line)
        fo.truncate()
        fo.close()        

        ########run UCC with test ID
        #cmd=TmsCommon.UccPath+SigmaExe+" "+progName+" "+testCaseId
        cmd="cd "+TmsCommon.UccPath+"&"+SigmaExe+" "+progName+" "+testCaseId
        print("The command is",cmd)
        cmd_output = ""
        self.logobj.LogMsg(cmd,WFA_DEBUG)        
        try:
            cmd_output=subprocess.check_output(cmd, shell=True)
        except:
            print("Error in running the command ", cmd)
            sys.exit(1)
            

        #print "The command output ",cmd_output
        msg = "The command output %s", cmd_output
        self.logobj.LogMsg(msg,WFA_DEBUG)        

        
        
        #######   find the folder to be zipped
        cmd="dir "+TmsCommon.UccPath+"log /ad /o-d" 
        #print "the command", cmd
        self.logobj.LogMsg(cmd,WFA_DEBUG)        
        try:
            cmd_output=subprocess.check_output(cmd, shell=True)
        except:
            print("Error in running the command ", cmd)
            sys.exit(1)
            
        #print "The command output ",cmd_output
        msg = "The command output %s", cmd_output


        self.logobj.LogMsg(msg,WFA_DEBUG)
        tmp1=cmd_output.split("\n")
        log_file =""
        for tmp2 in tmp1:
            filename = tmp2
            #print "inside for", tmp2,testCaseId
            if filename.find(testCaseId) > 0:
                #print "the file to be fetched", tmp2
                msg="the file to be fetched", tmp2
                self.logobj.LogMsg(msg,WFA_DEBUG)                
                file_tmp=tmp2.split(" ")
                log_file=file_tmp[-1].rstrip()
                #print "The log folder to be posted to TMS Server", log_file 
                msg="The log folder to be posted to TMS Server", log_file 
                self.logobj.LogMsg(msg,WFA_DEBUG)   
                break 
        if log_file != "":
            log_file_path = TmsCommon.UccPath+"log"+"\\"+log_file
            log_file_dir=log_file
        else:
            print("Error - No folder was selected with name ", testCaseId)
            return 0        
        
        
        ########find the json file    
        #post the json file suing the file name
        cmd="dir "+TmsCommon.UccPath+"log"+"\\"+log_file_dir+"\\"+"*.json /o-d" 
        #print "the command", cmd
        msg= "the command "+cmd
        self.logobj.LogMsg(msg,WFA_DEBUG)   
        
        try:
            cmd_output=subprocess.check_output(cmd, shell=True)
        except:
            print("Error in running the command ", cmd)
            return 0
        #print "The command output ",cmd_output
        msg = "The command output %s", cmd_output
        self.logobj.LogMsg(msg,WFA_DEBUG)
        tmp1=cmd_output.split("\n")
        log_file =""
        for tmp2 in tmp1:
            filename = tmp2
		    # check the filename is json file
            if filename.find("json") > 0:
                #print "the file to be fetched", tmp2
                file_tmp=tmp2.split(" ")
                log_file=file_tmp[-1].rstrip()
                #print "The json file to be posted to TMS Server", log_file 
                break 
        if log_file !="":
            json_file_path = TmsCommon.UccPath+"log"+"\\"+log_file
        else:
            print("Error - No Json file was selected with name ", testCaseId)
            return 0

        ##


        #copy the json file to local store
        cmd="copy "+TmsCommon.UccPath+"log"+"\\"+log_file_dir+"\\"+log_file+" "+TmsCommon.TmsLocalStoragePath 
        #print "the command", cmd
        msg= "the command "+cmd
        self.logobj.LogMsg(msg,WFA_DEBUG)         
        try:
            cmd_output=subprocess.check_output(cmd, shell=False)
        except:
            print("Error in running the command ", cmd)
            return 0
        #print "The command output ",cmd_output
        msg= "The command output ",cmd_output
        self.logobj.LogMsg(msg,WFA_DEBUG) 



        # Get the DUT and Test bed ftp path details 
        JsonInput,JsonFile=localStorage.GetJsonFile("latest")        
        if JsonInput == 0:
            print("Error in getting JSON file contents for log file Path")
            return 0 			
        self.logobj.LogMsg("The Json contents"+JsonInput,WFA_DEBUG)
        try:
            data_tmp = json.loads(JsonInput)
            #data = json.dumps(data_tmp,sort_keys=True,indent=2)
        except: 
            print("Error in processing input JSON contents")
            return 0
        #print the data 
        msg= "Json data ",data_tmp
        self.logobj.LogMsg(msg,WFA_DEBUG) 
        #print "Json data", data_tmp
        
        #print "the keys",data_tmp.keys()
        logFile_tmp=data_tmp['TmsTestResult']
        #print "the dictory items",logFile_tmp['LogFileName']
        logFile=logFile_tmp['LogFileName']
        print("The log file path:",logFile)

        tmp1=logFile.split("/")
        tmp1_length=len(tmp1)
        event_index=tmp1.index(TmsCommon.TmsEventId)
        #print "The log file - Zipfile",tmp1[-1]
        #print "The log file - TestCase",tmp1[-2]
        #print "The log file - Test Bed deviceID",tmp1[-3]
        #print "The log file - DUT deviceID",tmp1[-4]
        #print "The log file - Event ID",tmp1[-5]
        print("The log file link - length",tmp1_length)
        print("The log file link - Event ID index",event_index)

        #zip the folder to the local storage path
        if (tmp1_length-event_index-1) > 3 :
            msg= "The log file - Zipfile,TestCase,Test Bed deviceID,DUT deviceID,Event ID ",tmp1[-1],tmp1[-2],tmp1[-3],tmp1[-4],tmp1[-5]
            self.logobj.LogMsg(msg,WFA_DEBUG) 
            tmp_Target_filename=tmp1[-5]+"&&"+tmp1[-4]+"&&"+tmp1[-3]+"&&"+tmp1[-2]+"&&"+tmp1[-1]
        else:
            msg= "The log file - Zipfile,TestCase,DUT deviceID,Event ID ",tmp1[-1],tmp1[-2],tmp1[-3],tmp1[-4]
            self.logobj.LogMsg(msg,WFA_DEBUG) 
            tmp_Target_filename=tmp1[-4]+"&&"+tmp1[-3]+"&&"+tmp1[-2]+"&&"+tmp1[-1]
        
        
        if TmsCommon.TmsCompressTool.find(" ") > 0:
            cmd="\""+TmsCommon.TmsCompressTool+"\""+" a \""+TmsCommon.TmsLocalStoragePath+tmp_Target_filename+"\" "+log_file_path
        else:
            cmd=TmsCommon.TmsCompressTool+" a \""+TmsCommon.TmsLocalStoragePath+tmp_Target_filename+"\" "+log_file_path
       
        #print "The command is",cmd
        self.logobj.LogMsg(cmd,WFA_DEBUG)   

        try:
            cmd_output=subprocess.check_output(cmd, shell=True)
        except:
            print("Error in running the command ", cmd)
            sys.exit(1)

        #print "The command output ",cmd_output
        
        ret=os.path.isfile(TmsCommon.TmsLocalStoragePath+tmp_Target_filename) 
        if(ret == False):
            print("Zip file not created in the local storage!!!")
            sys.exit(1)
        
        #test the ftp file posting
        bulkStorage.PostZipLogFile(tmp_Target_filename,TmsCommon.TmsLocalStoragePath+tmp_Target_filename)
        #post the zip file & json using the file name
        self.TmsPostOffline(_RestclientObj,_LocalStorageObj,"latest")
        
        #return
        self.logobj.LogMsg("Exit TmsRunOneTest function",WFA_DEBUG)
        return 1

    def TmsUpdateTestResult(self,_RestclientObj,_LocalStorageObj,_ProgName,_testID,_BulkStorageObj):
        restClient = _RestclientObj
        localStorage = _LocalStorageObj
        testCaseId = _testID
        progName = _ProgName
        bulkStorage=_BulkStorageObj
        self.logobj.LogMsg("Entry TmsUpdateTestResult function",WFA_DEBUG)

        #Get the UCC path
        #Check the config file presence
        CurrentDir=os.getcwd()
        print("current working directory", CurrentDir)
        SigmaTmsConfFile=".\\config\\"+ConfigFile

        #print " Sigma Tms config file  %s", SigmaTmsConfFile
        msg=" WTS Tms config file  %s", SigmaTmsConfFile
        self.logobj.LogMsg(msg,WFA_DEBUG)

        ret=os.path.isfile(SigmaTmsConfFile) 
        if(ret == False):
            print("!!! Tms Config file does not exist, Please Check the WTS !!!")
            sys.exit(1)

        ########Update the variables
        fo = open(SigmaTmsConfFile,"r+")
        tmp_fc = fo.readlines()
        fo.seek(0)
        for line in tmp_fc:
            #print "The line read", line
            if "TmsEventId=" in line:
                fo.write("TmsEventId"+"="+TmsCommon.TmsEventId+"\n")
            elif "DutParticipantName=" in line:
                fo.write("DutParticipantName"+"="+TmsCommon.DutParticipantName+"\n")
            elif "BulkStorageServer=" in line:
                fo.write("BulkStorageServer"+"="+TmsCommon.FtpServerIp+"\n")
            elif "TestbedParticipantName=" in line:
                fo.write("TestbedParticipantName"+"="+TmsCommon.TestbedParticipantName+"\n")
            else:
                fo.write(line)
        fo.truncate()
        fo.close()        

    
        #######   find the folder to be zipped
        cmd="dir "+ '\"' + CurrentDir + "\\log" + '\"' + " /ad /o-d" 
        #print "the command", cmd
        self.logobj.LogMsg(cmd,WFA_DEBUG)        
        try:
            cmd_output=str(subprocess.check_output(cmd, shell=True))
        except:
            print("Error in running the command ", cmd)
            sys.exit(1)
            
        #print "The command output ",cmd_output
        msg = "The command output %s", cmd_output
        # print("The command output is", cmd_output)


        self.logobj.LogMsg(msg,WFA_DEBUG)
        tmp1=cmd_output.split("\\r\\n")
        # print("The tmp1 is", tmp1)
        # print("Length of tmp1 is", len(tmp1))

        log_file =""
        for tmp2 in tmp1:
            filename = tmp2
            #print "inside for", tmp2,testCaseId
            if filename.find(testCaseId) > 0:
                #print "the file to be fetched", tmp2
                msg="the file to be fetched", tmp2
                self.logobj.LogMsg(msg,WFA_DEBUG)                
                file_tmp=tmp2.split(" ")
                log_file=file_tmp[-1].rstrip()
                # log_file=file_tmp[31].rstrip()      # TED: we hardcode the index at this moment
                print("The log folder to be posted to TMS Server", log_file)
                msg="The log folder to be posted to TMS Server", log_file 
                self.logobj.LogMsg(msg,WFA_DEBUG)   
                break 
        if log_file != "":
            log_file_path = CurrentDir+"\\log"+"\\"+log_file
            log_file_dir=log_file
        else:
            print("Error - No folder was selected with name ", testCaseId)
            sys.exit(1)     
        
        
        ########find the json file    
        #post the json file suing the file name
        cmd="dir " + '\"' + CurrentDir+"\\log"+"\\"+log_file_dir+"\\"+ '\"' + "*.json /o-d" 
        #print "the command", cmd
        msg= "the command "+cmd
        self.logobj.LogMsg(msg,WFA_DEBUG)   
        
        try:
            cmd_output=str(subprocess.check_output(cmd, shell=True))
        except:
            print("Error in running the command ", cmd)
            sys.exit(1)
        
        msg = "The command output %s", cmd_output
        # print("The command output is", cmd_output)
        self.logobj.LogMsg(msg,WFA_DEBUG)

        tmp1=cmd_output.split("\\r\\n")
        log_file =""
        for tmp2 in tmp1:
            filename = tmp2
		    # check the filename is json file
            if filename.find("json") > 0:
                #print "the file to be fetched", tmp2
                file_tmp=tmp2.split(" ")
                log_file=file_tmp[-1].rstrip()
                #print "The json file to be posted to TMS Server", log_file 
                break 
        if log_file !="":
            json_file_path = CurrentDir+"\\log"+"\\"+log_file
        else:
            print("Error - No Json file was selected with name ", testCaseId)
            sys.exit(1)

        ##
        
        localStoragePath = os.getcwd()
        # localStoragePath = localStoragePath[:-3] + "localstorage\\"
        localStoragePath = localStoragePath + "\\localstorage\\"

        try: 
            os.makedirs(localStoragePath)
        except OSError:
            if not os.path.isdir(localStoragePath):
                raise
        #copy the json file to local store
        cmd="copy "+CurrentDir+"\\log"+"\\"+log_file_dir+"\\"+log_file+" "+localStoragePath 
        #print "the command", cmd

        fPath = CurrentDir+"\\log"+"\\"+log_file_dir+"\\"+log_file 
        msg= "the command "+cmd
        self.logobj.LogMsg(msg,WFA_DEBUG)         
        try:
            shutil.copy2(fPath, localStoragePath)
            #cmd_output=subprocess.check_output(cmd, shell=False)
        except:
            print("Error in running the command ", cmd)
            print(cmd_output)
            sys.exit(1)
        #print "The command output ",cmd_output
        msg= "The command output ",cmd_output
        self.logobj.LogMsg(msg,WFA_DEBUG) 



        # Get the DUT and Test bed ftp path details 
        JsonInput,JsonFile=localStorage.GetJsonFile("latest")        
        if JsonInput == 0:
            print("Error in getting JSON file contents for log file Path")
            sys.exit(1)			
        self.logobj.LogMsg("The Json contents"+JsonInput,WFA_DEBUG)
        try:
            data_tmp = json.loads(JsonInput)
            #data = json.dumps(data_tmp,sort_keys=True,indent=2)
        except: 
            print("Error in processing input JSON contents")
            sys.exit(1)
        #print the data 
        msg= "Json data ",data_tmp
        self.logobj.LogMsg(msg,WFA_DEBUG) 
        #print "Json data", data_tmp
        
        #print "the keys",data_tmp.keys()
        logFile_tmp=data_tmp['TmsTestResult']
        #print "the dictory items",logFile_tmp['LogFileName']
        logFile=logFile_tmp['LogFileName']
        print("The log file path:",logFile)


        if os.path.isfile(SigmaTmsConfFile):

            with open(SigmaTmsConfFile, "r") as f:

                for line in f:
                    if re.search(r"TmsEventId=", line):
                        pos = line.index('=') + 1
                        data = line[pos:].rstrip('\r\n')
                        TmsEventId = data

                    if re.search(r"BulkStorageServer=", line):
                        pos = line.index('=') + 1
                        data = line[pos:].rstrip('\r\n')
                        BulkStorageServer = data

        tmp1=logFile.split("/")
        tmp1_length=len(tmp1)
        #zipFileName = tmp1[-1][:-4]
        zipFileName = tmp1[-1]

        print("The log file - Zipfile =>",zipFileName.replace(":","-"))

        TBdeviceID = "unknown"
        DUTdeviceID = "unknown"

        #zip the folder to the local storage path
        if (tmp1_length) < 5 :
            msg= "The log file - Zipfile,TestCase,Test Bed deviceID,DUT deviceID,Event ID ",zipFileName,testCaseId,TBdeviceID,DUTdeviceID,TmsEventId
        else:
            TBdeviceID = tmp1[-3]
            DUTdeviceID = tmp1[-4]
            
        self.logobj.LogMsg(msg,WFA_DEBUG) 

        tmp_Target_filename=TmsEventId+"&&"+DUTdeviceID+"&&"+TBdeviceID+"&&"+testCaseId+"&&"+zipFileName.replace(":","-")


        shutil.make_archive(localStoragePath+tmp_Target_filename, 'zip', log_file_path)
        
        #if TmsCommon.TmsCompressTool.find(" ") > 0:
        #    cmd="\""+TmsCommon.TmsCompressTool+"\""+" a \""+localStoragePath+tmp_Target_filename+"\" "+log_file_path
        #else:
        #    cmd=TmsCommon.TmsCompressTool+" a \""+localStoragePath+tmp_Target_filename+"\" "+log_file_path
       
        ##print "The command is",cmd
        #self.logobj.LogMsg(cmd,WFA_DEBUG)   

        #try:
        #    cmd_output=subprocess.check_output(cmd, shell=True)
        #except:
        #    print "Error in running the command ", cmd
        #    return 0

        print(localStoragePath+tmp_Target_filename)
        
        ret=os.path.isfile(localStoragePath+tmp_Target_filename + ".zip") 
        if(ret == False):
            print("Zip file not created in the local storage!!!")
            sys.exit(1)  
        
        #test the ftp file posting
        if TmsCommon.FTP_feature == "Enabled":
            bulkStorage.PostZipLogFile_from_UCC(tmp_Target_filename, localStoragePath, tmp_Target_filename)
        #post the zip file & json using the file name
        self.TmsPostOffline(_RestclientObj,_LocalStorageObj,"latest")
        
        #return
        self.logobj.LogMsg("Exit TmsUpdateTestResult function",WFA_DEBUG)
        return 1


    def FtpOnlyUpdateTestResult(self,_RestclientObj,_LocalStorageObj,_ProgName,_testID,_BulkStorageObj):
        restClient = _RestclientObj
        localStorage = _LocalStorageObj
        testCaseId = _testID
        progName = _ProgName
        bulkStorage=_BulkStorageObj
        self.logobj.LogMsg("Entry FtpOnlyUpdateTestResult function",WFA_DEBUG)

        #Get the UCC path
        #Check the config file presence
        CurrentDir=os.getcwd()
        SigmaTmsConfFile=".\\config\\"+ConfigFile

        #print " Sigma Tms config file  %s", SigmaTmsConfFile
        msg=" WTS Tms config file  %s", SigmaTmsConfFile
        self.logobj.LogMsg(msg,WFA_DEBUG)

        ret=os.path.isfile(SigmaTmsConfFile) 
        if(ret == False):
            print("!!! Tms Config file does not exist, Please Check the WTS !!!")
            sys.exit(1)

        ########Update the variables
        fo = open(SigmaTmsConfFile,"r+")
        tmp_fc = fo.readlines()
        fo.seek(0)
        for line in tmp_fc:
            #print "The line read", line
            if "TmsEventId=" in line:
                fo.write("TmsEventId"+"="+TmsCommon.TmsEventId+"\n")
            elif "DutParticipantName=" in line:
                fo.write("DutParticipantName"+"="+TmsCommon.DutParticipantName+"\n")
            elif "BulkStorageServer=" in line:
                fo.write("BulkStorageServer"+"="+TmsCommon.FtpServerIp+"\n")
            elif "TestbedParticipantName=" in line:
                fo.write("TestbedParticipantName"+"="+TmsCommon.TestbedParticipantName+"\n")
            else:
                fo.write(line)
        fo.truncate()
        fo.close()        

    
        #######   find the folder to be zipped
        cmd="dir "+CurrentDir+"\\log /ad /o-d" 
        #print "the command", cmd
        self.logobj.LogMsg(cmd,WFA_DEBUG)        
        try:
            cmd_output=str(subprocess.check_output(cmd, shell=True))
        except:
            print("Error in running the command ", cmd)
            sys.exit(1)
            
        #print "The command output ",cmd_output
        msg = "The command output %s", cmd_output


        self.logobj.LogMsg(msg,WFA_DEBUG)
        tmp1=cmd_output.split("\\r\\n")
        log_file =""
        for tmp2 in tmp1:
            filename = tmp2
            #print "inside for", tmp2,testCaseId
            if filename.find(testCaseId) > 0:
                #print "the file to be fetched", tmp2
                msg="the file to be fetched", tmp2
                self.logobj.LogMsg(msg,WFA_DEBUG)                
                file_tmp=tmp2.split(" ")
                log_file=file_tmp[-1].rstrip()
                #print "The log folder to be posted to TMS Server", log_file 
                msg="The log folder to be posted to TMS Server", log_file 
                self.logobj.LogMsg(msg,WFA_DEBUG)   
                break 
        if log_file != "":
            log_file_path = CurrentDir+"\\log"+"\\"+log_file
            log_file_dir=log_file
        else:
            print("Error - No folder was selected with name ", testCaseId)
            sys.exit(1)     
        
        
        ########find the json file    
        #post the json file suing the file name
        cmd="dir "+CurrentDir+"\\log"+"\\"+log_file_dir+"\\"+"*.json /o-d" 
        #print "the command", cmd
        msg= "the command "+cmd
        self.logobj.LogMsg(msg,WFA_DEBUG)   
        
        try:
            cmd_output=str(subprocess.check_output(cmd, shell=True))
        except:
            print("Error in running the command ", cmd)
            sys.exit(1)
        #print "The command output ",cmd_output
        msg = "The command output %s", cmd_output
        self.logobj.LogMsg(msg,WFA_DEBUG)
        tmp1=cmd_output.split("\\r\\n")
        log_file =""
        for tmp2 in tmp1:
            filename = tmp2
		    # check the filename is json file
            if filename.find("json") > 0:
                #print "the file to be fetched", tmp2
                file_tmp=tmp2.split(" ")
                log_file=file_tmp[-1].rstrip()
                #print "The json file to be posted to TMS Server", log_file 
                break 
        if log_file !="":
            json_file_path = CurrentDir+"\\log"+"\\"+log_file
        else:
            print("Error - No Json file was selected with name ", testCaseId)
            sys.exit(1)

        ##
        
        localStoragePath = os.getcwd()
        localStoragePath = localStoragePath + "\\localstorage\\"
        
        try: 
            os.makedirs(localStoragePath)
        except OSError:
            if not os.path.isdir(localStoragePath):
                raise
        #copy the json file to local store
        cmd="copy "+CurrentDir+"\\log"+"\\"+log_file_dir+"\\"+log_file+" "+localStoragePath 
        #print "the command", cmd

        fPath = CurrentDir+"\\log"+"\\"+log_file_dir+"\\"+log_file 
        msg= "the command "+cmd
        self.logobj.LogMsg(msg,WFA_DEBUG)         
        try:
            shutil.copy2(fPath, localStoragePath)
            #cmd_output=subprocess.check_output(cmd, shell=False)
        except:
            print("Error in running the command ", cmd)
            print(cmd_output)
            sys.exit(1)
        #print "The command output ",cmd_output
        msg= "The command output ",cmd_output
        self.logobj.LogMsg(msg,WFA_DEBUG) 



        # Get the DUT and Test bed ftp path details 
        JsonInput,JsonFile=localStorage.GetJsonFile("latest")        
        if JsonInput == 0:
            print("Error in getting JSON file contents for log file Path")
            sys.exit(1)			
        self.logobj.LogMsg("The Json contents"+JsonInput,WFA_DEBUG)
        try:
            data_tmp = json.loads(JsonInput)
            #data = json.dumps(data_tmp,sort_keys=True,indent=2)
        except: 
            print("Error in processing input JSON contents") 	
            sys.exit(1)
        #print the data 
        msg= "Json data ",data_tmp
        self.logobj.LogMsg(msg,WFA_DEBUG) 
        #print "Json data", data_tmp
        
        #print "the keys",data_tmp.keys()
        logFile_tmp=data_tmp['TmsTestResult']
        #print "the dictory items",logFile_tmp['LogFileName']
        logFile=logFile_tmp['LogFileName']
        print("The log file path:",logFile)


        if os.path.isfile(SigmaTmsConfFile):

            with open(SigmaTmsConfFile, "r") as f:

                for line in f:
                    if re.search(r"TmsEventId=", line):
                        pos = line.index('=') + 1
                        data = line[pos:].rstrip('\r\n')
                        TmsEventId = data

                    if re.search(r"BulkStorageServer=", line):
                        pos = line.index('=') + 1
                        data = line[pos:].rstrip('\r\n')
                        BulkStorageServer = data

        tmp1=logFile.split("/")
        tmp1_length=len(tmp1)
        #zipFileName = tmp1[-1][:-4]
        zipFileName = tmp1[-1]

        print("The log file - Zipfile =>",zipFileName.replace(":","-"))

        TBdeviceID = "unknown"
        DUTdeviceID = "unknown"

        #zip the folder to the local storage path
        if (tmp1_length) < 5 :
            msg= "The log file - Zipfile,TestCase,Test Bed deviceID,DUT deviceID,Event ID ",zipFileName,testCaseId,TBdeviceID,DUTdeviceID,TmsEventId
        else:
            TBdeviceID = tmp1[-3]
            DUTdeviceID = tmp1[-4]
            
        self.logobj.LogMsg(msg,WFA_DEBUG) 

        tmp_Target_filename=TmsEventId+"&&"+DUTdeviceID+"&&"+TBdeviceID+"&&"+testCaseId+"&&"+zipFileName.replace(":","-")


        shutil.make_archive(localStoragePath+tmp_Target_filename, 'zip', log_file_path)
        
        #if TmsCommon.TmsCompressTool.find(" ") > 0:
        #    cmd="\""+TmsCommon.TmsCompressTool+"\""+" a \""+localStoragePath+tmp_Target_filename+"\" "+log_file_path
        #else:
        #    cmd=TmsCommon.TmsCompressTool+" a \""+localStoragePath+tmp_Target_filename+"\" "+log_file_path
       
        ##print "The command is",cmd
        #self.logobj.LogMsg(cmd,WFA_DEBUG)   

        #try:
        #    cmd_output=subprocess.check_output(cmd, shell=True)
        #except:
        #    print "Error in running the command ", cmd
        #    return 0

        print(localStoragePath+tmp_Target_filename)
        
        ret=os.path.isfile(localStoragePath+tmp_Target_filename + ".zip") 
        if(ret == False):
            print("Zip file not created in the local storage!!!")
            sys.exit(1)  
        
        #test the ftp file posting
        if TmsCommon.FTP_feature == "Enabled":
            bulkStorage.PostZipLogFile_from_UCC(tmp_Target_filename,localStoragePath, tmp_Target_filename)

        #return
        self.logobj.LogMsg("Exit TmsUpdateTestResult function",WFA_DEBUG)
        return 1
