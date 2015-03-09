
from Panel import Instrument
from Control import Control
from Buttons import *


class FUEL(Instrument) :
    def __init__(self, mgr) :
        Instrument.__init__(self, None, mgr)
        self.ctrls['BtnREFUEL'] = Button(self, 'REFUEL')
        self.ctrls['BtnCNTL'] = Button(self, 'CNTL>')

    def Layout(self) :
        w = self.w
        h = self.h

        self.ctrls['BtnREFUEL'].SetLeftTop(80,2)
        self.ctrls['BtnCNTL'].SetRightTop(320,2)

    def DrawContent(self) :
        gc = self.gc
        txt = 'GW: 48.4\nINLET: 43\nFED: 44'
        gc.SetFont(gc.font['default'])
        gc.DrawText(txt,10, 60)

    def DrawPreviewContent(self) :
        gc = self.gc
        txt = 'GW: 48.4\nINLET: 43\nFED: 44'
        gc.SetFont(gc.font['default'])
        gc.DrawText(txt,5,5)




