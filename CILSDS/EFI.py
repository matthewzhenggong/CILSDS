#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Panel
from Control import Control

from math import pi,sqrt

class ArtificialHorizon(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.pitch = 5
        self.roll = 4
        self.heading = 3
        self.AoA=2
        self.AoS=1

    def Draw(self) :
        self.BeginDraw()

        w = self.w
        h = self.h
        r = sqrt(w*w+h*w)

        gc = self.gc
        gc.PushState()
        gc.Clip(0,0,w,h)
        gc.Translate(w/2,h/2)

        gc.PushState()
        scale = w/30
        gc.Rotate(-self.roll/57.3)
        gc.Translate(0,self.pitch*scale)

        gc.SetPen(gc.pen['white'])
        gc.SetBrush(gc.brush['ground'])
        gc.DrawRectangle(-r,0,2*r,r+90*scale)

        gc.SetPen(gc.pen['white_sto'])
        gc.SetFont(gc.font['white10'])
        l = gc.CreatePath()
        gc.PushState()
        for i in range(5,95,5) :
            gc.Translate(0, 5*scale)
            ss = i*scale
            l.MoveToPoint(w/10,-4+ss)
            l.AddLineToPoint(w/10,ss)
            l.AddLineToPoint(w*3/10,ss)
            l.MoveToPoint(-w/10,-4+ss)
            l.AddLineToPoint(-w/10,ss)
            l.AddLineToPoint(-w*3/10,ss)
            gc.DrawText('{:<3d}'.format(-i),w*3/10+5,-5)
            gc.DrawText('{:>3d}'.format(-i),-w*3/10-25,-5)
        gc.PopState()
        gc.StrokePath(l)

        gc.SetPen(gc.pen['white'])
        gc.SetBrush(gc.brush['sky'])
        gc.DrawRectangle(-r,-r-90*scale,2*r,r+90*scale)

        l = gc.CreatePath()
        gc.PushState()
        for i in range(5,95,5) :
            gc.Translate(0, -5*scale)
            ss = -i*scale
            l.MoveToPoint(w/10,ss)
            l.AddLineToPoint(w*3/10,ss)
            l.AddLineToPoint(w*3/10,ss+4)
            l.MoveToPoint(-w/10,ss)
            l.AddLineToPoint(-w*3/10,ss)
            l.AddLineToPoint(-w*3/10,ss+4)
            gc.DrawText('{:<3d}'.format(i),w*3/10+5,-5)
            gc.DrawText('{:>3d}'.format(i),-w*3/10-25,-5)
        gc.PopState()
        gc.StrokePath(l)

        gc.PopState()

        gc.SetBrush(gc.brush['none'])

        gc.PushState()
        gc.Rotate(-30/57.3)
        gc.StrokeLine(0,h*0.35,0,h*0.4)
        for i in range(6) :
            gc.Rotate(10/57.3)
            if i % 3 == 2 :
                gc.StrokeLine(0,h*0.35,0,h*0.4)
            else :
                gc.StrokeLine(0,h*0.37,0,h*0.4)
        gc.PopState()

        if abs(self.roll) < 35 :
            gc.PushState()
            gc.Rotate(-self.roll/57.3)
            gc.StrokeLines([(2,h*0.43),(0,h*0.4),(-2,h*0.43)])
            gc.PopState()

        gc.StrokeLines([(-16,0),(-7.5,0),(-4.5,7),(0,0),(4.5,7),(7.5,0),(16,0)])

        gc.SetFont(gc.font['default'])
        txt = '{:03.0f}'.format(self.heading)
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,-te[0]/2,h/2-te[1])

        gc.SetPen(gc.pen['white1'])
        gc.Translate(self.AoS*scale, self.AoA*scale)
        gc.DrawEllipse(-4, -4, 8, 8)
        gc.StrokeLine(0,-4,0,-12)
        gc.StrokeLine(4,0,12,0)
        gc.StrokeLine(-4,0,-12,0)

        gc.PopState()
        gc.ResetClip()
        gc.SetPen(gc.pen['white'])
        gc.DrawRectangle(0,0,w,h)

        self.EndDraw()

class Clock(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.val = 500
        self.circle = 100.0

    def Draw(self) :
        self.BeginDraw()

        gc = self.gc
        gc.Translate(self.w/2,self.h/2)

        r = self.w/2 if self.w<self.h else self.h/2

        gc.SetPen(gc.pen['white'])
        gc.PushState()
        gc.StrokeLine(0,-r,0,r*-0.9)
        for i in xrange(9) :
            gc.Rotate(pi/5.0)
            gc.StrokeLine(0,-r,0,r*-0.9)
        gc.PopState()

        gc.PushState()
        gc.Rotate((self.val%self.circle)*2*pi/self.circle)
        gc.StrokeLines([(0,-0.5*r),(0,-0.9*r),(3,-0.7*r),(-3,-0.7*r),(0,-0.9*r)])
        gc.PopState()

        gc.SetFont(gc.font['default'])
        txt = '{:.0f}'.format(self.val)
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,-te[0]/2,-te[1]/2)

        self.EndDraw()

