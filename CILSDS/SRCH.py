
from Panel import Instrument
from Control import Control
from Buttons import *


class SRCH(Instrument) :
    def __init__(self, mgr) :
        Instrument.__init__(self, None, mgr)
        self.ctrls['BtnOPER'] = Button(self, 'OPER')
        self.ctrls['BtnCNTL'] = Button(self, 'CNTL>')

    def Layout(self) :
        w = self.w
        h = self.h

        self.ctrls['BtnOPER'].SetLeftTop(80,2)
        self.ctrls['BtnCNTL'].SetRightTop(320,2)

    def DrawContent(self) :
        gc = self.gc
        txt = 'AA A\n   P\nAS A\n   P'
        gc.SetFont(gc.font['default'])
        gc.DrawText(txt,10, 60)

    def DrawPreviewContent(self) :
        gc = self.gc
        txt = 'AA A\n   P\nAS A\n   P'
        gc.SetFont(gc.font['default'])
        gc.DrawText(txt,5,5)



