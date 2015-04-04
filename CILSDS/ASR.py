from Panel import Instrument
from Control import Control
from Buttons import *


class ASR(Instrument):

  def __init__(self, mgr):
    Instrument.__init__(self, None, mgr)
    self.ctrls['BtnMODE'] = ButtonSwitch(self, 'MODE', ['SAR', 'SCAN'])
    self.ctrls['BtnBLANK'] = Button(self, 'BLANK')
    self.ctrls['BtnCNTL'] = Button(self, 'CNTL>')

    self.ctrls['BtnDvRLAY'] = ButtonSwitch(self, 'DvRLAY', ['OFF', 'ON'], True)
    self.ctrls['BtnAFS'] = ButtonSwitch(self, 'AFS', ['1', '2', '3', '4'])

  def Layout(self):
    w = self.w
    h = self.h

    self.ctrls['BtnMODE'].SetLeftTop(80, 2)
    self.ctrls['BtnBLANK'].SetLeftTop(200, 2)
    self.ctrls['BtnCNTL'].SetRightTop(320, 2)

    self.ctrls['BtnDvRLAY'].SetRightTop(w, 200)

    self.ctrls['BtnAFS'].SetLeftBottom(2, 330)

  def DrawContent(self):
    gc = self.gc
    txt = 'NO IMAGE'
    gc.SetFont(gc.font['default'])
    te = gc.GetTextExtent(txt)
    gc.DrawText(txt, (self.w - te[0]) / 2, (self.h - te[1]) / 2)

  def DrawPreviewContent(self):
    self.DrawContent()
