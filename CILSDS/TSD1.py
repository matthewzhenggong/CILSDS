#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Instrument
from Control import Control
from Buttons import *

from math import pi,sqrt,sin,cos,radians

def LatLon2Meter(lat) :
    m1 = 111132.92
    m2 = -559.82
    m3 = 1.175
    m4 = -0.0023
    p1 = 111412.84
    p2 = -93.5
    p3 = 0.118

    deg2m_lat = m1 + (m2 * cos(2 * lat)) + (m3 * cos(4 * lat)) + \
    		(m4 * cos(6 * lat));
    deg2m_lon = (p1 * cos(lat)) + (p2 * cos(3 * lat)) + \
    			(p3 * cos(5 * lat));
    return (deg2m_lat, deg2m_lon)


class Stat(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.heading = 0
        self.nav = None
        self.lat = 23
        self.lon = 112
        self.h = 5000

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

        scale = (2*r)/(self.parent.ctrls['RANGE'].GetValue()*1000.0)
        if self.nav :
            (deg2m_lat, deg2m_lon) = LatLon2Meter(radians(self.lat))
            gc.SetPen(gc.pen['white'])
            l = gc.CreatePath()
            c = gc.CreatePath()
            first = True
            for i,p in enumerate(self.nav['PNTS']) :
                y = -(p[0]-self.lat)*deg2m_lat*scale
                x = (p[1]-self.lon)*deg2m_lon*scale
                if i ==self.nav['cur'] :
                    c.AddCircle(x,y,6)
                c.AddCircle(x,y,3)
                if first :
                    first = False
                    l.MoveToPoint(x,y)
                else :
                    l.AddLineToPoint(x,y)
            gc.StrokePath(l)
            gc.StrokePath(c)

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

    def OnTouch(self, x, y) :
        self.touching = False
        if self.visable :
            x -= self.x
            y -= self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                pass
        return False

    def OnClick(self, x, y) :
        if self.visable :
            x -= self.x
            y -= self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                if self.click_func :
                    self.click_func(ClickEvent(self,x,y))
        return False


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
        self.ctrls['RANGE'] = ButtonNumSpin(self, [4,8,20,40,80,160,400,800], 5)
        self.ctrls['STA'] = Stat(self)

    def Layout(self) :
        w = self.w
        h = self.h

        self.ctrls['STA'].SetPosition(0,0,w,h)

        self.ctrls['BtnVIEW'].SetLeftTop(80,2)
        self.ctrls['BtnDLNK'].SetLeftTop(200,2)
        self.ctrls['BtnCNTL'].SetRightTop(320,2)

        self.ctrls['BtnFocus'].SetRightTop(w,50)
        self.ctrls['BtnDEP'].SetRightTop(w,100)
        self.ctrls['BtnMK'].SetRightTop(w,150)
        self.ctrls['BtnDCLT'].SetRightTop(w,200)
        self.ctrls['BtnATK'].SetRightTop(w,250)

        self.ctrls['BtnATK360'].SetLeftTop(2,250)
        self.ctrls['BtnBLDB'].SetLeftTop(2,200)
        self.ctrls['BtnEMC'].SetLeftTop(2,150)
        self.ctrls['RANGE'].SetLeftTop(2,50)

    def DrawContent(self) :
        heading=self.mgr.data['heading']
        lat=self.mgr.data['lat']
        lon=self.mgr.data['lon']
        h=self.mgr.data['ASL']
        nav=self.mgr.data['NAV']

        self.ctrls['STA'].heading = heading
        self.ctrls['STA'].nav = nav
        self.ctrls['STA'].lat = lat
        self.ctrls['STA'].lon = lon
        self.ctrls['STA'].h = h

    def DrawPreviewContent(self) :
        self.ctrls['STA'].DrawPreview()

