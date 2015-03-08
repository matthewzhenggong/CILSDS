#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Instrument
from Control import Control
from Buttons import *

from math import pi,sqrt,sin,cos

class ArtificialHorizon(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.pitch = 5
        self.roll = 4
        self.heading = 3
        self.AoA=2
        self.AoS=1

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc
            gl = gc.CreatePath()
            sl = gc.CreatePath()
            w = self.w
            scale = w/30
            for i in range(5,95,5) :
                ss = i*scale
                gl.MoveToPoint(w/10,-4+ss)
                gl.AddLineToPoint(w/10,ss)
                gl.AddLineToPoint(w*3/10,ss)
                gl.MoveToPoint(-w/10,-4+ss)
                gl.AddLineToPoint(-w/10,ss)
                gl.AddLineToPoint(-w*3/10,ss)
                ss = -i*scale
                sl.MoveToPoint(w/10,ss)
                sl.AddLineToPoint(w*3/10,ss)
                sl.AddLineToPoint(w*3/10,ss+4)
                sl.MoveToPoint(-w/10,ss)
                sl.AddLineToPoint(-w*3/10,ss)
                sl.AddLineToPoint(-w*3/10,ss+4)
            self.ground_ladder = gl
            self.sky_ladder = sl

            ws = gc.CreatePath()
            ws.MoveToPoint(-16,0)
            ws.AddLineToPoint(-7.5,0)
            ws.AddLineToPoint(-4.5,7)
            ws.AddLineToPoint(0,0)
            ws.AddLineToPoint(4.5,7)
            ws.AddLineToPoint(7.5,0)
            ws.AddLineToPoint(16,0)
            self.w_symbol = ws

            h = self.h
            rs = gc.CreatePath()
            rs.MoveToPoint(2,h*0.40)
            rs.AddLineToPoint(0,h*0.37)
            rs.AddLineToPoint(-2,h*0.4)
            self.roll_symbol = rs

            ps = gc.CreatePath()
            ps.AddCircle(0, 0, 4)
            ps.MoveToPoint(0,-4)
            ps.AddLineToPoint(0,-12)
            ps.MoveToPoint(4,0)
            ps.AddLineToPoint(12,0)
            ps.MoveToPoint(-4,0)
            ps.AddLineToPoint(-12,0)
            self.airplane_symbol = ps
        else :
            self.ground_ladder = None
            self.sky_ladder = None
            self.w_symbol = None
            self.roll_symbol = None
            self.airplane_symbol = None

    def DrawContent(self) :
        w = self.w
        h = self.h
        r = sqrt(w*w+h*w)

        gc = self.gc
        gc.PushState()
        gc.Clip(0,0,w,h)
        gc.Translate(w/2,h/2)

        gc.PushState()
        scale = w/30
        roll_rad = self.roll/57.3
        gc.Rotate(-roll_rad)
        gc.Translate((self.AoS*cos(-roll_rad)+self.AoA*sin(-roll_rad))*scale,self.pitch*scale)

        #ground
        gc.SetPen(gc.pen['white'])
        gc.SetBrush(gc.brush['ground'])
        gc.DrawRectangle(-r-90*scale,0,2*r+180*scale,r+90*scale)

        gc.SetPen(gc.pen['white_sto'])
        gc.SetFont(gc.font['white10'])
        gc.PushState()
        for i in range(5,95,5) :
            gc.Translate(0, 5*scale)
            if abs(self.pitch + i) < h*0.5/scale :
                gc.DrawText('{:<3d}'.format(-i),w*3/10+5,-5)
                gc.DrawText('{:>3d}'.format(-i),-w*3/10-25,-5)
        gc.PopState()
        gc.StrokePath(self.ground_ladder)

        #sky
        gc.SetPen(gc.pen['white'])
        gc.SetBrush(gc.brush['sky'])
        gc.DrawRectangle(-r-90*scale,-r-90*scale,2*r+180*scale,r+90*scale)

        gc.PushState()
        for i in range(5,95,5) :
            gc.Translate(0, -5*scale)
            if abs(self.pitch - i) < h*0.5/scale :
                gc.DrawText('{:<3d}'.format(i),w*3/10+5,-5)
                gc.DrawText('{:>3d}'.format(i),-w*3/10-25,-5)
        gc.PopState()
        gc.StrokePath(self.sky_ladder)

        gc.PopState()

        gc.PushState()
        gc.Rotate(-180/57.3)
        for i in range(36) :
            ang =-i*10+180
            if ang - self.roll > 180 :
                ang -= 360
            elif ang - self.roll < -180 :
                ang += 360
            if ang < 45 and ang > -45 or abs(ang-self.roll)<30 :
                if i % 3 == 0 :
                    gc.StrokeLine(0,h*0.32,0,h*0.37)
                elif ang < 45 and ang > -45 :
                    gc.StrokeLine(0,h*0.34,0,h*0.37)
            gc.Rotate(10/57.3)
        gc.PopState()

        gc.PushState()
        gc.Rotate(-self.roll/57.3)
        gc.StrokePath(self.roll_symbol)
        gc.PopState()

        gc.StrokePath(self.w_symbol)

        gc.SetFont(gc.font['default'])
        txt = '{:03.0f}'.format(self.heading)
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,-te[0]/2,h/2-te[1])

        gc.SetPen(gc.pen['white1'])
        gc.Translate(self.AoS*scale, self.AoA*scale)
        gc.StrokePath(self.airplane_symbol)

        gc.PopState()
        gc.ResetClip()
        gc.SetBrush(gc.brush['none'])
        gc.SetPen(gc.pen['white'])
        gc.DrawRectangle(0,0,w,h)

