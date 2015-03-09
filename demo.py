#!/bin/env python
# -*- coding: utf-8 -*-

import sys
if not hasattr(sys, 'frozen'):
    import wxversion
    wxversion.select('3.0')

import wx
import os
import os.path as path
import argparse
import logging
from CILSDS import Manager as MFD
from subprocess import Popen
import threading
import time
import socket
import json

log = logging.getLogger('scene')

class RedirectError(object):
    def __init__(self):
        pass

    def write(self,string):
        string = string.strip('\r\n\t ')
        if string :
            log.error(string)

class RedirectInfo(object):
    def __init__(self):
        pass

    def write(self,string):
        string = string.strip('\r\n\t ')
        if string :
            log.info(string)

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.AppendText(string)


class MyFrame(wx.Frame):
        def __init__(
                        self, parent, ID, title, pos=wx.DefaultPosition,
                        size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
                        ):

                wx.Frame.__init__(self, parent, ID, title, pos, size, style)

                self.panel = wx.Panel(self,-1)
                self.panel.SetForegroundColour(wx.GREEN)
                self.panel.SetBackgroundColour(wx.BLACK)

                self.log_txt = wx.TextCtrl(self.panel, -1, "", size=(300,100), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
                self.log_txt.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                self.log_txt.SetForegroundColour(wx.GREEN)
                self.log_txt.SetBackgroundColour(wx.BLACK)

                self.log = logging.getLogger('scene')
                self.log.setLevel(logging.INFO)
                self.log_handle = logging.StreamHandler(RedirectText(self.log_txt))
                self.log_handle.setFormatter(logging.Formatter('%(asctime)s:%(message)s'))
                #self.log.addHandler(self.log_handle)
                # redirect stdout to log
                #sys.stdout=RedirectInfo()
                #sys.stderr=RedirectError()

                self.log.info('Starting...')

                self.MFD = MFD.Manager(self.panel, self.log)

                self.Bind(wx.EVT_SIZE, self.OnSize)
                self.Bind(wx.EVT_CLOSE, self.OnClose)

                self.aclink = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.aclink.settimeout(0.1)
                self.aclink.bind(('',0))
                sockname = self.aclink.getsockname()
		self.log.info('CILSDS listening on '+sockname.__str__())

                self.enable = True
                self.running = True
                self.thread = threading.Thread(target=self.run)
                self.thread.daemon = True
                self.thread.start()

                try :
                    # start up associate simulation application
                    sys.path.append('.')
                    bin_path = path.abspath(path.dirname(sys.argv[0]))
                    sys.path.append(bin_path)
                    parser = argparse.ArgumentParser(description='Parse and start aircraft-complex.')
                    parser.add_argument("--cmd", help="commander")
                    parser.add_argument("--cwd", help="workspace directory")
                    args = parser.parse_args()
                    if args.cwd :
                        os.chdir(args.cwd)
                        self.log.info('Change current work directory to '+args.cwd)
                    if args.cmd :
                        cmd = args.cmd+' --mfdport {}'.format(sockname[1])
                        self.ac = Popen(cmd, shell=False, bufsize=-1)
                        self.log.info('Running '+cmd)
                    else :
                        self.ac = None
                except :
                    self.ac = None


        def run(self) :
            while self.enable :
                try :
                    (dat,address) = self.aclink.recvfrom(4096)
                except socket.timeout :
                    continue
                try :
                    dat = json.loads(dat)
                    if 'data' in dat :
                        self.MFD.UpdateData(dat['data'])
                        pass
                    elif 'log' in dat :
                        self.log.info(dat['log'])
                except :
                    pass
            self.running = False

        def OnClose(self, evt):
            evt.Skip()
            if self.ac :
                self.ac.terminate()
            self.enable = False
            self.thread.join()
            self.MFD.Close()

        def OnSize(self, evt):
            #self.log.info('Resizing...')
            sz = self.GetClientSize()
            self.panel.SetSize(sz)
            scalex = sz.width/(1280.0*2)
            scaley = (sz.height-100)/1024.0
            scale = scalex if scalex<scaley else scaley
            w = scale*1280*2
            h = scale*1024
            self.MFD.SetSize((w,h))
            self.log_txt.SetPosition((0, h))
            self.log_txt.SetSize((sz.width,sz.height-h))

if __name__ == '__main__' :
        app = wx.App(False)
        frame = MyFrame(None, wx.ID_ANY,'Cockpit integrative large screen display system', size=(1296,650))
        frame.Show(True)
        app.MainLoop()

