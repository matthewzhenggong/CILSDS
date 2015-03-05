#!/bin/env python
# -*- coding: utf-8 -*-

import wx
import time
import itertools

from Window import Window

from Resources import CreateResources
from EFI import EFI
from SMS import SMS

class Manager(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.SetForegroundColour(wx.GREEN)
        self.SetBackgroundColour(wx.BLACK)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnUp)

        self.data = {
        'VC' : 287.5,
        'VG' : 625,
        'Ma' : 1.03,
        'AoA' : 1.3,
        'AoS' : 0.3,
        'GLoad' : 1.1,
        'ASL' : 11030,
        'AGL' : 10000,
        'pitch' : -15.6,
        'roll' : -8,
        'heading' : 7,
        'ROC' : -100,
        }

        self.mini_panels = {}
        self.body_panels = { \
                'EFI':EFI(self), \
                'SMS':SMS(self) \
                }

        self.Body0 = Window(self,0, 0, 0, 640, 512, 1, \
                ['EFI','SMS','FCS','HUD','DAS','ASR', 'H1'])
        self.Body1 = Window(self,1, 640, 0, 640, 512, 5, \
                ['TSD-1','TSD-2','FCS','HUD','DAS','ASR', 'H2'])

        self.panels = [self.Body0, self.Body1]
        self.ActivePanel = None

        self.clicking = False
        self.enduring = 0

        self.dc = None

    def UpdateData(self, data):
        for i in data :
            self.data[i] = data[i]
        self.Refresh(False)

    def OnSize(self, evt):
        self.sz = self.GetClientSize()
        self.sz.width = max(1, self.sz.width)
        self.sz.height = max(1, self.sz.height)
        self._buffer = wx.EmptyBitmap(self.sz.width, self.sz.height, 32)
        self.dc = wx.MemoryDC(self._buffer)
        self.gc = wx.GraphicsContext.Create(self.dc)
        CreateResources(self.gc)
        for i in self.mini_panels :
            self.mini_panels[i].UpdateGC(self.gc)
        for i in self.body_panels :
            self.body_panels[i].UpdateGC(self.gc)
        for i in self.panels :
            i.UpdateGC(self.gc)

        self.width = 1280.0
        self.height = 512.0
        scalex = self.sz.width/self.width
        scaley = self.sz.height/self.height
        self.base_scale = scalex if scalex<scaley else scaley

        evt.Skip()
        
    def Close(self):
        for i in self.mini_panels :
            self.mini_panels[i].UpdateGC(None)
        for i in self.body_panels :
            self.body_panels[i].UpdateGC(None)
        for i in self.panels :
            i.UpdateGC(None)
        self.gc = None
        self.dc.SelectObject(wx.NullBitmap);
        self.dc = None
        self._buffer = None

    def OnPaint(self, evt):
        if self.dc :
            self.Draw()

            dc = wx.PaintDC(self)
            dc.Blit(0,0,self.sz.width,self.sz.height,self.dc, 0, 0)

    def OnMotion(self, evt):
        if self.clicking :
            pos = evt.GetPosition()
            self.cur_pos = pos
            self.OnTouch(pos.x/self.base_scale, pos.y/self.base_scale)
            self.Refresh(False)

    def OnDown(self, evt):
        evt.Skip()
        self.clicking = True
        self.click_time = time.time()
        pos = evt.GetPosition()
        self.last_pos = self.cur_pos = pos
        self.OnTouch(pos.x/self.base_scale, pos.y/self.base_scale)
        self.Refresh(False)

    def OnUp(self, evt):
        self.clicking = False
        delta_time = time.time() - self.click_time
        pos = evt.GetPosition()
        delta_pos = pos - self.last_pos
        if delta_time < 0.4 and abs(delta_pos.x) < 5 and  abs(delta_pos.y) <5 :
            self.OnClick(pos.x/self.base_scale, pos.y/self.base_scale)
        self.OnTouch(-1,-1)
        self.Refresh(False)

    def OnClick(self, x,y):
        for i in self.panels :
            i.OnClick(x,y) 

    def OnTouch(self, x,y):
        for i in self.panels :
            i.OnTouch(x,y) 

    def Draw(self):
        tick0 = time.time()

        gc = self.gc
        gc.PushState()
        gc.Scale(self.base_scale, self.base_scale)

        for i in self.panels :
            i.Draw()

        gc.PopState()
        if self.clicking :
            gc.SetPen(gc.pen['clicking_cross'])
            gc.StrokeLine(self.cur_pos.x-50, self.cur_pos.y,
                    self.cur_pos.x+50, self.cur_pos.y)
            gc.StrokeLine(self.cur_pos.x, self.cur_pos.y-50,
                    self.cur_pos.x, self.cur_pos.y+50)
        self.enduring = time.time()-tick0
        gc.SetFont(gc.font['default'])
        gc.DrawText('%.3f'%self.enduring, 0,0)

    def SwapWindow(self, ctrl, x, y):
        for (i,j) in itertools.izip(self.Body0.panels, self.Body1.panels) :
            tt = i.title
            i.SetTitle(j.title)
            j.SetTitle(tt)
        frame_id = self.Body0.frame_id
        self.Body0.Layout(self.Body1.frame_id)
        self.Body1.Layout(frame_id)

