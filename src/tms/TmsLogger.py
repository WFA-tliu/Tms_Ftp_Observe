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
import logging
import logging.handlers
from tms.TmsHeaders import * 
import tms.TmsCommon


class WfaLogger:
    def __init__(self,_filename,_level):
        #'_filename is the log file and _level is the debug level to this file'
        global LogPath
        self.fileName = _filename
        self.Level = _level
        fname=self.fileName + ".log"
        fname="%s/%s" % (LogPath,fname)
        ret=os.path.exists(LogPath) 
        if(ret == False):
            # Log folder does not exist
            try:
                os.system("mkdir " + LogPath)
            except:   
                print("!!!Error creating Log folder!!!")
                sys.exit(0)
        #print "log file %s, level %d", _filename,_level
        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger('TmsClient')
        if (_level == 0):
            # No logger or ERROR/CRITICAL
            self.my_logger.setLevel(logging.ERROR)
        elif (_level == 1):
            #Info level
            self.my_logger.setLevel(logging.INFO)
        elif (_level == 2):
            #Debug level
            self.my_logger.setLevel(logging.DEBUG)
        else:
            #default Warning
            self.my_logger.setLevel(logging.WARNING)

        #set the formater
        formatter=logging.Formatter('%(asctime)s - %(name)s- ::%(levelname)s:: - %(message)s')
                    
        # Add the log message handler to the logger
        # Maximum log file size is 2MB and one backup file
        self.handler = logging.handlers.RotatingFileHandler(
              fname, maxBytes=100000, backupCount=1)
        self.handler.setFormatter(formatter)
        
        self.my_logger.addHandler(self.handler)
        self.my_logger.info ("###########################################################\n")    
        self.my_logger.info ("Wi-Fi Alliance - TMS Client")
        self.my_logger.info('Logging started in file - %s',fname)

    def LogMsg(self,_msg,_level):
        if _level == WFA_ERROR:
            self.my_logger.error ('*** %s ***',_msg)
            
        elif _level == WFA_WARNING:
            self.my_logger.warn ('** %s **',_msg)
            
        elif _level == WFA_DEBUG:
            self.my_logger.debug ('%s',_msg)
        
        else:
            self.my_logger.info ('%s',_msg)
        