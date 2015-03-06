#!/bin/env python
# -*- coding: utf-8 -*-

from Control import Control
from Panel import Panel

class Recorder(Control) :
    def __init__(self, parent) :
        Control.__init__(self, parent)
        self.T = 0

    def RebuildPath(self) :
        if self.gc :
            gc = self.gc
            rec = gc.CreatePath()
            rec.AddRectangle(6,35,30,14)
            rec.MoveToPoint(36,38)
            rec.AddLineToPoint(46,35)
            rec.AddLineToPoint(46,47)
            rec.AddLineToPoint(36,45)
            rec.AddCircle(10,24,10)
            rec.AddCircle(30,24,10)
            self.rec = rec
            cyc = gc.CreatePath()
            cyc.MoveToPoint(-10,0)
            cyc.AddLineToPoint(10,0)
            cyc.MoveToPoint(0,-10)
            cyc.AddLineToPoint(0,10)
            self.cyc = cyc
        else :
            self.rec = None
            self.cyc = None

    def Draw(self) :
        self.BeginDraw()

        gc = self.gc
        gc.SetPen(gc.pen['green'])
        gc.SetFont(gc.font['green12'])
        gc.DrawText('RECORD',0,0)
        gc.DrawText('%05.0f'%self.T,0,49)
        gc.StrokePath(self.rec)

        gc.PushState()
        gc.Translate(10, 24)
        gc.Rotate(self.T)
        gc.StrokePath(self.cyc)
        gc.PopState()

        gc.PushState()
        gc.Translate(30, 24)
        gc.Rotate(self.T+0.785)
        gc.StrokePath(self.cyc)
        gc.PopState()

        self.EndDraw()


class Header2(Panel) :
    def __init__(self, mgr) :
        Panel.__init__(self, None, mgr)
        self.ctrls['R'] = Recorder(self)
        self.ctrls['R'].SetPosition(183, 0, 68,68)

    def Draw(self) :
        self.BeginDraw()

        self.ctrls['R'].T = self.mgr.data['T']

        gc = self.gc
        gc.DrawText('A  U  1\nB  V  1\nC  U  1',70,5)
        gc.DrawText('  CAS  42\n SCAS auto\nALCON  36',470,5)

        gc.PushState()
        gc.Translate(330, 6)
        gc.SetPen(gc.pen['green1'])
        gc.DrawLines([(0,0),(60,0)])
        gc.DrawLines([(0,10),(60,10)])
        gc.DrawLines([(0,20),(60,20)])
        gc.DrawLines([(0,30),(60,30)])
        gc.DrawLines([(0,40),(60,40)])
        gc.DrawLines([(0,50),(60,50)])
        gc.DrawLines([(0,0),(0,50)])
        gc.DrawLines([(10,0),(10,50)])
        gc.DrawLines([(20,0),(20,50)])
        gc.DrawLines([(30,0),(30,50)])
        gc.DrawLines([(40,0),(40,50)])
        gc.DrawLines([(50,0),(50,50)])
        gc.DrawLines([(60,0),(60,50)])
        gc.SetFont(gc.font['white20'])
        gc.DrawText('MENU',3,11)
        gc.PopState()

        self.EndDraw()


