#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Instrument
from Control import Control
from Buttons import *

from math import pi,sin

class WeaponManager(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.sms = None
        self.pylon = [ \
                ['sm',-148,-10, '', -20],
                ['mm',-110,-20, '', -9],
                ['mm',-90,-20, '', -9],
                ['sm',-30,-20, '', 9],
                ['mm',-15,-20, '', 9],
                ['', 0, -20, '', 9],
                ['mm', 15,-20, '', 9],
                ['sm', 30,-20, '', 9],
                ['mm', 90,-20, '', -9],
                ['mm', 110,-20, '', -9],
                ['sm',148,-10, '', -20] ]

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc

            ac = gc.CreatePath()
            ac.MoveToPoint(-50.9243,-113.466235)
            ac.AddLineToPoint(-78.945425,-53.955798)
            ac.AddLineToPoint(-146.141815,-24.372455)
            ac.AddLineToPoint(-145.84051,37.465255)
            ac.AddLineToPoint(-66.29135,70.037055)
            
            ac.MoveToPoint(50.9243,-113.466235)
            ac.AddLineToPoint(78.945425,-53.955798)
            ac.AddLineToPoint(146.141815,-24.372455)
            ac.AddLineToPoint(145.84051,37.465255)
            ac.AddLineToPoint(66.29135,70.037055)
            
            ac.MoveToPoint(-75.93566,91.979915)
            ac.AddLineToPoint(-110.58905,117.906115)
            ac.AddLineToPoint(-110.28548,145.167205)
            ac.AddLineToPoint(-28.92615,169.77231)
            ac.AddLineToPoint(-17.173765,113.57904)
            ac.AddLineToPoint(0,113.57904)
            
            ac.MoveToPoint(75.93566,91.979915)
            ac.AddLineToPoint(110.58905,117.906115)
            ac.AddLineToPoint(110.28548,145.167205)
            ac.AddLineToPoint(28.92615,169.77231)
            ac.AddLineToPoint(17.173765,113.57904)
            ac.AddLineToPoint(0,113.57904)
            
            ac.MoveToPoint(-41.280025,42.778475)
            ac.AddLineToPoint(-75.935665,83.338255)
            ac.AddLineToPoint(-75.0306,124.89296)
            ac.AddLineToPoint(-24.710025,91.97992)
            ac.AddLineToPoint(-41.280025,42.778475)
            
            ac.MoveToPoint(41.280025,42.778475)
            ac.AddLineToPoint(75.935665,83.338255)
            ac.AddLineToPoint(75.0306,124.89296)
            ac.AddLineToPoint(24.710025,91.97992)
            ac.AddLineToPoint(41.280025,42.778475)
            
            ac.MoveToPoint(-75.93225,107.6059)
            ac.AddLineToPoint(-29.830095,76.02523)
            
            ac.MoveToPoint(75.93225,107.6059)
            ac.AddLineToPoint(29.830095,76.02523)
            
            ac.MoveToPoint(-83.767545,-51.6310325)
            ac.AddLineToPoint(-83.16721,-44.316745)
            ac.AddLineToPoint(-145.539215,-15.065865)
            
            ac.MoveToPoint(83.767545,-51.6310325)
            ac.AddLineToPoint(83.16721,-44.316745)
            ac.AddLineToPoint(145.539215,-15.065865)
            
            ac.MoveToPoint(-130.473475,42.78098)
            ac.AddLineToPoint(-130.173305,21.16934)
            ac.AddLineToPoint(-66.89624,36.797815)
            ac.AddLineToPoint(-67.1964,71.040725)
            
            
            ac.MoveToPoint(130.473475,42.78098)
            ac.AddLineToPoint(130.173305,21.16934)
            ac.AddLineToPoint(66.89624,36.797815)
            ac.AddLineToPoint(67.1964,71.040725)

            self.ac = ac

            ac = gc.CreatePath()
            ac.MoveToPoint(-60,-12)
            ac.AddLineToPoint(0,0)
            ac.AddLineToPoint(60,-12)
            ac.AddLineToPoint(64,-17)
            ac.AddLineToPoint(146,-20)
            ac.AddLineToPoint(146,-22)
            ac.AddLineToPoint(62,-26)
            ac.MoveToPoint(-60,-12)
            ac.AddLineToPoint(-64,-17)
            ac.AddLineToPoint(-146,-20)
            ac.AddLineToPoint(-146,-22)
            ac.AddLineToPoint(-62,-26)
            #ac.MoveToPoint(0,0)
            #ac.AddLineToPoint(0,21)
            ac.MoveToPoint(-51,-10)
            ac.AddLineToPoint(-41,14)
            ac.AddLineToPoint(-34,21)
            ac.AddLineToPoint(34,21)
            ac.AddLineToPoint(41,14)
            ac.AddLineToPoint(51,-10)
            ac.MoveToPoint(-62,-26)
            ac.AddCurveToPoint(-40,-31,  -13,-44, 0,-44)
            ac.MoveToPoint(62,-26)
            ac.AddCurveToPoint(40,-31,  13,-44, 0,-44)
            self.acx = ac

            ac = gc.CreatePath()
            ac.MoveToPoint(-41+41,14-14)
            ac.AddLineToPoint(-34+41,21-14)
            ac.AddLineToPoint(0+41,21-14)
            self.door_left = ac

            ac = gc.CreatePath()
            ac.MoveToPoint(41-41,14-14)
            ac.AddLineToPoint(34-41,21-14)
            ac.AddLineToPoint(0-41,21-14)
            self.door_right = ac

            sm = gc.CreatePath()
            sm.MoveToPoint(0,-25)
            sm.AddLineToPoint(-3,-11)
            sm.AddLineToPoint(-1,-11)
            sm.AddLineToPoint(-1,46)
            sm.AddLineToPoint(-5,54)
            sm.AddLineToPoint(0,52)
            sm.AddLineToPoint(5,54)
            sm.AddLineToPoint(1,46)
            sm.AddLineToPoint(1,-11)
            sm.AddLineToPoint(3,-11)
            sm.AddLineToPoint(0,-25)

            smx = gc.CreatePath()
            smx.AddCircle(0,0,2)
            smx.MoveToPoint(-5,-5)
            smx.AddLineToPoint(5,5)
            smx.MoveToPoint(5,-5)
            smx.AddLineToPoint(-5,5)

            mm = gc.CreatePath()
            mm.MoveToPoint(0,-31)
            mm.AddLineToPoint(-2,-27)
            mm.AddLineToPoint(-2,10)
            mm.AddLineToPoint(-6,16)
            mm.AddLineToPoint(-2,16)
            mm.AddLineToPoint(-2,49)
            mm.AddLineToPoint(-7,57)
            mm.AddLineToPoint(0,55)
            mm.AddLineToPoint(7,57)
            mm.AddLineToPoint(2,49)
            mm.AddLineToPoint(2,16)
            mm.AddLineToPoint(6,16)
            mm.AddLineToPoint(2,10)
            mm.AddLineToPoint(2,-27)
            mm.AddLineToPoint(0,-31)

            mmx = gc.CreatePath()
            mmx.AddCircle(0,0,3)
            mmx.MoveToPoint(-6,-6)
            mmx.AddLineToPoint(6,6)
            mmx.MoveToPoint(6,-6)
            mmx.AddLineToPoint(-6,6)

            self.wps = {'sm':[sm,smx], 'mm':[mm,mmx]}
        
        else :
            self.ac = None
            self.wps = None
            self.acx = None
            self.door_left = None
            self.door_right = None
        
    def drawContent(self, preview) :
        if not self.sms :
            return

        gc = self.gc

        gc.PushState()
        gc.SetPen(gc.pen['green'])
        gc.Translate(164,113)
        gc.StrokePath(self.ac)

        pylons = self.sms['pylons']
        firing = pylons['firing']
        if firing < 0 :
            firing = 0
        elif firing > 100 :
            firing = 100
        door_pos = sin(firing/100.0*pi)

        if self.h > 380 and not preview :
            gc.PushState()
            gc.Translate(0,250)
            gc.SetPen(gc.pen['green'])
            gc.StrokePath(self.acx)

            gc.SetPen(gc.pen['white'])
            gc.PushState()
            gc.Translate(-41,14)
            gc.Rotate(1.6*door_pos)
            gc.StrokePath(self.door_left)
            gc.PopState()
            gc.PushState()
            gc.Translate(41,14)
            gc.Rotate(-1.6*door_pos)
            gc.StrokePath(self.door_right)
            gc.PopState()

            gc.PopState()

        for i in self.pylon :
            i[0] = ''
        for i in pylons['MRM'] :
            self.pylon[i[1]-1][0] = 'mm'
            self.pylon[i[1]-1][3] = i[0]
        for i in pylons['SRM'] :
            self.pylon[i[1]-1][0] = 'sm'
            self.pylon[i[1]-1][3] = i[0]
        for i in pylons['AS'] :
            self.pylon[i[1]-1][0] = 'as'
            self.pylon[i[1]-1][3] = i[0]

        gc.SetPen(gc.pen['green'])
        gc.SetBrush(gc.brush['green'])
        gc.SetFont(gc.font['green12'])
        for idx,i in enumerate(self.pylon) :
            if i[0] in self.wps and idx+1 != pylons['RDY'] :
                gc.PushState()
                gc.Translate(i[1],i[2])
                gc.DrawPath(self.wps[i[0]][0])
                txt = str(idx+1)
                te = gc.GetTextExtent(txt)
                gc.DrawText(txt, -te[0]/2, -40-te[1])
                gc.PopState()
                if self.h > 380 and not preview :
                    gc.PushState()
                    gc.Translate(i[1],250+i[4])
                    gc.DrawPath(self.wps[i[0]][1])
                    gc.DrawText(txt, -te[0]/2, -10-te[1])
                    gc.PopState()

        notice = 'NO WPN SELECTED'
        if pylons['RDY']>0 and pylons['RDY']<12 :
            i = self.pylon[pylons['RDY']-1]
            if int(pylons['firing']/10)%2 :
                gc.SetPen(gc.pen['white'])
                gc.SetBrush(gc.brush['white'])
                gc.SetFont(gc.font['white12'])
                gc.PushState()
                gc.Translate(i[1],i[2])
                gc.DrawPath(self.wps[i[0]][0])
                txt = str(pylons['RDY'])
                te = gc.GetTextExtent(txt)
                gc.DrawText(txt, -te[0]/2, -40-te[1])
                gc.PopState()
                if self.h > 380 and not preview :
                    gc.PushState()
                    gc.Translate(i[1],250+i[4])
                    gc.DrawPath(self.wps[i[0]][1])
                    gc.DrawText(txt, -te[0]/2, -10-te[1])
                    gc.PopState()
            if pylons['firing'] > 0 :
                notice = 'STAS %s-REL'%(i[3])
            else :
                notice = 'STAS %s-RDY'%(i[3])

        if not preview :
            chat = self.sms['CHAT']
            flat = self.sms['FLAT']

            gc.SetPen(gc.pen['white'])
            gc.SetBrush(gc.brush['tab'])
            gc.DrawRectangle(-45,75,90,90)
            gc.SetFont(gc.font['white12'])
            gc.DrawText('CHAT{:3d}\nFLAT{:3d}'.format(chat,flat),-26,80)

        gc.SetFont(gc.font['white20'])
        gc.SetPen(gc.pen['white'])
        gc.SetBrush(gc.brush['tab'])
        te = gc.GetTextExtent(notice)
        gc.DrawRectangle((-te[0])/2-1,40-1,te[0]+2,te[1]+2)
        gc.DrawText(notice,(-te[0])/2,40)

        gc.PopState()

    def DrawContent(self) :
        self.drawContent(False)

    def DrawPreview(self) :
        self.gc.PushState()
        self.gc.Scale(0.5,0.5)
        self.drawContent(True)
        self.gc.PopState()

    def OnClick(self, x, y) :
        if self.visable :
            x -= self.x
            y -= self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                if abs(x-164) < 45 and abs(y-113-40-10) < 10 :
                    self.parent.mgr.PushMessage({'name':'release', 'weapon':"missile"})
                if x-164 < 45 and x-164 > 0 and abs(y-113-75-45) < 45 :
                    self.parent.mgr.PushMessage({'name':'release', 'weapon':"flat"})
                if x-164 >-45 and x-164 < 0 and abs(y-113-75-45) < 45 :
                    self.parent.mgr.PushMessage({'name':'release', 'weapon':"chat"})
                if self.click_func :
                    self.click_func(ClickEvent(self,x,y))
        return False

class Doors(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.w = 50
        self.h = 50
        self.sms = None

    def DrawContent(self) :
        if self.sms :
            sms = self.sms
            pylons = sms['pylons']
            firing = pylons['firing']

            gc = self.gc

            gc.SetFont(gc.font['button'])
            txt = 'DOORS'
            gc.DrawText(txt,5,0)

            txt = 'OPEN'
            if firing > 0 and firing <100 :
                gc.SetPen(gc.pen['white'])
                gc.SetFont(gc.font['white12'])
                gc.SetBrush(gc.brush['none'])
                te = gc.GetTextExtent(txt)
                gc.DrawRectangle(5-1,18-1,te[0]+2,te[1]+2)
                gc.DrawText(txt,5,18)
            else :
                gc.SetFont(gc.font['button'])
                gc.DrawText(txt,5,18)

            txt = 'CLOSED'
            if firing > 0 and firing <100 :
                gc.SetFont(gc.font['button'])
                gc.DrawText(txt,5,30)
            else :
                gc.SetPen(gc.pen['white'])
                gc.SetFont(gc.font['white12'])
                gc.SetBrush(gc.brush['none'])
                te = gc.GetTextExtent(txt)
                gc.DrawRectangle(5-1,36-1,te[0]+2,te[1]+2)
                gc.DrawText(txt,5,36)


class SMS(Instrument) :
    def __init__(self, mgr) :
        Instrument.__init__(self, None, mgr)
        self.ctrls['BtnETOPT'] = ButtonSwitch(self, 'ET OPT', ['OFF', 'ON'], align_right=True)
        self.ctrls['BtnETRUN'] = Button(self, 'ET RUN')
        self.ctrls['DOORS'] = Doors(self)
        self.ctrls['WM'] = WeaponManager(self)

    def Layout(self) :
        self.ctrls['WM'].SetPosition((self.w-320)/2,0,320,self.h)
        self.ctrls['BtnETOPT'].SetRightTop(self.w,180)
        self.ctrls['BtnETRUN'].SetRightTop(self.w,270)
        self.ctrls['DOORS'].SetLeftTop(0,170)

    def DrawContent(self) :

        sms = self.mgr.data['SMS']

        self.ctrls['WM'].sms = sms
        self.ctrls['DOORS'].sms = sms

    def DrawPreviewContent(self) :
        sms = self.mgr.data['SMS']
        self.ctrls['WM'].sms = sms

        self.ctrls['WM'].DrawPreview()