class Clock(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.val = 500
        self.circle = 100.0

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc
            r = self.w/2 if self.w<self.h else self.h/2
            r2 = r*0.9
            cs = gc.CreatePath()
            for i in xrange(10) :
                a = (pi/5.0)*i
                sa = sin(a)
                ca = cos(a)
                cs.MoveToPoint(r*sa,r*ca)
                cs.AddLineToPoint(r2*sa,r2*ca)
            self.clock_symbol = cs
            ps = gc.CreatePath()
            ps.MoveToPoint(0,-0.5*r)
            ps.AddLineToPoint(0,-0.9*r)
            ps.AddLineToPoint(2,-0.7*r)
            ps.AddLineToPoint(-2,-0.7*r)
            ps.AddLineToPoint(0,-0.9*r)
            self.pointer_symbol = ps
        else :
            self.clock_symbol = None
            self.pointer_symbol = None

    def DrawContent(self) :
        gc = self.gc

        gc.Translate(self.w/2,self.h/2)

        gc.SetPen(gc.pen['white'])

        gc.StrokePath(self.clock_symbol)

        gc.PushState()
        gc.Rotate((self.val%self.circle)*2*pi/self.circle)
        gc.StrokePath(self.pointer_symbol)
        gc.PopState()

        gc.SetFont(gc.font['default'])
        txt = '{:.0f}'.format(self.val)
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,-te[0]/2,-te[1]/2)

class Compass(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.val = 0

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc

            r = self.w/2-60 if self.w-120<self.h else self.h/2
            if r < 75 :
                r = 75
            r2 = r*0.9
            r3 = r*0.95

            cs = gc.CreatePath()
            cs.AddCircle(0, 0, r)
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

            y = -0.88*r+12
            bs = gc.CreatePath()
            bs.MoveToPoint(0,-15)
            bs.AddLineToPoint(0,y)
            bs.AddLineToPoint(2,y+6)
            bs.AddLineToPoint(-2,y+6)
            bs.AddLineToPoint(0,y)
            bs.MoveToPoint(0,15)
            bs.AddLineToPoint(0,-y)
            self.arrow_symbol = bs

            bs = gc.CreatePath()
            bs.MoveToPoint(r/5,0)
            bs.AddLineToPoint(r/5+1,0)
            bs.MoveToPoint(r*2/5,0)
            bs.AddLineToPoint(r*2/5+1,0)
            bs.MoveToPoint(r*3/5,0)
            bs.AddLineToPoint(r*3/5+1,0)
            bs.MoveToPoint(-r/5,0)
            bs.AddLineToPoint(-r/5-1,0)
            bs.MoveToPoint(-r*2/5,0)
            bs.AddLineToPoint(-r*2/5-1,0)
            bs.MoveToPoint(-r*3/5,0)
            bs.AddLineToPoint(-r*3/5-1,0)

            bs.MoveToPoint(-r-30,-r/5)
            bs.AddLineToPoint(-r-30,-r/5-1)
            bs.MoveToPoint(-r-30,-r*2/5)
            bs.AddLineToPoint(-r-30,-r*2/5-1)
            bs.MoveToPoint(-r-30,-r*3/5)
            bs.AddLineToPoint(-r-30,-r*3/5-1)
            bs.MoveToPoint(-r-30,r/5)
            bs.AddLineToPoint(-r-30,r/5+1)
            bs.MoveToPoint(-r-30,r*2/5)
            bs.AddLineToPoint(-r-30,r*2/5+1)
            bs.MoveToPoint(-r-30,r*3/5)
            bs.AddLineToPoint(-r-30,r*3/5+1)
            self.bias_symbol = bs
        else :
            self.compass_symbol = None
            self.arrow_symbol = None
            self.bias_symbol = None

    def DrawContent(self) :
        gc = self.gc
        gc.Clip(0,0,self.w,self.h)

        r = self.w/2-60 if self.w-120<self.h else self.h/2
        if r < 75 :
            r = 75

        gc.Translate(self.w/2,r)

        gc.SetPen(gc.pen['white'])
        gc.SetFont(gc.font['default'])
        gc.DrawEllipse(-r, -r, 2*r, 2*r)
        gc.PushState()
        gc.Rotate(-self.val/57.3)
        gc.StrokePath(self.compass_symbol)
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

        gc.SetPen(gc.pen['purple'])
        gc.StrokePath(self.arrow_symbol)

        gc.SetPen(gc.pen['big_purple'])
        gc.StrokePath(self.bias_symbol)

        txt = 'SLG'
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,-r-30-te[0]/2,-te[1]/2)

        gc.SetPen(gc.pen['white'])
        gc.DrawSymAC(gc,0,0,8,12)

        gc.ResetClip()

