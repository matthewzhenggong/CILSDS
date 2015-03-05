#!/bin/env python
# -*- coding: utf-8 -*-

from Panel import Panel

class SMS(Panel) :
    def __init__(self, mgr) :
        Panel.__init__(self, None, mgr)

    def Draw(self) :
        self.BeginDraw()
        self.EndDraw()

