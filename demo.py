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
import traceback

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
                parser = argparse.ArgumentParser(prog='CILSDS',description='Cockpit integrative large screen display system')
                parser.add_argument("--cmd", help="commander")
                parser.add_argument("--cwd", help="workspace directory")
                parser.add_argument("--debug", action='store_true',help="loggin on debug level ")
                parser.add_argument("--half", action='store_true',help="loggin on debug level ")
                args = parser.parse_args()
                self.half = args.half
                if self.half :
                    size = (size[0]/2,size[1])

                wx.Frame.__init__(self, parent, ID, title, pos, size, style)

                self.panel = wx.Panel(self,-1)
                #self.panel.SetForegroundColour(wx.GREEN)
                #self.panel.SetBackgroundColour(wx.BLACK)

                self.log_txt = wx.TextCtrl(self.panel, -1, "", size=(300,100), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
                self.log_txt.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                self.log_txt.SetForegroundColour(wx.GREEN)
                self.log_txt.SetBackgroundColour(wx.BLACK)

                self.btn_save = wx.Button(self.panel, -1, 'Save')
                self.btn_cls = wx.Button(self.panel, -1, 'Clear')

                self.log = logging.getLogger('scene')
                self.log_handle = logging.StreamHandler(RedirectText(self.log_txt))
                self.log_handle.setFormatter(logging.Formatter('%(asctime)s:%(message)s'))
                self.log.addHandler(self.log_handle)
                # redirect stdout to log
                sys.stdout=RedirectInfo()
                sys.stderr=RedirectError()

                if args.debug :
                    self.log.setLevel(logging.DEBUG)
                else :
                    self.log.setLevel(logging.INFO)

                self.log.info('Starting...')

                self.MFD = MFD.Manager(self.panel, self.log, args.half)

                self.Bind(wx.EVT_SIZE, self.OnSize)
                self.Bind(wx.EVT_CLOSE, self.OnClose)
                self.Bind(wx.EVT_BUTTON, self.OnClsLog, self.btn_cls)
                self.Bind(wx.EVT_BUTTON, self.OnSavLog, self.btn_save)

                self.aclink = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.aclink.settimeout(0.1)
                try :
                    self.aclink.bind(('',0))
                except :
                    self.aclink.bind(('',7132))
                    traceback.print_exc()
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
                    if args.cwd :
                        os.chdir(args.cwd)
                        self.log.debug('Change current work directory to '+args.cwd)
                    if args.cmd :
                        cmd = args.cmd+' --mfdport {}'.format(sockname[1])
                        self.ac = Popen(cmd, shell=False, bufsize=-1)
                        self.log.debug('Running '+cmd)
                    else :
                        self.ac = None
                except :
                    traceback.print_exc()
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
                    elif 'log' in dat :
                        self.log.info(dat['log'])
                except :
                    pass
                msgs = self.MFD.GetAllMessages()
                if msgs :
                    self.aclink.sendto(json.dumps(msgs),address)
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
            if self.half :
                w = 1280.0
            else :
                w = 1280.0*2
            scalex = sz.width/w
            scaley = (sz.height-100)/1024.0
            scale = scalex if scalex<scaley else scaley
            w = scale*w
            h = scale*1024
            self.MFD.SetSize((w,h))
            self.log_txt.SetPosition((0, h))
            self.log_txt.SetSize((sz.width,sz.height-h-20))
            self.btn_save.SetSize((50,20))
            self.btn_save.SetPosition((0, sz.height-20))
            self.btn_cls.SetSize((50,20))
            self.btn_cls.SetPosition((50, sz.height-20))

        def OnClsLog(self, evt):
            self.log_txt.Clear()

        def OnSavLog(self, evt):
            dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="log", wildcard="Text files (*.txt)|*.txt", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                self.log_txt.SaveFile(dlg.GetPath())

if __name__ == '__main__' :
        app = wx.App(False)
        frame = MyFrame(None, wx.ID_ANY,'Cockpit integrative large screen display system', size=(1296,650))
        frame.Show(True)
        app.MainLoop()

