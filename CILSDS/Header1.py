#!/bin/env python
# -*- coding: utf-8 -*-

from Control import Control
from Panel import Instrument
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

    def DrawContent(self) :
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

    def DrawContent(self) :
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

class SMS(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.sms = None

    def DrawContent(self) :
        if self.sms :
            sms = self.sms
            pylons = sms['pylons']
            mrm = len(pylons['MRM'])
            srm = len(pylons['SRM'])
            gun = sms['GUN']
            a2s  = len(pylons['AS'])
            chat = sms['CHAT']
            flat = sms['FLAT']

            rdy = pylons['RDY']

            gc = self.gc

            flag = True
            gc.SetPen(gc.pen['white'])
            gc.SetBrush(gc.brush['none'])
            for i in pylons['MRM'] :
                if rdy == i[1] :
                    gc.SetFont(gc.font['white10'])
                    txt = '%1d MRM'%(mrm)
                    te = gc.GetTextExtent(txt)
                    gc.DrawRectangle(0-1,3-1,te[0]+2,te[1]+2)
                    gc.DrawText(txt,0,3)
                    flag = False
                    break
            if flag :
                gc.SetFont(gc.font['green10'])
                txt = '%1d MRM'%(mrm)
                gc.DrawText(txt,0,3)

            flag = True
            for i in pylons['SRM'] :
                if rdy == i[1] :
                    gc.SetFont(gc.font['white10'])
                    txt = '%1d SRM'%(srm)
                    te = gc.GetTextExtent(txt)
                    gc.DrawRectangle(0-1,3+15-1,te[0]+2,te[1]+2)
                    gc.DrawText(txt,0,3+15)
                    flag = False
                    break
            if flag :
                gc.SetFont(gc.font['green10'])
                txt = '%1d SRM'%(srm)
                gc.DrawText(txt,0,3+15)

            flag = True
            for i in pylons['AS'] :
                if rdy == i[1] :
                    gc.SetFont(gc.font['white10'])
                    txt = '%1d AS'%(a2s)
                    te = gc.GetTextExtent(txt)
                    gc.DrawRectangle(0-1,3+45-1,te[0]+2,te[1]+2)
                    gc.DrawText(txt,0,3+45)
                    flag = False
                    break
            if flag :
                gc.SetFont(gc.font['green10'])
                txt = '%1d AS'%(a2s)
                gc.DrawText(txt,0,3+45)

            gc.SetFont(gc.font['green10'])
            txt = '%3dGUN'%gun
            gc.DrawText(txt,0,3+30)

            gc.SetFont(gc.font['white10'])
            txt = '%2d\n%2d'%(chat,flat)
            gc.DrawText(txt,40,3)

class Header1(Instrument) :
    def __init__(self, mgr) :
        Instrument.__init__(self, None, mgr)
        self.get_active = False
        #self.ctrls['M'] = Meter(self)
        self.ctrls['M'] = ThrottleMeter(self)
        self.ctrls['M'].SetPosition(76,10,40,40)
        self.ctrls['S'] = SMS(self)
        self.ctrls['S'].SetPosition(200,0,60,68)

    def DrawContent(self) :
        #heading=self.mgr.data['heading']
        throttle=self.mgr.data['throttle']
        fuelrate=self.mgr.data['fuelrate']

        sms = self.mgr.data['SMS']

        #self.ctrls['M'].heading = heading
        self.ctrls['M'].throttle = throttle
        self.ctrls['M'].fuelrate = fuelrate
        self.ctrls['S'].sms = sms

        gc = self.gc
        gc.SetPen(gc.pen['green'])
        gc.DrawSymAC(gc,292,35,21,30)

        gc.SetFont(gc.font['cyan12'])
        try :
            gc.DrawText(self.mgr.data['NAV']['MODE'],360,20)
        except :
            gc.DrawText('ICAWS',360,20)
        try :
            if self.mgr.data['NAV']['AP'] > 0.5 :
                gc.DrawText('AP',579,11)
        except :
            gc.DrawText('MA',579,11)
        try :
            if self.mgr.data['NAV']['PF'] > 0.5 :
                gc.DrawText('PF',579,35)
        except :
            pass

        gc.SetFont(gc.font['green10'])
        gc.DrawText('  10 0\nI 10 0\nE  0 0',125,10)

        gc.SetPen(gc.pen['none'])
        gc.SetBrush(gc.brush['blue'])

        fuel_per = 0.95
        gc.DrawRectangle(170,6+60*(1-fuel_per),20,60*fuel_per)
        gc.SetPen(gc.pen['black'])
        gc.StrokeLine(170,6+12,190,6+12)
        gc.StrokeLine(170,6+24,190,6+24)
        gc.StrokeLine(170,6+36,190,6+36)
        gc.StrokeLine(170,6+48,190,6+48)

