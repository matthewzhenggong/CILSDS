#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Panel
from Control import Control

class WeaponManager(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.chat = 0
        self.flat = 0
        self.pylon = [ \
                ['sm',-148,-10],
                ['mm',-110,-20],
                ['mm',-90,-20],
                ['sm',-30,-20],
                ['mm',-15,-20],
                ['', 0, -20],
                ['mm', 15,-20],
                ['sm', 30,-20],
                ['mm', 90,-20],
                ['mm', 110,-20],
                ['sm',148,-10] ]

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

            self.wps = {'sm':sm, 'mm':mm}
        
        else :
            self.ac = None
            self.wps = None
        
    def Draw(self) :
        self.BeginDraw()

        gc = self.gc

        gc.PushState()
        gc.SetPen(gc.pen['green'])
        gc.Translate(164,113)
        gc.DrawPath(self.ac)

        gc.SetBrush(gc.brush['green'])

        gc.SetFont(gc.font['green12'])
        for idx,i in enumerate(self.pylon) :
            if i[0] in self.wps :
                gc.PushState()
                gc.Translate(i[1],i[2])
                gc.DrawPath(self.wps[i[0]])
                txt = str(idx+1)
                te = gc.GetTextExtent(txt)
                gc.DrawText(txt, -te[0]/2, -40-te[1])
                gc.PopState()


        gc.SetPen(gc.pen['white'])
        gc.SetBrush(gc.brush['back'])
        gc.DrawRectangle(-45,75,90,90)
        gc.SetFont(gc.font['white12'])
        gc.DrawText('CHAT{:3d}\nFLAT{:3d}'.format(self.chat,self.flat),-26,80)

        gc.PopState()

        self.EndDraw()

class SMS(Panel) :
    def __init__(self, mgr) :
        Panel.__init__(self, None, mgr)
        self.ctrls['WM'] = WeaponManager(self)
        self.ctrls['WM'].SetPosition(0,0,320,320)

    def Layout(self) :
        pass

    def Draw(self) :
        self.BeginDraw()
        self.EndDraw()

