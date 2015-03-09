
from Panel import Instrument
from Control import Control
from Buttons import *


class TWD(Instrument) :
    def __init__(self, mgr) :
        Instrument.__init__(self, None, mgr)
        self.ctrls['BtnOPER'] = Button(self, 'OPER')
        self.ctrls['BtnCM'] = ButtonSwitch(self, 'MODE', ['SEMI', 'ACTI'])
        self.ctrls['BtnCNTL'] = Button(self, 'CNTL>')

        self.ctrls['BtnDCLT'] = Button(self, 'DCLT')

        self.ctrls['BtnSEP'] = Button(self, 'SEP')

        self.ctrls['BtnRWSS'] = ButtonSwitch(self, 'RW SS', ['AS1', 'AS2'])
        self.ctrls['BtnHSSS'] = ButtonSwitch(self, 'HS SS', ['WB', 'COL'])

    def Layout(self) :
        w = self.w
        h = self.h

        self.ctrls['BtnOPER'].SetLeftTop(80,2)
        self.ctrls['BtnCM'].SetLeftTop(200,2)
        self.ctrls['BtnCNTL'].SetRightTop(320,2)

        self.ctrls['BtnDCLT'].SetRightTop(w,200)

        self.ctrls['BtnRWSS'].SetLeftTop(2,50)
        self.ctrls['BtnHSSS'].SetLeftTop(2,100)
        self.ctrls['BtnSEP'].SetLeftTop(2,150)

    def DrawContent(self) :
        gc = self.gc

        w = self.w
        h = self.h
        w2 = w/2
        h2 = h/2
        l = gc.CreatePath()
        l.AddCircle(w2,h2,h2*0.7)
        l.AddCircle(w2,h2,h2*0.4)
        l.AddCircle(w2,h2,h2*0.1)
        l.MoveToPoint(w2-h2*0.7,h2)
        l.AddLineToPoint(w2-h2*0.1,h2)
        l.MoveToPoint(w2+h2*0.7,h2)
        l.AddLineToPoint(w2+h2*0.1,h2)
        l.MoveToPoint(w2,h2+h2*0.7)
        l.AddLineToPoint(w2,h2+h2*0.1)
        l.MoveToPoint(w2,h2-h2*0.7)
        l.AddLineToPoint(w2,h2-h2*0.1)
        gc.SetPen(gc.pen['green'])
        gc.StrokePath(l)

    def DrawPreviewContent(self) :
        self.DrawContent()


