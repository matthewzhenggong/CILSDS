
#!/bin/env python
# -*- coding: utf-8 -*-

from Buttons import *
from Panel import Panel

class HeadPanel(Panel) :
    def __init__(self, parent, mgr, title) :
        Panel.__init__(self, parent, mgr)
        self.SetTitle(title)

    def SetTitle(self, title) :
        self.title = title

class BodyPanel(Panel) :
    def __init__(self, parent, mgr, title) :
        Panel.__init__(self, parent, mgr)
        self.SetTitle(title)
        self.ctrls['menu'] = ButtonTitle(self)

        self.ctrls['menu'].SetClickFunc(self.parent.ShowMenu)

    def SetTitle(self, title) :
        self.title = title
        if title in self.mgr.body_panels :
           self.panels = [self.mgr.body_panels[self.title]]
           self.panels[0].SetPosition(0,0, self.w, self.h)
        else :
           self.panels = []

    def Layout(self) :
        if len(self.panels) :
            self.panels[0].SetPosition(0,0, self.w, self.h)
        self.ctrls['menu'].SetLeftTop(0,0)
        Panel.Layout(self)

    def Draw(self) :
        if self.visable and len(self.panels) :
            self.panels[0].SetPosition(0,0, self.w, self.h)
            self.panels[0].Layout()
            self.BeginDraw(drawBoarder=False)
            self.EndDraw()
        else :
            Panel.Draw(self)

class MiniPanel(Panel) :
    def __init__(self, parent, mgr, title, upper) :
        Panel.__init__(self, parent, mgr)
        self.upper = upper
        self.SetTitle(title)

    def SetTitle(self, title) :
        self.title = title
        if title in self.mgr.mini_panels :
           self.panels = [self.mgr.mini_panels[self.title]]
           self.panels[0].SetPosition(0,0, self.w, self.h)
        else :
           self.panels = []

    def Layout(self) :
        if len(self.panels) :
            self.panels[0].SetPosition(0,0, self.w, self.h)
        Panel.Layout(self)

    def Draw(self) :
        if self.visable and len(self.panels) :
            self.panels[0].SetPosition(0,0, self.w, self.h)
            self.panels[0].Layout()
            self.BeginDraw(drawBoarder=False)
            self.EndDraw()
        else :
            Panel.Draw(self)

    def OnClick(self, x, y) :
        if self.visable:
            x = x - self.x
            y = y - self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                if self.upper.visable :
                    name = self.upper.title
                    self.upper.SetTitle(self.title)
                    self.SetTitle(name)
                elif self.parent.panel_left.visable :
                    name = self.parent.panel_left.title
                    self.parent.panel_left.SetTitle(self.title)
                    self.SetTitle(name)
                elif self.parent.panel_right.visable :
                    name = self.parent.panel_right.title
                    self.parent.panel_right.SetTitle(self.title)
                    self.SetTitle(name)
                return True
        return False

class MenuPanel(Panel) :
    def __init__(self, parent, mgr) :
        Panel.__init__(self, parent, mgr)
        self.items = ['ASR>','CKLST>','CNI>','DAS>','DTM>', \
                      'EFI>', 'ENG>', 'FCS>', 'FTA>','FTI>', \
                      'FUEL>', 'HUD>', 'ICAWS>', 'PHD>', 'SMS>', \
                      'SRCH>', 'TFLIR>', 'TSD-1>', 'TSD-2>', 'TSD-3>', \
                      'TWD>', 'WPN-A>', 'WPN-S>']
        self.pt = (-1,-1)

    def Layout(self) :
        Panel.Layout(self)
        self.pt = (-1,-1)

    def OnClick(self, x, y) :
        if self.visable:
            x = x - self.x
            y = y - self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                self.parent.ShowingMenu = False
                for idx,item in enumerate(self.marks) :
                    row = idx / 5
                    cow = idx % 5
                    if x>=item[0] and x < item[1] \
                        and y>= item[2] and y < item[3] :
                        self.MenuCtrl.parent.SetTitle(item[4][:-1])
                        break
                return True
        return False

    def OnTouch(self, x, y) :
        rslt = False
        if self.visable:
            x = x - self.x
            y = y - self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                self.mgr.ActivePanel = self
                self.pt = (x,y)
                rslt = True
        return rslt

    def Draw(self) :
        if self.visable:
            self.BeginDraw()

            gc = self.gc
            gc.SetFont(gc.font['menu_title'])
            tt = self.MenuCtrl.parent.title
            te = gc.GetTextExtent(tt)
            gc.DrawText(tt, (self.MenuCtrl.w-te[0])/2, (self.MenuCtrl.h-te[1])/2)
            gc.SetFont(gc.font['menu_subtitle'])
            gc.DrawText('MENU', 10, self.MenuCtrl.h)
            gc.DrawText('POPUP', 8, self.MenuCtrl.h+te[1])
            gc.SetFont(gc.font['menu_text'])

            self.marks = []
            for idx,item in enumerate(self.items) :
                row = idx / 5
                cow = idx % 5
                te = gc.GetTextExtent(item)
                x = (cow+0.5)*self.w/5-te[0]/2
                y = 100+row*te[1]*3
                x0 = x-2
                y0 = y-te[1]
                x1 = (cow+0.5)*self.w/5+te[0]/2+2
                y1 = 100+(row*3+2)*te[1]
                self.marks.append((x0,x1,y0,y1, item))
                if self.pt[0] >= x0 and self.pt[0] < x1 \
                        and self.pt[1] >= y0 and self.pt[1] < y1 :
                    gc.SetPen(gc.pen['focus'])
                    gc.DrawRectangle(x0,y0,x1-x0,y1-y0)
                gc.DrawText(item, x, y)

            self.EndDraw()

