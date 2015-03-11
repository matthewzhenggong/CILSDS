#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Instrument
from Control import Control
from Buttons import *

from math import pi,sqrt,sin,cos,atan2,radians

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
        self.contacts = None
        self.lat = 23
        self.lon = 112
        self.alt = 5000
        self.vn = 0
        self.ve = 0
        self.vd = 0
        self.select_x = -1000
        self.select_y = -1000

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
        r4 = self.parent.ctrls['RANGE'].GetValue()

        heading = radians(self.heading)
        cos_heading = cos(heading)
        sin_heading = sin(heading)

        gc.SetPen(gc.pen['white1.5'])
        gc.SetFont(gc.font['default'])
        gc.PushState()
        gc.Rotate(-heading)
        gc.StrokePath(self.compass_symbol)
        gc.PopState()

        if not preview :
            txt = '{:.0f}'.format(r4*0.25)
            te = gc.GetTextExtent(txt)
            gc.DrawText(txt,-r/2*sin_heading-te[0]/2,-r/2*cos_heading-te[1]/2)

            txt = '{:.0f}'.format(r4*0.5)
            te = gc.GetTextExtent(txt)
            gc.DrawText(txt,-r*sin_heading-te[0]/2,-r*cos_heading-te[1]/2)

            txt = '{:.0f}'.format(r4*0.75)
            te = gc.GetTextExtent(txt)
            gc.DrawText(txt,-r*1.5*sin_heading-te[0]/2,-r*1.5*cos_heading-te[1]/2)

            txt = '{:.0f}'.format(r4)
            te = gc.GetTextExtent(txt)
            gc.DrawText(txt,-r*2*sin_heading-te[0]/2,-r*2*cos_heading-te[1]/2)

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
                gc.DrawText(txt,-te[0]/2+0.88*r*sin(-heading+i*pi/6.0),-te[1]/2-0.88*r*cos(-heading+i*pi/6.0))

        (deg2m_lat, deg2m_lon) = LatLon2Meter(radians(self.lat))
        scale = (2*r)/(r4*1000.0)
        if self.nav :
            gc.SetPen(gc.pen['white'])
            l = gc.CreatePath()
            c = gc.CreatePath()
            first = True
            for i,p in enumerate(self.nav['PNTS']) :
                y1 = -(p[0]-self.lat)*deg2m_lat*scale
                x1 = (p[1]-self.lon)*deg2m_lon*scale
                x = cos_heading*x1 + sin_heading*y1
                y =-sin_heading*x1 + cos_heading*y1
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

        select_obj = None
        select_circle = 5*5
        if self.contacts :
            select = self.contacts['select']
            for i,obj in enumerate(self.contacts['OBJS']) :
                p = obj['pos']
                y1 = -(p[0]-self.lat)*deg2m_lat*scale
                x1 = (p[1]-self.lon)*deg2m_lon*scale
                x = cos_heading*x1 + sin_heading*y1
                y =-sin_heading*x1 + cos_heading*y1
                idf = obj['idf']
                if idf == 'foe' :
                    gc.SetPen(gc.pen['red'])
                elif idf == 'friend' :
                    gc.SetPen(gc.pen['green'])
                else :
                    gc.SetPen(gc.pen['yellow'])
                typ = obj['type']
                if typ == 'missile' :
                    gc.StrokeLines([(x-5,y),(x,y-5),(x+5,y)])
                else :
                    gc.StrokeLines([(x-5,y),(x-5,y-5),(x+5,y-5),(x+5,y)])
                vel = obj['vel']
                speed = sqrt(vel[0]**2+vel[1]**2)/300.0*5+5
                if speed > 20 :
                    speed = 20
                hd = atan2(vel[1],vel[0])
                gc.StrokeLines([(x,y),(x+speed*sin(-heading+hd),y-speed*cos(-heading+hd))])
                if select == i :
                    c = gc.CreatePath()
                    c.AddCircle(x-1,y-1,12)
                    gc.SetPen(gc.pen['lock'])
                    gc.StrokePath(c)
                cc = (x - self.select_x)**2 + (y - self.select_y)**2 
                if cc < select_circle :
                    select_obj = obj
                    select_circle = cc
                    select_x = x
                    select_y = y

        if select_obj :
            self.select_x = select_x
            self.select_y = select_y
            gc.SetPen(gc.pen['green'])
            gc.SetBrush(gc.brush['tab'])
            gc.DrawRectangle(50,0, 100,100)
            p = select_obj['pos']
            y1 = -(p[0]-self.lat)*deg2m_lat
            x1 = (p[1]-self.lon)*deg2m_lon
            dist = sqrt(x1**2+y1**2)
            vel = select_obj['vel']
            vel[0] -= self.vn
            vel[1] -= self.ve
            relvel =-(vel[0]*y1+vel[1]*x1)/dist*3.6
            gc.DrawText('Id:{}\nH{:.0f}\n{:.0f}kph'.format(select_obj['callsign'],p[2], relvel) ,50,0)

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
                self.select_x = x-self.w/2
                self.select_y = y-280
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
        contacts=self.mgr.data['CONTACTS']
        vn=self.mgr.data['Vn']
        ve=self.mgr.data['Ve']
        vd=self.mgr.data['Vd']

        self.ctrls['STA'].heading = heading
        self.ctrls['STA'].nav = nav
        self.ctrls['STA'].contacts = contacts
        self.ctrls['STA'].lat = lat
        self.ctrls['STA'].lon = lon
        self.ctrls['STA'].alt = h
        self.ctrls['STA'].vn = vn
        self.ctrls['STA'].ve = ve
        self.ctrls['STA'].vd = vd

    def DrawPreviewContent(self) :
        self.DrawContent()
        self.ctrls['STA'].DrawPreview()

