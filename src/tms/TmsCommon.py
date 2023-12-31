﻿###################################################################
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
from tms.TmsHeaders import *


# common utilities

def ResetAndClean():
    self.logobj.LogMsg("Inside ResetAndClean function",WFA_DEBUG)
    # check the processes and kill gracefully to make system clear

# checks for element in the list/array
def is_exists(_in_array,_in_element):
    array_len = len(_in_array)
    i = 0
    while i < array_len :
        if str(_in_array[i]) == str(_in_element):
            #print "matchfound"
            return "1"
        i= i+1
                 
    return "0"

def TmsClientInitialize():
    #print "Inside TmsClientInitialize function"
    global TmsServerUN
    global TmsServerPS
    global TmsServerURL
    global TmsServerHostName
    global FtpServerUN
    global FtpServerPS
    global FtpServerIp
    global UccPath
    global TmsEventId
    global DutParticipantName
    global TestbedParticipantName
    global TmsLocalStoragePath
    global TmsCompressTool
    global FtpServerIpAddress
    global BulkStorageServer
    global TMS_feature
    global FTP_feature
   
    global ConfigFile
     
    #Check the config file exits and accessible
    CurrentDir=os.getcwd()
    UccPath = CurrentDir                # TED: Since there is no entry of UCCPath defined in the TmsClient.conf file, we hardcode it here
    print("current working directory", CurrentDir)
    ConfFile=".\\config\\"+ConfigFile
    print("config file directory", ConfFile)
    ret=os.path.isfile(ConfFile) 
    # ret=os.path.isfile("TmsCommon.py") 
    if(ret == False):
        print("Config file does not exist!!!")
        sys.exit(1)    
      
    #Read the config file and assign the values
    try:
        fo = open(ConfFile, "r")
    except:
        print("Error opening config file!!!")
        sys.exit(1)

    line = fo.readline()
    #print "Comment Read %s", line
    while line:
        #print "Read %s", line
        if line[0] == '#' or line[0] == "" or line[0] == '\n':
            #comment line
            #print "Comment Read %s", line
            line = fo.readline()
            continue
        else:
            tmp_params = line.split("=")

        if len(tmp_params) > 2:
            print("Error with parameter %s", tmp_params[0])
            line = fo.readline()
            continue  

        if tmp_params is not None :
            if tmp_params[0] == 'TMS_feature':
                TMS_feature=tmp_params[1].rstrip()
            elif tmp_params[0] == 'FTP_feature':
                FTP_feature=tmp_params[1].rstrip()
            elif tmp_params[0] == 'TmsServerUN':
                TmsServerUN=tmp_params[1].rstrip()
            elif tmp_params[0] == 'TmsServerPS':
                TmsServerPS=tmp_params[1].rstrip()     
            elif tmp_params[0] == 'TmsServerURL':
                TmsServerURL=tmp_params[1].rstrip()    
            elif tmp_params[0] == 'TmsServerHostName':
                TmsServerHostName=tmp_params[1].rstrip()     
            elif tmp_params[0] == 'FtpServerUN':
                FtpServerUN=tmp_params[1].rstrip()     
            elif tmp_params[0] == 'FtpServerPS':
                FtpServerPS=tmp_params[1].rstrip()     
            elif tmp_params[0] == 'FtpServerIp':
                FtpServerIp=tmp_params[1].rstrip()     
            elif tmp_params[0] == 'BulkStorageServer':
                BulkStorageServer=tmp_params[1].rstrip()   
            elif tmp_params[0] == 'FtpServerIpAddress':
                FtpServerIpAddress=tmp_params[1].rstrip()     
            elif tmp_params[0] == 'UccPath':
                UccPath=tmp_params[1].rstrip()    
            elif tmp_params[0] == 'TmsEventId':
                TmsEventId=tmp_params[1].rstrip() 
            elif tmp_params[0] == 'DutParticipantName':
                DutParticipantName=tmp_params[1].rstrip()   
            elif tmp_params[0] == 'TestbedParticipantName':
                TestbedParticipantName=tmp_params[1].rstrip()
            elif tmp_params[0] == 'TmsLocalStoragePath':
                TmsLocalStoragePath=tmp_params[1].rstrip()
            elif tmp_params[0] == 'TmsCompressTool':
                TmsCompressTool=tmp_params[1].rstrip()
            else:               
                print (tmp_params[1])
            line = fo.readline()	
            continue

    fo.close()

    if TMS_feature=="" or TMS_feature=="Disabled":
        self.logobj.LogMsg( "TMS is disabled..change conf file to enable")
        sys.exit(1)
    #if any of the variable is not defined error 
    if TmsServerUN=="" or TmsServerPS=="" or TmsServerURL=="" or FtpServerUN=="" or FtpServerPS=="" or \
       FtpServerIp=="" or TmsEventId=="" or DutParticipantName=="" or TestbedParticipantName=="" or TmsCompressTool=="":
        self.logobj.LogMsg( "Not all parameters initialized ")
        sys.exit(1)