class Compass(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.val = 0

    def Draw(self) :
        self.BeginDraw()

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
        for i in xrange(360/6) :
            if i % 5 == 0 :
                if i == 0 :
                    txt = 'N'
                elif i == 90/6 :
                    txt = 'E'
                elif i == 180/6 :
                    txt = 'S'
                elif i == 270/6 :
                    txt = 'W'
                else :
                    txt = '{:.0f}'.format(i*0.6)
                te = gc.GetTextExtent(txt)
                gc.DrawText(txt,-te[0]/2,-0.88*r)
                gc.StrokeLine(0,-r,0,r*-0.9)
            else :
                gc.StrokeLine(0,-r,0,r*-0.95)
            gc.Rotate(6*pi/180.0)
        gc.PopState()

        gc.SetPen(gc.pen['purple'])
        y = -0.88*r+te[1]
        gc.StrokeLines([(0,-15),(0,y),(2,y+6),(-2,y+6),(0,y)])
        gc.StrokeLine(0,15,0,-y)
        gc.SetPen(gc.pen['big_purple'])
        gc.StrokeLine(r/5,0,r/5+1,0)
        gc.StrokeLine(r*2/5,0,r*2/5+1,0)
        gc.StrokeLine(r*3/5,0,r*3/5+1,0)
        gc.StrokeLine(-r/5,0,-r/5-1,0)
        gc.StrokeLine(-r*2/5,0,-r*2/5-1,0)
        gc.StrokeLine(-r*3/5,0,-r*3/5-1,0)

        gc.StrokeLine(-r-30,-r/5,-r-30,-r/5-1)
        gc.StrokeLine(-r-30,-r*2/5,-r-30,-r*2/5-1)
        gc.StrokeLine(-r-30,-r*3/5,-r-30,-r*3/5-1)
        gc.StrokeLine(-r-30,r/5,-r-30,r/5+1)
        gc.StrokeLine(-r-30,r*2/5,-r-30,r*2/5+1)
        gc.StrokeLine(-r-30,r*3/5,-r-30,r*3/5+1)

        txt = 'SLG'
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,-r-30-te[0]/2,-te[1]/2)

        gc.SetPen(gc.pen['white'])
        gc.DrawSymAC(gc,0,0,8,12)

        gc.ResetClip()
        self.EndDraw()


class EFI(Panel) :
    def __init__(self, mgr) :
        Panel.__init__(self, None, mgr)
        self.ctrls['AH'] = ArtificialHorizon(self)
        self.ctrls['V'] = Clock(self)
        self.ctrls['H'] = Clock(self)
        self.ctrls['H'].circle = 1000.0
        self.ctrls['C'] = Compass(self)

    def Layout(self) :
        margin = 60
        ahw = 320-2*margin
        rdir = 75
        if self.w > 320 :
            ahh = self.h - margin
        else :
            ahh = 512-68-margin-rdir*2
        self.ctrls['AH'].SetPosition(margin, margin, ahw, ahh)
        self.ctrls['V'].SetPosition(0, margin+ahh/2-margin/2, margin, margin)
        self.ctrls['H'].SetPosition(margin+ahw, margin+ahh/2-margin/2, margin, margin)

        if self.w > 320 :
            self.ctrls['C'].SetPosition(320, 0, self.w-320, self.h)
        else :
            self.ctrls['C'].SetPosition(0, margin+ahh, 320, self.h-margin-ahh)

    def Draw(self) :
        self.BeginDraw()

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
        rdir = 75
        if self.w > 320 :
            ahh = self.h - margin
        else :
            ahh = 512-68-margin-rdir*2

        gc = self.gc
        gc.SetFont(gc.font['default'])
        gc.DrawText(u'GS{:4.0f}\nM {:4.2f}\nα{:4.1f}\nG {:4.1f}'.format(VG,Ma,AoA,GLoad),2,margin+margin/2+ahh/2)
        gc.DrawText(u'{:5.0f}'.format(ROC),margin+ahw+2,margin+margin/2+ahh/2+5)
        if AGL > 0 :
            gc.DrawText(u'R{:4.0f}'.format(AGL),margin+ahw+2,margin+margin/2+ahh/2+20)

        gc.SetPen(gc.pen['white1'])
        if self.w > 320 :
            gc.DrawLines([(320,0),(320,self.h)])
        else :
            gc.DrawLines([(0,margin+ahh),(320,margin+ahh)])

        ah = self.ctrls['AH']
        ah.pitch = pitch
        ah.roll = roll
        ah.heading = heading
        ah.AoA=AoA
        ah.AoS=AoS

        self.ctrls['V'].val = VC
        self.ctrls['H'].val = ASL
        self.ctrls['C'].val = heading

        self.EndDraw()


