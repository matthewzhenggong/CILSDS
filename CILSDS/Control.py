#!/bin/env python
# -*- coding: utf-8 -*-

class Control :
    def __init__(self, parent) :
        self.parent = parent
        self.x=self.y=self.w=self.h=0
        self.txt = ''
        self.brush = 'default'
        self.font = 'default'
        self.pen = 'default'
        self.visable = True
        self.touching = False
        self.click_func = None
        self.gc = None

    def Visable(self, v) :
        self.visable = v

    def UpdateGC(self, gc) :
        self.gc = gc
        self.RebuildPath()

    def SetClickFunc(self, func) :
        self.click_func = func

    def OnClick(self, x, y) :
        if self.visable :
            x -= self.x
            y -= self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                if self.click_func :
                    self.click_func(self,x,y)
                    return True
        return False

    def OnTouch(self, x, y) :
        self.touching = False
        if self.visable :
            x -= self.x
            y -= self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                self.touching = True
                return True
        return False

    def BeginDraw(self) :
        self.gc.PushState()
        self.gc.Translate(self.x,self.y)

    def EndDraw(self) :
        self.gc.PopState()

    def RebuildPath(self) :
        pass

    def SetSize(self, w, h) :
        if w != self.w or h != self.h :
            self.w = w
            self.h = h
            self.RebuildPath()

    def SetPosition(self, x, y, w, h) :
        self.visable = True
        self.x = x
        self.y = y
        self.SetSize(w,h)

    def SetLeftTop(self, x, y) :
        self.visable = True
        self.x = x
        self.y = y

    def SetRightTop(self, x, y) :
        self.visable = True
        self.x = x-self.w
        self.y = y

    def SetLeftBottom(self, x, y) :
        self.visable = True
        self.x = x
        self.y = y-self.h

    def SetRightBottom(self, x, y) :
        self.visable = True
        self.x = x-self.w
        self.y = y-self.h

    def Visable(self, v) :
        self.visable = v


