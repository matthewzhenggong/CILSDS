from Control import Control
from Panel import Instrument
from math import pi


class Display(Control):

  def __init__(self, parent, title, cur_val, length=50):
    Control.__init__(self, parent)
    self.title = title
    self.cur_val = cur_val
    self.length = length

  def DrawContent(self):
    gc = self.gc

    gc.SetFont(gc.font['green12'])
    gc.SetPen(gc.pen['green'])
    gc.SetBrush(gc.brush['back'])

    te = gc.GetTextExtent(self.title)
    gc.DrawText(self.title, 0, 0)
    gc.DrawRectangle(te[0] + 3, -1, self.length, te[1] + 2)
    txt = '%.0f' % self.cur_val
    te2 = gc.GetTextExtent(txt)
    gc.DrawText(txt, te[0] + 4 + self.length - te2[0], 0)


class Meter(Control):

  def __init__(self, parent, title, cur_val, min_val, max_val, aug_val):
    Control.__init__(self, parent)
    self.title = title
    self.cur_val = cur_val
    self.min_val = min_val
    self.max_val = max_val
    self.aug_val = aug_val
    self.w = 60
    self.h = 75

  def RebuildPath(self):
    if self.gc:
      gc = self.gc
      r = (self.h - 15) / 2
      cyc1 = gc.CreatePath()
      cyc1.AddArc(0, 0, r, -pi * 0.3, 1.3 * pi, True)
      cyc1.MoveToPoint(-r, 0)
      cyc1.AddLineToPoint(-r - 4, 0)
      self.cyc = cyc1

      arr1 = gc.CreatePath()
      arr1.MoveToPoint(0, 0)
      arr1.AddLineToPoint(0, -r)
      arr1.AddLineToPoint(2, -r * 0.6)
      arr1.AddLineToPoint(-2, -r * 0.6)
      arr1.AddLineToPoint(0, -r)
      self.arr = arr1
    else:
      self.cyc = None
      self.arr = None

  def DrawContent(self):
    gc = self.gc
    gc.SetPen(gc.pen['green'])
    r = (self.h - 20) / 2
    gc.Translate((self.w - 4) / 2 + 4, r + 5)
    gc.DrawPath(self.cyc)

    val = self.cur_val
    if val < self.min_val:
      val = self.min_val
    elif val > self.aug_val:
      val = self.aug_val

    if val <= self.max_val:
      val = (val - self.min_val) / float(self.max_val - self.min_val)
    else:
      val = 1 + 0.3 / 1.3 * (val - self.max_val) / float(self.aug_val - self.
                                                         max_val)

    gc.SetFont(gc.font['green12'])
    txt = '%3.0f' % (self.cur_val)
    te = gc.GetTextExtent(txt)
    gc.DrawText(txt, -te[0] / 2, -r - te[1] / 2)

    te = gc.GetTextExtent(self.title)
    gc.DrawText(self.title, -te[0] / 2, r + 2)

    gc.Rotate(val * pi * 1.3 + 0.2 * pi)
    gc.DrawPath(self.arr)


class ENG(Instrument):

  def __init__(self, mgr):
    Instrument.__init__(self, None, mgr)
    self.ctrls['FF'] = Display(self, 'FF', 0)
    self.ctrls['thrust'] = Meter(self, 'THRUST', 90, 0, 100, 130)
    self.ctrls['egt'] = Meter(self, 'EGT', 816, 0, 1000, 1300)
    self.ctrls['nozzle'] = Meter(self, 'NOZZLE', 72, 0, 100, 130)
    self.ctrls['n2'] = Meter(self, 'N2', 92, 0, 100, 130)
    self.ctrls['oil'] = Meter(self, 'OIL', 60, 0, 100, 130)
    self.ctrls['A'] = Display(self, 'HYD A', 4000)
    self.ctrls['B'] = Display(self, 'HYD B', 4000)

  def Layout(self):
    w = self.w
    h = self.h

    self.ctrls['FF'].SetLeftTop(10, 165)
    self.ctrls['thrust'].SetLeftTop(50, 80)
    self.ctrls['egt'].SetLeftTop(130, 80)
    self.ctrls['nozzle'].SetLeftTop(210, 80)
    self.ctrls['n2'].SetLeftTop(130, 250)
    self.ctrls['oil'].SetLeftTop(210, 250)
    self.ctrls['A'].SetLeftTop(10, 265)
    self.ctrls['B'].SetLeftTop(10, 290)

  def DrawContent(self):
    throttle = self.mgr.data['throttle']
    fuelrate = self.mgr.data['fuelrate']

    self.ctrls['thrust'].cur_val = throttle * 100
    self.ctrls['FF'].cur_val = fuelrate

  def DrawPreviewContent(self):
    self.DrawContent()
    gc = self.gc
    gc.PushState()
    gc.Translate((self.w - 70) / 2, 5)
    self.ctrls['thrust'].DrawContent()
    gc.PopState()
