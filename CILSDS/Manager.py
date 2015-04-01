#!/bin/env python
# -*- coding: utf-8 -*-

import wx
import time
import itertools

from Window import Window

from Resources import CreateResources
from EFI import EFI
from SMS import SMS
from TSD1 import TSD1 as TSD
from Header1 import Header1
from Header2 import Header2

from TFLIR import TFLIR
from SRCH import SRCH
from TWD import TWD
from ASR import ASR
from FUEL import FUEL
#from HUD import HUD
from ENG import ENG

class Manager(wx.Panel):
    def __init__(self, parent, log, half=False):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.half = half
        self.SetWindowStyle(wx.WANTS_CHARS)
        self.SetForegroundColour(wx.GREEN)
        self.SetBackgroundColour(wx.BLACK)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnUp)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        self.data = {
        'Vn' : 37.5,
        'Ve' : 87.5,
        'Vd' : 7.5,
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
        'lat' : 64.4,
        'lon' : 121.8,
        'throttle' : 0,
        'fuelrate' : 0,
        'T' : 0,
        'mode' : 'AA1',
        'cursor' : [0, 0, 0, 0, 0],
        'SMS' : {'GUN':182, 'CHAT':10, 'FLAT':20,  \
                 'pylons':{ 'firing': -1, 'RDY':4, \
                    'SRM' : [('AIM9',1), ('AIM9',11)], \
                    'MRM' : [('A120',4), ('A120',5), ('A120',7), ('A120',8)], \
                    'AS' : [] }
                },
        'NAV' : {'cur':1,
            'PNTS':[(23.0, 109.0, 5000),(23.0, 108.5, 5000),(23.2, 108.0, 5000),(22.2, 107.0, 5000)]
            },
        'SENS' : {'infrWorkStatus':2,'RadarWorkStatus':3, \
                'ESM_OpenFlag':1,'ESM_WorkModul':1,\
                'ECM_OpenFlag':1,'ECM_WorkModul':1},
        'CONTACTS' : [
                {'pos':(23.0, 107.0, 5000), 'vel':(0,300,0), 'type':'airplane', 'idf':'foe'},
                {'pos':(23.2, 108.0, 5000), 'vel':(0,-300,0), 'type':'airplane', 'idf':'friend'},
                {'pos':(23.0, 107.5, 5000), 'vel':(300,0,0), 'type':'airplane', 'idf':'unknown'},
                {'pos':(23.2, 107.5, 5000), 'vel':(0,-1000,0), 'type':'missile', 'idf':'friend'},
            ],
        }

        self.using_panels = {}
        self.free_panels = { \
                'EFI':EFI(self),
                'SMS':SMS(self),
                'TSD-1':TSD(self),
                'TSD-2':TSD(self),
                'TSD-3':TSD(self),
                'TFLIR':TFLIR(self),
                'SRCH':SRCH(self),
                'TWD':TWD(self),
                'ASR':ASR(self),
                'FUEL':FUEL(self),
                #'HUD':HUD(self),
                'ENG':ENG(self),
                'H1':Header1(self),
                'H2':Header2(self),
                }

        if self.half :
            self.Body0 = Window(self,0, 0, 0, 640, 512, 2, \
                    ['EFI','TSD-1','TFLIR','SMS','FUEL','ASR', 'H1'])
            self.panels = [self.Body0]
        else :
            self.Body0 = Window(self,0, 0, 0, 640, 512, 3, \
                    ['EFI','SMS','FCS','HUD','DAS','ASR', 'H1'])
            self.Body1 = Window(self,1, 640, 0, 640, 512, 4, \
                    ['TSD-1','TSD-2','FCS','HUD','DAS','ASR', 'H2'])
            self.panels = [self.Body0, self.Body1]

        self.ActivePanel = None

        self.clicking = False
        self.enduring = 0
        self.cursor = [100,100]
        self.cursor_step = 1


        self.cursor_press_cnt = 0
        self.cursor_left_cnt = 0
        self.cursor_right_cnt = 0
        self.cursor_up_cnt = 0
        self.cursor_down_cnt = 0

        self.dc = None
        self.msgs = []

    def UpdateData(self, data):
        self.data.update(data)
        self.UpdateCursorFromData(self.data['cursor'])
        self.Refresh(False)

    def UpdateCursorFromData(self, cursor):
        if cursor[4] :
            self.cursor_press_cnt += 1
            if self.cursor_press_cnt == 6 :
                self.cursor_press_cnt = 1
                self.keyDown(wx.WXK_RETURN)
        elif self.cursor_press_cnt != 0 :
                self.cursor_step = 1
                self.cursor_press_cnt = 0

        if cursor[0] :
            self.cursor_left_cnt += 1
            if self.cursor_left_cnt == 4 :
                self.cursor_left_cnt = 1
                self.keyDown(wx.WXK_LEFT)
        elif self.cursor_left_cnt != 0 :
                self.cursor_step = 1
                self.cursor_left_cnt = 0

        if cursor[1] :
            self.cursor_right_cnt += 1
            if self.cursor_right_cnt == 4 :
                self.cursor_right_cnt = 1
                self.keyDown(wx.WXK_RIGHT)
        elif self.cursor_right_cnt != 0 :
                self.cursor_step = 1
                self.cursor_right_cnt = 0

        if cursor[2] :
            self.cursor_up_cnt += 1
            if self.cursor_up_cnt == 4 :
                self.cursor_up_cnt = 1
                self.keyDown(wx.WXK_UP)
        elif self.cursor_up_cnt != 0 :
                self.cursor_step = 1
                self.cursor_up_cnt = 0

        if cursor[3] :
            self.cursor_down_cnt += 1
            if self.cursor_down_cnt == 4 :
                self.cursor_down_cnt = 1
                self.keyDown(wx.WXK_DOWN)
        elif self.cursor_down_cnt != 0 :
                self.cursor_step = 1
                self.cursor_down_cnt = 0

    def RestoreInstrument(self, title, panel) :
        if title in self.using_panels :
            del self.using_panels[title]
        self.free_panels[title] = panel

    def GetInstrument(self, slot, title) :
        if title in self.using_panels :
            self.using_panels[title].FreeInstrument()
        if title in self.free_panels :
            panel = self.free_panels[title]
            del self.free_panels[title]
            self.using_panels[title] = slot
            return panel
        return None

    def OnSize(self, evt):
        self.sz = self.GetClientSize()
        self.sz.width = max(1, self.sz.width)
        self.sz.height = max(1, self.sz.height)
        self._buffer = wx.EmptyBitmap(self.sz.width, self.sz.height, 32)
        self.dc = wx.MemoryDC(self._buffer)
        self.gc = wx.GraphicsContext.Create(self.dc)
        CreateResources(self.gc)
        for i in self.panels :
            i.UpdateGC(self.gc)

        if self.half :
            self.width = 640.0
        else :
            self.width = 1280.0
        self.height = 512.0
        scalex = self.sz.width/self.width
        scaley = self.sz.height/self.height
        self.base_scale = scalex if scalex<scaley else scaley

        self.Refresh(False)
        evt.Skip()
        
    def Close(self):
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
        self.SetFocus()
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

    def OnKeyUp(self, event):
        self.cursor_step = 1

    def AccelCursor(self):
        if self.cursor_step < 10 :
            self.cursor_step += 0.2
        if self.cursor[0] < 0 :
            self.cursor[0] = 0 
        elif self.cursor[0] > 1280 :
            self.cursor[0] = 1280 
        if self.cursor[1] < 0 :
            self.cursor[1] = 0 
        elif self.cursor[1] > 512 :
            self.cursor[1] = 512
        self.OnTouch(self.cursor[0], self.cursor[1])

    def OnKeyDown(self, event):
        k = event.GetKeyCode()
        self.keyDown(k)

    def keyDown(self, k):
        if k in [wx.WXK_LEFT, wx.WXK_NUMPAD_LEFT, wx.WXK_NUMPAD4, ord('A')]:
            self.cursor[0] -= self.cursor_step
            self.AccelCursor()
        elif k in [wx.WXK_RIGHT, wx.WXK_NUMPAD_RIGHT, wx.WXK_NUMPAD6, ord('D')] :
            self.cursor[0] += self.cursor_step
            self.AccelCursor()
        elif k in [wx.WXK_UP, wx.WXK_NUMPAD_UP, wx.WXK_NUMPAD8, ord('W')] :
            self.cursor[1] -= self.cursor_step
            self.AccelCursor()
        elif k in [wx.WXK_DOWN, wx.WXK_NUMPAD_DOWN, wx.WXK_NUMPAD2, ord('S')] :
            self.cursor[1] += self.cursor_step
            self.AccelCursor()
        elif k in [wx.WXK_RETURN, wx.WXK_SPACE] :
            self.OnClick(self.cursor[0], self.cursor[1])
        elif self.ActivePanel :
            self.ActivePanel.OnKey(k, self.cursor)
        self.Refresh(False)

    def Draw(self):
        tick0 = time.time()

        gc = self.gc
        gc.PushState()
        gc.Scale(self.base_scale, self.base_scale)

        for i in self.panels :
            i.Draw()

        gc.SetPen(gc.pen['cursor'])
        gc.StrokeLine(self.cursor[0]-4, self.cursor[1]-6,
                    self.cursor[0]+4, self.cursor[1]-6)
        gc.StrokeLine(self.cursor[0]-0.01, self.cursor[1],
                    self.cursor[0]+0.01, self.cursor[1])
        gc.StrokeLine(self.cursor[0]-4, self.cursor[1]+6,
                    self.cursor[0]+4, self.cursor[1]+6)
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

    def SwapWindow(self, event):
        if self.half :
            return

        for (i,j) in itertools.izip(self.Body0.panels, self.Body1.panels) :
            tt = i.title
            i.SetInstrument(j.title)
            j.SetInstrument(tt)
        frame_id = self.Body0.frame_id
        self.Body0.Layout(self.Body1.frame_id)
        self.Body1.Layout(frame_id)

    def PushMessage(self, msg):
        self.msgs.append(msg)

    def GetAllMessages(self):
        msgs = self.msgs
        self.msgs = []
        return msgs

