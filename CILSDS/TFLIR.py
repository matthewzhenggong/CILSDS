from Panel import Instrument
from Control import Control
from Buttons import *


class TFLIR(Instrument):

  def __init__(self, mgr):
    Instrument.__init__(self, None, mgr)
    self.ctrls['BtnCM'] = ButtonSwitch(self, 'MODE', ['A-A', 'A-S'])
    self.ctrls['BtnSYS'] = Button(self, 'SYSTEM')
    self.ctrls['BtnCNTL'] = Button(self, 'CNTL>')

    self.ctrls['BtnCAPTR'] = Button(self, 'CAPTR')

  def Layout(self):
    w = self.w
    h = self.h

    self.ctrls['BtnCM'].SetLeftTop(80, 2)
    self.ctrls['BtnSYS'].SetLeftTop(200, 2)
    self.ctrls['BtnCNTL'].SetRightTop(320, 2)

    self.ctrls['BtnCAPTR'].SetRightTop(w, 200)

  def DrawContent(self):
    gc = self.gc

    w = self.w
    h = self.h
    gc.Clip(0, 0, w, h)
    gc.SetBrush(gc.brush['ir_ground'])
    l = gc.CreatePath()
    l.AddRectangle(0, h * 0.7, w, h * 0.7)
    gc.FillPath(l)

    w2 = w / 2
    h2 = h / 2
    l = gc.CreatePath()
    l.MoveToPoint(w2 - h2 * 0.7, h2)
    l.AddLineToPoint(w2 - h2 * 0.1, h2)
    l.MoveToPoint(w2 + h2 * 0.7, h2)
    l.AddLineToPoint(w2 + h2 * 0.1, h2)
    l.MoveToPoint(w2, h2 + h2 * 0.7)
    l.AddLineToPoint(w2, h2 + h2 * 0.1)
    l.MoveToPoint(w2, h2 - h2 * 0.7)
    l.AddLineToPoint(w2, h2 - h2 * 0.1)
    gc.SetPen(gc.pen['green'])
    gc.StrokePath(l)
    gc.ResetClip()

    txt = 'IRST'
    gc.SetPen(gc.pen['white'])
    gc.SetFont(gc.font['white12'])
    gc.SetBrush(gc.brush['none'])
    te = gc.GetTextExtent(txt)
    gc.DrawRectangle(5 - 1, 150 - 1, te[0] + 2, te[1] + 2)
    gc.DrawText(txt, 5, 150)

  def DrawPreviewContent(self):
    self.DrawContent()
