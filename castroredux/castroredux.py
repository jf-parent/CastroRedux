# -*- coding: utf-8 -*-

import os

from tools.flvrec import FlvRec

class CastroRedux(object):
    """CastroRedux vnc to flv recorder
    
    Attributes:
        outfile_file (str)
        host (str)
        port (int)
        pwdfile (str)
        framerate (int)
        keyframe (int)
        clipping (int)
        debug (bool)
    """
    def __init__(self,
                 outfile_file,
                 host,
                 port = 5900,
                 pwdfile = os.path.join(os.path.expanduser("~"), ".vnc", "passwd"),
                 framerate = 12,
                 keyframe = 120,
                 clipping = None,
                 debug = False):

        self.outfile_file = outfile_file
        self.host = host
        self.port = port
        self.framerate = framerate
        self.keyframe = keyframe
        self.clipping = clipping
        self.pwdfile = pwdfile
        self.debug = debug

    def start(self):
        """Start the recorder
        """

        self.recorder = FlvRec(
                            self.outfile_file,
                            host = self.host,
                            port = self.port,
                            framerate = self.framerate,
                            keyframe = self.keyframe,
                            pwdfile = self.pwdfile,
                            clipping = self.clipping,
                            debug =self.debug
                        )

        self.recorder.start()

    def stop(self):
        """Stop the recorder
        """
        self.recorder.stop()
