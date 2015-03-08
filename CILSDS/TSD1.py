#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Instrument
from Control import Control
from Buttons import *

from math import pi,sqrt,sin,cos

class Stat(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.heading = 0

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc

            cs = gc.CreatePath()
            r = 130
            r2 = r*0.9
            r3 = r*0.95
            cs.AddCircle(0, 0, r)
            cs.AddCircle(0, 0, r/2)
            cs.AddCircle(0, 0, r/2*3)
            cs.AddCircle(0, 0, r*2)
            for i in xrange(60) :
                a = (pi/30.0)*i
                sa = sin(a)
                ca = cos(a)
                if i % 5 == 0 :
                    cs.MoveToPoint(r*sa,r*ca)
                    cs.AddLineToPoint(r2*sa,r2*ca)
                else :
                    cs.MoveToPoint(r*sa,r*ca)
                    cs.AddLineToPoint(r3*sa,r3*ca)
            self.compass_symbol = cs
        else :
            self.compass_symbol = None

    def drawContent(self, preview) :
        gc = self.gc
        if preview :
            gc.Clip(0,0,self.w*4,self.h*4)
            gc.Translate(self.w*2, 280)
        else :
            gc.Clip(0,0,self.w,self.h)
            gc.Translate(self.w/2, 280)

        r = 130
        gc.SetPen(gc.pen['white1'])
        gc.SetFont(gc.font['default'])
        gc.PushState()
        gc.Rotate(-self.heading/57.3)
        gc.StrokePath(self.compass_symbol)
        if not preview :
            for i in xrange(12) :
                if i == 0 :
                    txt = 'N'
                elif i == 3 :
                    txt = 'E'
                elif i == 6 :
                    txt = 'S'
                elif i == 9 :
                    txt = 'W'
                else :
                    txt = '{:.0f}'.format(i*3)
                te = gc.GetTextExtent(txt)
                gc.DrawText(txt,-te[0]/2,-0.88*r)
                gc.Rotate(pi/6.0)
        gc.PopState()

        gc.SetPen(gc.pen['white'])
        gc.DrawSymAC(gc,0,0,8,12)

        gc.ResetClip()

    def DrawContent(self) :
        self.drawContent(False)

    def DrawPreview(self) :
        self.gc.PushState()
        self.gc.Scale(0.25,0.25)
        self.drawContent(True)
        self.gc.PopState()

class TSD1(Instrument) :
    def __init__(self, mgr) :
        Instrument.__init__(self, None, mgr)
        self.ctrls['BtnVIEW'] = ButtonSwitch(self, 'VIEW', ['HSD', 'VSD'])
        self.ctrls['BtnDLNK'] = Button(self, 'DLNK>')
        self.ctrls['BtnCNTL'] = Button(self, 'CNTL>')
        self.ctrls['BtnFocus'] = Button(self, 'NORM')
        self.ctrls['BtnDEP'] = Button(self, 'DEP')
        self.ctrls['BtnMK'] = Button(self, 'MK')
        self.ctrls['BtnDCLT'] = Button(self, 'DCLT>')
        self.ctrls['BtnATK'] = Button(self, 'ATK')
        self.ctrls['BtnATK360'] = Button(self, 'ATK 360')
        self.ctrls['BtnBLDB'] = Button(self, 'BLDB')
        self.ctrls['BtnEMC'] = ButtonSwitch(self, 'EMC', ['EMC1', 'EMC2', 'EMC3', 'EMC4'])
        self.ctrls['STA'] = Stat(self)

    def Layout(self) :
        w = self.w
        h = self.h

        self.ctrls['STA'].SetPosition(0,0,w,h)

        self.ctrls['BtnVIEW'].SetLeftTop(80,2)
        self.ctrls['BtnDLNK'].SetLeftTop(150,2)
        self.ctrls['BtnCNTL'].SetRightTop(320,2)

        self.ctrls['BtnFocus'].SetRightTop(w,50)
        self.ctrls['BtnDEP'].SetRightTop(w,100)
        self.ctrls['BtnMK'].SetRightTop(w,150)
        self.ctrls['BtnDCLT'].SetRightTop(w,200)
        self.ctrls['BtnATK'].SetRightTop(w,250)

        self.ctrls['BtnATK360'].SetLeftTop(2,250)
        self.ctrls['BtnBLDB'].SetLeftTop(2,200)
        self.ctrls['BtnEMC'].SetLeftTop(2,150)

    def DrawContent(self) :
        heading=self.mgr.data['heading']

        self.ctrls['STA'].heading = heading

    def DrawPreviewContent(self) :
        self.ctrls['STA'].DrawPreview()

