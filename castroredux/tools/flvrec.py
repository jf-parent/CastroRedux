##
##  flvrec
##
##  Copyright (c) 2009-2010 by Yusuke Shinyama 
##
##  Refactoring by brome-hq 2015
##

import sys, socket, os, os.path, signal
from time import sleep
import threading

from vnc2flv.flv import FLVWriter
from vnc2flv.rfb import RFBNetworkClient, RFBError, PWDFile, PWDCache
from vnc2flv.video import FLVVideoSink, str2clip, str2size

class FlvRec(threading.Thread):
    """Record a vnc session to a flv file
    """
    def __init__(self, filename,
            host='localhost',
            port=5900,
            framerate=12,
            keyframe=120,
            preferred_encoding=(0,),
            pwdfile=None,
            blocksize=32,
            clipping=None,
            debug=0,
            verbose=1):

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
        self.debug = debug
        self.verbose = verbose

        self.pwdcache = PWDFile(self.pwdfile)
        self.is_recording = False
        self.keep_recording = True

    def run(self):
        self.fp = file(self.filename, 'wb')

        self.writer = FLVWriter(self.fp, framerate = self.framerate, debug = self.debug)

        self.sink = FLVVideoSink(
                            self.writer,
                            blocksize = self.blocksize, 
                            framerate = self.framerate, 
                            keyframe = self.keyframe,
                            clipping = self.clipping, 
                            debug = self.debug
                    )

        self.client = RFBNetworkClient(
                                self.host, 
                                self.port, 
                                self.sink, 
                                timeout = 500 / self.framerate,
                                pwdcache = self.pwdcache, 
                                preferred_encoding = self.preferred_encoding,
                                debug = self.debug
                        )

        if self.verbose:
            print >>sys.stderr, '[vnc2flv] Start recording'

        try:
            self.client.open()

            self.is_recording = True
            while self.keep_recording:
                self.client.idle()

            self.is_recording = False

        except socket.error as e:
            self.stop()
            raise Exception("[vnc2flv] Socket error: %s"%unicode(e))

        except RFBError as e:
            self.stop()
            raise Exception("[vnc2flv] RFB error: %s"%unicode(e))

    def stop(self):
        if self.verbose:
            print >>sys.stderr, '[vnc2flv] Stop recording...'

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
