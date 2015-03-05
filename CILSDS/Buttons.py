#!/bin/env python
# -*- coding: utf-8 -*-

from Control import Control

class Button(Control) :
    def __init__(self, parent, label='') :
        Control.__init__(self, parent)
        self.brush = 'button'
        self.font = 'button'
        self.pen = 'button'
        self.txt = label

    def Draw(self) :
        if self.visable :
            self.BeginDraw()

            gc = self.gc
            if self.touching :
                gc.SetPen(gc.pen['focus'])
            else :
                gc.SetPen(gc.pen['none'])
            gc.SetBrush(gc.brush[self.brush])
            gc.DrawRectangle(1,1,self.w-2,self.h-2)

            gc.SetPen(gc.pen[self.pen])
            gc.SetFont(gc.font[self.font])

            self.DrawContent()

            self.EndDraw()

    def DrawContent(self) :
        te = self.gc.GetTextExtent(self.txt)
        self.gc.DrawText(self.txt, (self.w-te[0])/2, (self.h-te[1])/2)

class ButtonSW(Button) :
    def __init__(self, parent) :
        Button.__init__(self, parent, 'SW')
        self.w = 40
        self.h = 60

    def DrawContent(self) :
        gc = self.gc
        te = gc.GetTextExtent(self.txt)
        gc.StrokeLines([(40-6,20),(40-6,11),(40-28,29),(40-6,49),(40-6,40)])
        gc.DrawText(self.txt, (self.w-te[0]), (self.h-te[1])/2)

class ButtonAP(Button) :
    def __init__(self, parent) :
        Button.__init__(self, parent, 'AP')
        self.w = 40
        self.h = 60

    def DrawContent(self) :
        gc = self.gc
        te = gc.GetTextExtent(self.txt)
        gc.StrokeLines([(6,20),(6,11),(28,29),(6,49),(6,40)])
        gc.DrawText(self.txt, 0, (self.h-te[1])/2)

class ButtonArrowRight(Button) :
    def __init__(self, parent) :
        Button.__init__(self, parent)
        self.w = 20
        self.h = 40

    def DrawContent(self) :
        margin = 1
        self.gc.StrokeLines([(margin,margin),(self.w-margin,self.h/2),(margin,self.h-margin),(margin,margin)])

class ButtonArrowLeft(Button) :
    def __init__(self, parent) :
        Button.__init__(self, parent)
        self.w = 20
        self.h = 40

    def DrawContent(self) :
        margin = 1
        self.gc.StrokeLines([(margin,self.h/2),(self.w-margin,margin),(self.w-margin,self.h-margin),(margin,self.h/2)])

class ButtonArrowDown(Button) :
    def __init__(self, parent) :
        Button.__init__(self, parent)
        self.w = 40
        self.h = 20

    def DrawContent(self) :
        margin = 1
        self.gc.StrokeLines([(margin,margin),(self.w/2,self.h-margin),(self.w-margin,margin),(margin,margin)])

class ButtonArrowUp(Button) :
    def __init__(self, parent) :
        Button.__init__(self, parent)
        self.w = 40
        self.h = 20

    def DrawContent(self) :
        margin = 1
        self.gc.StrokeLines([(self.w/2,margin),(margin,self.h-margin),(self.w-margin,self.h-margin),(self.w/2,margin)])

class ButtonTitle(Button) :
    def __init__(self, parent) :
        Button.__init__(self, parent)
        self.w = 50
        self.h = 40
        self.font = 'menu_title'

    def DrawContent(self) :
        gc = self.gc
        te = gc.GetTextExtent(self.parent.title)
        gc.DrawText(self.parent.title, (self.w-te[0])/2, (self.h-te[1])/2)


