##
##  flvrec
##
##  Copyright (c) 2009-2010 by Yusuke Shinyama 
##
##  Refactoring by brome-hq 2015-2016
##

import sys, socket, os, os.path, signal
import traceback
from time import sleep
import threading
import logging

from vnc2flv.flv import FLVWriter
from vnc2flv.rfb import RFBNetworkClient, RFBError, PWDFile, PWDCache
from vnc2flv.video import FLVVideoSink, str2clip, str2size

class FlvRec(threading.Thread):
    """Record a vnc session to a flv file
    """
    def __init__(self, filename,
            host = 'localhost',
            port = 5900,
            framerate = 12,
            keyframe = 120,
            preferred_encoding = (0,),
            pwdfile = None,
            blocksize = 32,
            clipping = None,
            logger_level = 'INFO',
            logger_log_dir = False,
            logger_name = 'CastroRedux'):

        super(FlvRec, self).__init__()

        self.filename = filename
        self.host = host
        self.port = port
        self.framerate = framerate
        self.keyframe = keyframe
        self.preferred_encoding = preferred_encoding
        self.pwdfile = pwdfile
        self.blocksize = blocksize
        self.clipping = clipping
        self.logger_name = logger_name
        self.logger_level = logger_level
        self.logger_log_dir = logger_log_dir

        self.pwdcache = PWDFile(self.pwdfile)
        self.is_recording = False
        self.keep_recording = True

        self.configure_logger()

    def configure_logger(self):
        #Logger
        self.logger = logging.getLogger(self.logger_name)

        #File logger
        if self.logger_log_dir:
            fh = logging.FileHandler(os.path.join(
                self.logger_log_dir,
                '%s-CastroRedux.log'%self.logger_name
            ))
            self.logger.addHandler(fh)

        #Stream logger 
        self.logger.addHandler(logging.StreamHandler())

        #Set level
        self.logger.setLevel(self.logger_level)

    def run(self):
        self.fp = file(self.filename, 'wb')

        self.writer = FLVWriter(self.fp, framerate = self.framerate, logger  = self.logger)

        self.sink = FLVVideoSink(
                            self.writer,
                            blocksize = self.blocksize, 
                            framerate = self.framerate, 
                            keyframe = self.keyframe,
                            clipping = self.clipping, 
                            logger = self.logger
                    )

        self.client = RFBNetworkClient(
                                self.host, 
                                self.port, 
                                self.sink, 
                                timeout = 500 / self.framerate,
                                pwdcache = self.pwdcache, 
                                preferred_encoding = self.preferred_encoding,
                                logger = self.logger
                        )

        self.logger.info('[vnc2flv] Start recording')

        try:
            self.client.open()

            self.is_recording = True
            while self.keep_recording:
                self.client.idle()

            self.is_recording = False

        except socket.error as e:
            self.is_recording = False
            tb = traceback.format_exc()
            self.logger.error("[vnc2flv] Socket traceback: %s"%unicode(tb))
            self.stop()
            raise Exception("[vnc2flv] Socket error: %s"%unicode(e))

        except RFBError as e:
            self.is_recording = False
            tb = traceback.format_exc()
            self.logger.error("[vnc2flv] RFB traceback: %s"%unicode(tb))
            self.stop()
            raise Exception("[vnc2flv] RFB error: %s"%unicode(e))

    def stop(self):
        self.logger.info('[vnc2flv] Stop recording...')

        self.keep_recording = False
        #Wait until the recording is over
        for i in range(10):
            if self.is_recording:
                sleep(1)
            else:
                break

        self.client.close()
        self.writer.close()
        self.fp.close()
