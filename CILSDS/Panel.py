#!/bin/env python
# -*- coding: utf-8 -*-

from Control import Control

class Panel(Control) :
    def __init__(self, parent, mgr) :
        Control.__init__(self, parent)
        self.mgr = mgr
        self.panels = []
        self.ctrls = {}

    def SetPosition(self, x, y, w, h) :
        self.visable = True
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def Layout(self) :
        for i in self.panels :
            i.Layout()

    def UpdateGC(self, gc) :
        Control.UpdateGC(self, gc)
        for i in self.panels :
            i.UpdateGC(gc)
        for i in self.ctrls :
            self.ctrls[i].UpdateGC(gc)

    def BeginDraw(self, drawBoarder=True) :
        Control.BeginDraw(self)
        if drawBoarder :
            self.gc.SetBrush(self.gc.brush['back'])
            if self.mgr.ActivePanel == self :
                self.gc.SetPen(self.gc.pen['act_panel_board'])
                self.gc.DrawRoundedRectangle(0,0,self.w,self.h,10)
            else :
                self.gc.SetPen(self.gc.pen['panel_board'])
                self.gc.DrawRectangle(0,0,self.w,self.h)
        for i in self.panels :
            i.Draw()

    def EndDraw(self) :
        for i in self.ctrls :
            self.ctrls[i].Draw() 
        Control.EndDraw(self)

    def Draw(self) :
        if self.visable:
            self.BeginDraw()
            self.EndDraw()

    def OnClick(self, x, y) :
        if self.visable:
            x = x - self.x
            y = y - self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                for i in self.ctrls :
                    if self.ctrls[i].OnClick(x,y) :
                        return True
                for i in self.panels :
                    if i.OnClick(x,y) :
                        return True
        return False

    def OnTouch(self, x, y) :
        rslt = False
        if self.visable:
            x = x - self.x
            y = y - self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                self.mgr.ActivePanel = self
            for i in self.ctrls :
                if self.ctrls[i].OnTouch(x,y) :
                    x = -1
                    y = -1
                    rslt = True
            for i in self.panels :
                if i.OnTouch(x,y) :
                    x = -1
                    y = -1
                    rslt = True
        return rslt