class EFI(Instrument) :
    def __init__(self, mgr) :
        Instrument.__init__(self, None, mgr)
        self.ctrls['AH'] = ArtificialHorizon(self)
        self.ctrls['V'] = Clock(self)
        self.ctrls['H'] = Clock(self)
        self.ctrls['H'].circle = 1000.0
        self.ctrls['C'] = Compass(self)
        self.ctrls['BtnCDI'] = ButtonSwitch(self, 'CDI', ['OFF', 'ON'])
        self.ctrls['BtnFD'] = ButtonSwitch(self, 'FD', ['OFF', 'ON'], align_right=True)
        self.ctrls['BtnJPALS'] = Button(self, 'JPALS')
        self.ctrls['BtnILS'] = Button(self, 'ILS')
        self.ctrls['BtnCNTL'] = Button(self, 'CNTL>')

    def Layout(self) :
        margin = 60
        ahw = 320-2*margin
        x0 = (self.w-320)/2
        rdir = 75
        ahh = 512-68-margin-rdir*2
        self.ctrls['AH'].SetPosition(x0+margin, margin, ahw, ahh)
        self.ctrls['V'].SetPosition(x0, margin+ahh/2-margin/2, margin, margin)
        self.ctrls['H'].SetPosition(x0+margin+ahw, margin+ahh/2-margin/2, margin, margin)
        self.ctrls['C'].SetPosition(x0, margin+ahh, 320, self.h-margin-ahh)
        self.ctrls['BtnCDI'].SetLeftTop(2,50)
        self.ctrls['BtnFD'].SetRightTop(self.w,50)
        self.ctrls['BtnJPALS'].SetCenterTop(self.w/2,2)
        self.ctrls['BtnILS'].SetCenterTop(self.w*0.7,2)
        self.ctrls['BtnCNTL'].SetRightTop(self.w,2)

    def DrawContent(self) :

        VC = self.mgr.data['VC']
        VG=self.mgr.data['VG']
        Ma=self.mgr.data['Ma']
        AoA=self.mgr.data['AoA']
        AoS=self.mgr.data['AoS']
        GLoad=self.mgr.data['GLoad']
        ASL=self.mgr.data['ASL']
        AGL=self.mgr.data['AGL']
        pitch=self.mgr.data['pitch']
        roll=self.mgr.data['roll']
        heading=self.mgr.data['heading']
        ROC=self.mgr.data['ROC']


        margin = 60
        ahw = 320-2*margin
        x0 = (self.w-320)/2
        rdir = 75
        ahh = 512-68-margin-rdir*2

        gc = self.gc
        gc.SetFont(gc.font['default'])
        gc.DrawText(u'GS{:4.0f}\nM {:4.2f}\nα{:4.1f}\nG {:4.1f}'.format(VG,Ma,AoA,GLoad),x0+2,margin+margin/2+ahh/2)
        gc.DrawText(u'{:5.0f}'.format(ROC),x0+margin+ahw+2,margin+margin/2+ahh/2+5)
        if AGL > 0 :
            gc.DrawText(u'R{:5.0f}'.format(AGL),x0+margin+ahw+2,margin+margin/2+ahh/2+20)

        gc.SetPen(gc.pen['white1'])
        gc.DrawLines([(0,margin+ahh),(self.w,margin+ahh)])

        ah = self.ctrls['AH']
        ah.pitch = pitch
        ah.roll = roll
        ah.heading = heading
        ah.AoA=AoA
        ah.AoS=AoS

        self.ctrls['V'].val = VC
        self.ctrls['H'].val = ASL
        self.ctrls['C'].val = heading

    def DrawPreviewContent(self) :
        VC = self.mgr.data['VC']
        ASL=self.mgr.data['ASL']
        heading=self.mgr.data['heading']

        self.ctrls['V'].val = VC
        self.ctrls['H'].val = ASL

        gc = self.gc

        gc.PushState()
        self.ctrls['V'].DrawContent()
        gc.PopState()

        gc.PushState()
        gc.Translate(self.w-self.ctrls['H'].w,0)
        self.ctrls['H'].DrawContent()
        gc.PopState()

        gc.SetFont(gc.font['white20'])
        txt = '{:03.0f}'.format(heading)
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,(self.w-te[0])/2,self.h/2)

