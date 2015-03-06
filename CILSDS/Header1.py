#!/bin/env python
# -*- coding: utf-8 -*-

from Control import Control
from Panel import Panel
from math import pi

class Meter(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.heading = 3

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc
            r = self.h/2
            cyc1 = gc.CreatePath()
            cyc1.AddCircle(0, 0, r)
            cyc1.MoveToPoint(0, r)
            cyc1.AddLineToPoint(0, r+2)
            cyc1.MoveToPoint(0, -r)
            cyc1.AddLineToPoint(0, -r-2)
            cyc1.MoveToPoint(r, 0)
            cyc1.AddLineToPoint(r+2, 0)
            cyc1.MoveToPoint(-r, 0)
            cyc1.AddLineToPoint(-r-2, 0)
            self.cyc = cyc1

            arr1 = gc.CreatePath()
            arr1.MoveToPoint(0, 0)
            arr1.AddLineToPoint(0, -r)
            arr1.AddLineToPoint(2, -r*0.6)
            arr1.AddLineToPoint(-2, -r*0.6)
            arr1.AddLineToPoint(0, -r)
            self.arr = arr1
        else :
            self.cyc = None
            self.arr = None

    def Draw(self) :
        self.BeginDraw()

        gc = self.gc
        gc.SetPen(gc.pen['green'])
        gc.SetFont(gc.font['green12'])
        gc.Translate(self.w/2, self.h/2)
        gc.DrawPath(self.cyc)
        txt = '%03.0f'%self.heading
        te = gc.GetTextExtent(txt)
        r = self.h/2
        gc.DrawText(txt,-r-te[0],r-te[1]/2)
        gc.Rotate(self.heading/57.3)
        gc.DrawPath(self.arr)

        self.EndDraw()

class ThrottleMeter(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.throttle = 0
        self.fuelrate = 0

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc
            r = self.h/2
            cyc1 = gc.CreatePath()
            cyc1.AddArc(0,0,r,-pi*0.3,1.3*pi, True)
            cyc1.MoveToPoint(-r, 0)
            cyc1.AddLineToPoint(-r-2, 0)
            self.cyc = cyc1

            arr1 = gc.CreatePath()
            arr1.MoveToPoint(0, 0)
            arr1.AddLineToPoint(0, -r)
            arr1.AddLineToPoint(2, -r*0.6)
            arr1.AddLineToPoint(-2, -r*0.6)
            arr1.AddLineToPoint(0, -r)
            self.arr = arr1
        else :
            self.cyc = None
            self.arr = None

    def Draw(self) :
        self.BeginDraw()

        gc = self.gc
        gc.SetPen(gc.pen['green'])
        gc.Translate(self.w/2, self.h/2)
        gc.DrawPath(self.cyc)

        throttle = self.throttle
        if throttle < 0 :
            throttle = 0
        elif throttle > 1.3 :
            throttle = 1.3

        gc.SetFont(gc.font['green12'])
        txt = '%3.0f'%(throttle*100)
        te = gc.GetTextExtent(txt)
        r = self.h/2
        gc.DrawText(txt,-te[0]/2,-r-te[1]/2)

        gc.SetFont(gc.font['white12'])
        txt = '%3.0f'%(self.fuelrate)
        te = gc.GetTextExtent(txt)
        gc.DrawText(txt,-r*0.8-te[0],r*0.8)

        gc.Rotate(throttle*pi*1.3+0.2*pi)
        gc.DrawPath(self.arr)

        self.EndDraw()

class Header1(Panel) :
    def __init__(self, mgr) :
        Panel.__init__(self, None, mgr)
        #self.ctrls['M'] = Meter(self)
        self.ctrls['M'] = ThrottleMeter(self)
        self.ctrls['M'].SetPosition(76,10,40,40)

    def Draw(self) :
        self.BeginDraw()

        heading=self.mgr.data['heading']
        lat=self.mgr.data['lat']
        lon=self.mgr.data['lon']
        vel=self.mgr.data['VG']
        throttle=self.mgr.data['throttle']
        fuelrate=self.mgr.data['fuelrate']

        #self.ctrls['M'].heading = heading
        self.ctrls['M'].throttle = throttle
        self.ctrls['M'].fuelrate = fuelrate

        gc = self.gc
        gc.SetPen(gc.pen['green'])
        gc.DrawSymAC(gc,292,35,21,30)

        gc.SetFont(gc.font['green12'])
        gc.DrawText('ICAWS',360,20)
        gc.DrawText('AP',579,11)
        gc.DrawText('AT',579,35)

        txt = 'GSLONG%7.1f\n GSLAT%7.1f\n GSSPD%7.1f'%(lon,lat,vel)
        gc.DrawText(txt,128,6)

        self.EndDraw()