class Window(Panel) :
    def __init__(self, mgr, right_hand, x, y, w, h, frame_id, configs) :
        Panel.__init__(self, None, mgr)
        self.right_hand = right_hand
        self.SetPosition(x, y, w, h)
        self.ShowingMenu = False

        self.header = HeadPanel(self,mgr, configs[6])
        self.panel_left = BodyPanel(self,mgr, configs[0])
        self.panel_right = BodyPanel(self,mgr, configs[1])
        self.panel_left_left = MiniPanel(self,mgr, configs[2], self.panel_left)
        self.panel_left_right = MiniPanel(self,mgr, configs[3], self.panel_left)
        self.panel_right_left = MiniPanel(self,mgr, configs[4], self.panel_right)
        self.panel_right_right = MiniPanel(self,mgr, configs[5], self.panel_right)
        self.MenuPanel = MenuPanel(self,mgr)

        self.panels = [ self.panel_left_right, self.panel_right_right,
            self.panel_right_left, self.panel_left_left,
            self.panel_right, self.panel_left,self.header]

        if right_hand :
            self.ctrls['swap'] = ButtonAP(self)
        else :
            self.ctrls['swap'] = ButtonSW(self)
        self.ctrls['extR'] = ButtonArrowRight(self)
        self.ctrls['extL'] = ButtonArrowLeft(self)
        self.ctrls['extLU'] = ButtonArrowUp(self)
        self.ctrls['extLD'] = ButtonArrowDown(self)
        self.ctrls['extRU'] = ButtonArrowUp(self)
        self.ctrls['extRD'] = ButtonArrowDown(self)
        self.ctrls['swap'].SetClickFunc(mgr.SwapWindow)
        self.ctrls['extR'].SetClickFunc(self.ExtRight)
        self.ctrls['extL'].SetClickFunc(self.ExtLeft)
        self.ctrls['extLU'].SetClickFunc(self.ExtLeftUp)
        self.ctrls['extLD'].SetClickFunc(self.ExtLeftDown)
        self.ctrls['extRU'].SetClickFunc(self.ExtRightUp)
        self.ctrls['extRD'].SetClickFunc(self.ExtRightDown)

        self.Layout(frame_id)

    def ExtRight(self, ctrl, x,y) :
        self.Layout([6,4,6,4,4,3,6,0][self.frame_id])

    def ExtLeft(self, ctrl, x,y) :
        self.Layout([7,7,5,5,3,5,0,7][self.frame_id])

    def ExtLeftUp(self, ctrl, x,y) :
        self.Layout([0,0,2,2,6,5,6,7][self.frame_id])

    def ExtLeftDown(self, ctrl, x,y) :
        self.Layout([1,1,3,3,4,5,4,7][self.frame_id])

    def ExtRightUp(self, ctrl, x,y) :
        self.Layout([0,1,0,1,4,7,6,7][self.frame_id])

    def ExtRightDown(self, ctrl, x,y) :
        self.Layout([2,3,2,3,4,5,6,5][self.frame_id])

    def UpdateGC(self, gc) :
        Panel.UpdateGC(self, gc)
        self.MenuPanel.UpdateGC(gc)

    def Layout(self, frame_id) :
        self.ShowingMenu = False
        self.frame_id = frame_id
        w2 = self.w/2
        w4 = self.w/4
        y1 = 68
        hm = (self.h-y1)/4
        y3 = y1+3*hm
        self.header.SetPosition(0,0,self.w,y1)
        if self.right_hand :
            self.ctrls['swap'].SetLeftTop(0,0)
        else :
            self.ctrls['swap'].SetRightTop(self.w,0)

        if self.frame_id == 0 :
            self.panel_left.SetPosition(0,y1,w2,self.h-y1-hm)
            self.panel_right.SetPosition(w2,y1,w2,self.h-y1-hm)
            self.panel_left_left.SetPosition(0,y3,w4,hm)
            self.panel_left_right.SetPosition(w4,y3,w4,hm)
            self.panel_right_left.SetPosition(w2,y3,w4,hm)
            self.panel_right_right.SetPosition(w2+w4,y3,w4,hm)
            self.ctrls['extR'].SetRightBottom(self.w/2,self.h)
            self.ctrls['extL'].SetLeftBottom(self.w/2,self.h)
            self.ctrls['extLU'].Visable(False)
            self.ctrls['extLD'].SetLeftBottom(0,self.h)
            self.ctrls['extRU'].Visable(False)
            self.ctrls['extRD'].SetRightBottom(self.w,self.h)
        elif self.frame_id == 1 :
            self.panel_left.SetPosition(0,y1,w2,self.h-y1)
            self.panel_right.SetPosition(w2,y1,w2,self.h-y1-hm)
            self.panel_left_left.Visable(False)
            self.panel_left_right.Visable(False)
            self.panel_right_left.SetPosition(w2,y3,w4,hm)
            self.panel_right_right.SetPosition(w2+w4,y3,w4,hm)
            self.ctrls['extR'].SetRightBottom(self.w/2,self.h)
            self.ctrls['extL'].SetLeftBottom(self.w/2,self.h)
            self.ctrls['extLU'].SetLeftBottom(0,self.h)
            self.ctrls['extLD'].Visable(False)
            self.ctrls['extRU'].Visable(False)
            self.ctrls['extRD'].SetRightBottom(self.w,self.h)
        elif self.frame_id == 2 :
            self.panel_left.SetPosition(0,y1,w2,self.h-y1-hm)
            self.panel_right.SetPosition(w2,y1,w2,self.h-y1)
            self.panel_left_left.SetPosition(0,y3,w4,hm)
            self.panel_left_right.SetPosition(w4,y3,w4,hm)
            self.panel_right_left.Visable(False)
            self.panel_right_right.Visable(False)
            self.ctrls['extR'].SetRightBottom(self.w/2,self.h)
            self.ctrls['extL'].SetLeftBottom(self.w/2,self.h)
            self.ctrls['extLU'].Visable(False)
            self.ctrls['extLD'].SetLeftBottom(0,self.h)
            self.ctrls['extRU'].SetRightBottom(self.w,self.h)
            self.ctrls['extRD'].Visable(False)
        elif self.frame_id == 3 :
            self.panel_left.SetPosition(0,y1,w2,self.h-y1)
            self.panel_right.SetPosition(w2,y1,w2,self.h-y1)
            self.panel_left_left.Visable(False)
            self.panel_left_right.Visable(False)
            self.panel_right_left.Visable(False)
            self.panel_right_right.Visable(False)
            self.ctrls['extR'].SetRightBottom(self.w/2,self.h)
            self.ctrls['extL'].SetLeftBottom(self.w/2,self.h)
            self.ctrls['extLU'].SetLeftBottom(0,self.h)
            self.ctrls['extLD'].Visable(False)
            self.ctrls['extRU'].SetRightBottom(self.w,self.h)
            self.ctrls['extRD'].Visable(False)
        elif self.frame_id == 4 :
            self.panel_left.SetPosition(0,y1,self.w,self.h-y1)
            self.panel_right.Visable(False)
            self.panel_left_left.Visable(False)
            self.panel_left_right.Visable(False)
            self.panel_right_left.Visable(False)
            self.panel_right_right.Visable(False)
            self.ctrls['extL'].SetRightBottom(self.w,self.h)
            self.ctrls['extR'].Visable(False)
            self.ctrls['extLU'].SetLeftBottom(0,self.h)
            self.ctrls['extLD'].Visable(False)
            self.ctrls['extRU'].Visable(False)
            self.ctrls['extRD'].Visable(False)
        elif self.frame_id == 5 :
            self.panel_left.Visable(False)
            self.panel_right.SetPosition(0,y1,self.w,self.h-y1)
            self.panel_left_left.Visable(False)
            self.panel_left_right.Visable(False)
            self.panel_right_left.Visable(False)
            self.panel_right_right.Visable(False)
            self.ctrls['extL'].Visable(False)
            self.ctrls['extR'].SetLeftBottom(0,self.h)
            self.ctrls['extLU'].Visable(False)
            self.ctrls['extLD'].Visable(False)
            self.ctrls['extRU'].SetRightBottom(self.w,self.h)
            self.ctrls['extRD'].Visable(False)
        elif self.frame_id == 6 :
            self.panel_left.SetPosition(0,y1,self.w,self.h-y1-hm)
            self.panel_right.Visable(False)
            self.panel_left_left.SetPosition(0,y3,w4,hm)
            self.panel_left_right.SetPosition(w4,y3,w4,hm)
            self.panel_right_left.SetPosition(w2,y3,w4,hm)
            self.panel_right_right.SetPosition(w2+w4,y3,w4,hm)
            self.ctrls['extL'].SetRightBottom(self.w,self.h)
            self.ctrls['extR'].Visable(False)
            self.ctrls['extLU'].Visable(False)
            self.ctrls['extLD'].SetLeftBottom(0,self.h)
            self.ctrls['extRU'].Visable(False)
            self.ctrls['extRD'].Visable(False)
        elif self.frame_id == 7 :
            self.panel_left.Visable(False)
            self.panel_right.SetPosition(0,y1,self.w,self.h-y1-hm)
            self.panel_left_left.SetPosition(0,y3,w4,hm)
            self.panel_left_right.SetPosition(w4,y3,w4,hm)
            self.panel_right_left.SetPosition(w2,y3,w4,hm)
            self.panel_right_right.SetPosition(w2+w4,y3,w4,hm)
            self.ctrls['extL'].Visable(False)
            self.ctrls['extR'].SetLeftBottom(0,self.h)
            self.ctrls['extLU'].Visable(False)
            self.ctrls['extLD'].Visable(False)
            self.ctrls['extRU'].Visable(False)
            self.ctrls['extRD'].SetRightBottom(self.w,self.h)
        for i in self.panels :
            i.Layout()

    def ShowMenu(self, ctrl, x, y) :
        self.ShowingMenu = True
        self.MenuPanel.MenuCtrl = ctrl
        self.MenuPanel.SetPosition(ctrl.parent.x,
                ctrl.parent.y, ctrl.parent.w, self.h)
        self.MenuPanel.Layout()

    def Draw(self) :
        self.BeginDraw(drawBoarder=False)
        if self.ctrls :
            for i in self.ctrls :
                self.ctrls[i].Draw() 
        if self.ShowingMenu :
            self.MenuPanel.Draw()
        Control.EndDraw(self)

    def OnClick(self, x, y) :
        if self.visable:
            x = x - self.x
            y = y - self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                if self.ShowingMenu :
                    if self.MenuPanel.OnClick(x,y) :
                        return True
                for i in self.ctrls :
                    if self.ctrls[i].OnClick(x,y) :
                        return True
                for i in self.panels :
                    if i.OnClick(x,y) :
                        return True
        return False

    def OnTouch(self, x, y) :
        rslt = False
        if self.visable:
            x = x - self.x
            y = y - self.y
            if x >= 0 and x < self.w and y >= 0 and y < self.h :
                self.mgr.ActivePanel = self
            if self.ShowingMenu :
                if self.MenuPanel.OnTouch(x,y) :
                    x = -1
                    y = -1
                    rslt = True
            for i in self.ctrls :
                if self.ctrls[i].OnTouch(x,y) :
                    x = -1
                    y = -1
                    rslt = True
            for i in self.panels :
                if i.OnTouch(x,y) :
                    x = -1
                    y = -1
                    rslt = True
        return rslt


