#!/bin/env python
# -*- coding: utf-8 -*-

import wx

def DrawSymAC(gc, x, y, sx, sy):
    gc.PushState()
    gc.Translate(x, y)
    gc.StrokeLines([(i[0]*sx,i[1]*sy) for i in gc.symbol_ac])
    gc.PopState()


def CreateResources(gc):
    gc.pen = {}
    gc.pen['none'] = gc.CreatePen(wx.NullPen)
    gc.pen['default'] = gc.CreatePen(wx.Pen(wx.GREEN, 2, wx.PENSTYLE_SOLID))
    gc.pen['panel_board'] = gc.CreatePen(wx.Pen(wx.GREEN, 1, wx.PENSTYLE_SOLID))
    gc.pen['act_panel_board'] = gc.CreatePen(wx.Pen(wx.Colour(0xCF,0xFF,0x50), 3))
    gc.pen['focus'] = gc.CreatePen(wx.Pen(wx.WHITE, 1, wx.PENSTYLE_SHORT_DASH))
    gc.pen['clicking_cross'] = gc.CreatePen(wx.Pen(wx.RED, 2, wx.PENSTYLE_SHORT_DASH))
    gc.pen['button'] = gc.CreatePen(wx.Pen(wx.CYAN, 2, wx.PENSTYLE_SOLID))
    gc.pen['red'] = gc.CreatePen(wx.Pen(wx.RED, 2))
    gc.pen['blue'] = gc.CreatePen(wx.Pen(wx.BLUE, 2))
    gc.pen['green'] = gc.CreatePen(wx.Pen(wx.GREEN, 2))
    gc.pen['green1'] = gc.CreatePen(wx.Pen(wx.GREEN, 1))
    gc.pen['white'] = gc.CreatePen(wx.Pen(wx.WHITE, 2))
    gc.pen['black'] = gc.CreatePen(wx.Pen(wx.BLACK, 2))
    gc.pen['white1'] = gc.CreatePen(wx.Pen(wx.WHITE, 1))
    gc.pen['big_purple'] = gc.CreatePen(wx.Pen(wx.Colour(0xCC,0x00,0xFF), 7))
    gc.pen['purple'] = gc.CreatePen(wx.Pen(wx.Colour(0xCC,0x00,0xFF), 2))
    gc.pen['white_sto'] = gc.CreatePen(wx.Pen(wx.WHITE, 2, wx.PENSTYLE_SHORT_DASH ))
    gc.brush = {}
    gc.brush['none'] = gc.CreateBrush(wx.NullBrush)
    gc.brush['default'] = gc.brush['none']
    gc.brush['back'] = gc.CreateBrush(wx.BLACK_BRUSH)
    gc.brush['button'] = gc.brush['none']
    gc.brush['blue'] = gc.CreateBrush(wx.Brush(wx.BLUE))
    gc.brush['green'] = gc.CreateBrush(wx.Brush(wx.GREEN))
    gc.brush['white'] = gc.CreateBrush(wx.Brush(wx.WHITE))
    gc.brush['ground'] = gc.CreateBrush(wx.Brush(wx.Colour(0x7D,0x3B,0x42)))
    gc.brush['sky'] = gc.CreateBrush(wx.Brush(wx.Colour(0x23,0x51,0x7C)))
    gc.brush['tab'] = gc.CreateBrush(wx.Brush(wx.Colour(0x00,0x00,0x00, 0x7E)))
    gc.font = {}
    font = [wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD),
            wx.Font(20, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD),
            wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL) ]
    gc.font['default'] = gc.CreateFont(font[0], wx.WHITE)
    gc.font['button'] = gc.CreateFont(font[0], wx.CYAN)
    gc.font['tab'] = gc.font['button']
    gc.font['white12'] = gc.CreateFont(font[0], wx.WHITE)
    gc.font['white20'] = gc.CreateFont(font[1], wx.WHITE)
    gc.font['green12'] = gc.CreateFont(font[0], wx.GREEN)
    gc.font['cyan12'] = gc.CreateFont(font[0], wx.CYAN)
    gc.font['menu_title'] = gc.font['green12']
    gc.font['menu_subtitle'] = gc.CreateFont(font[0], wx.Colour(0xCC,0x00,0xFF))
    gc.font['menu_text'] = gc.CreateFont(font[0], wx.CYAN)
    gc.font['white10'] = gc.CreateFont(font[2], wx.WHITE)
    gc.font['green10'] = gc.CreateFont(font[2], wx.GREEN)

    gc.symbol_ac = [(0.015102934, -1.000386053),
(0.202795457, -0.594298431),
(0.370614148, -0.447834978),
(0.432758074, -0.22054247),
(0.979001064, 0.072955673),
(0.998725363, 0.365025673),
(0.429939382, 0.395929191),
(0.639359943, 0.656067432),
(0.407099195, 0.785222644),
(-0.330099403, 0.79944626),
(-0.64548959, 0.685028768),
(-0.496731179, 0.393415836),
(-0.980903609, 0.343433132),
(-1.000628842, 0.051363132),
(-0.472926038, -0.206775793),
(-0.366510618, -0.449834294),
(-0.197209216, -0.627829669),
(0.015102934, -1.000386053)]
    gc.DrawSymAC = DrawSymAC



