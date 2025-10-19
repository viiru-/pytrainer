# -*- coding: utf-8 -*-

#Copyright (C) Fiz Vazquez vud1@sindominio.net

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import logging
from .gui.drawArea import DrawArea

class RecordGraph:
    def __init__(self, vbox = None, window = None, pytrainer_main=None):
        logging.debug(">>")
        self.pytrainer_main = pytrainer_main
        self.drawarea = DrawArea(vbox, window)
        logging.debug("<<")

    def drawgraph(self,values,laps=None, y1limits=None, y1color=None, y1_linewidth=1):
        logging.debug(">>")

        xval = []
        yval = []
        xlab = []
        ylab = []
        tit = []
        col = []
        lapValues = None

        value_selected = 0

        value_selected2 = 0
        xvalues, yvalues = self.get_values(values,value_selected)
        max_yvalue = max(yvalues)
        min_yvalue = min(yvalues)
        xlabel,ylabel,title,color = self.get_value_params(value_selected)
        if y1color is not None:
            color = y1color

        xval.append(xvalues)
        yval.append(yvalues)
        if value_selected2 > 0:
            xlab.append("")
        else:
            xlab.append(xlabel)
        ylab.append(ylabel)
        tit.append(title)
        col.append(color)

        if value_selected2 > 0:
            value_selected2 = value_selected2-1
            xlabel,ylabel,title,color = self.get_value_params(value_selected2)
            xvalues,yvalues = self.get_values(values,value_selected2)
            xval.append(xvalues)
            yval.append(yvalues)
            xlab.append(xlabel)
            ylab.append(ylabel)
            tit.append("")
            col.append(color)
        logging.info("To show: tit: %s | col: %s | xlab: %s | ylab: %s", tit, col, xlab, ylab)
        self.drawarea.drawPlot(xval,yval,xlab,ylab,tit,col,None,lapValues, ylimits=y1limits, y1_linewidth=y1_linewidth)

        logging.debug("<<")

    def get_value_params(self,value):
        if value == 0:
            return _("Distance (km)"),_("Height (m)"),_("Stage Profile"),"#000000"
        if value == 1:
            return _("Distance (km)"),_("Speed (Km/h)"),_("Speed"),"#00ff00"
        if value == 2:
            return _("Distance (km)"),_("Pace (min/km)"),_("Pace"),"#0000ff"
        if value == 3:
            return _("Distance (km)"),_("Beats (bpm)"),_("Heart Rate"),"#ff0000"
        if value == 4:
            return _("Distance (km)"),_("Cadence (rpm)"),_("Cadence"),"#7B3F00"
        if value == 5:
            return _("Distance (km)"),_("Beats (%)"),_("Beats"),"#ff0000"
        if value == 6:
            return _("Distance (km)"),_("Zone"),_("Zone"),"#ff0000"


    def get_values(self,values, value_selected):
        logging.debug(">>")
        xvalue = []
        yvalue = []
        zones = self.pytrainer_main.profile.getZones()
        for value in values:
            xvalue.append(value[0])
            if value_selected==0:
                yvalue.append(value[1])
            if value_selected==1:
                yvalue.append(value[3])
            if value_selected==2:
                try:
                    yvalue.append(60/value[3])
                except:
                    yvalue.append(0)
            if value_selected==3:
                yvalue.append(value[6])
            if value_selected==4:
                yvalue.append(value[7])
            if value_selected==5:
                if value[6] <= zones[4][0]:
                    yvalue.append(50.0*value[6]/zones[4][0])
                else:
                    yvalue.append(50.0+50.0*((value[6]-zones[4][0])/(zones[0][1]-zones[4][0])))
            if value_selected==6:
                if value[6] <= zones[4][0]:
                    yvalue.append(1.0*value[6]/zones[4][0])
                else:
                    yvalue.append(1.0+5.0*((value[6]-zones[4][0])/(zones[0][1]-zones[4][0])))
        logging.debug("<<")
        return xvalue,yvalue

    def getFloatValue(self, value):
        try:
            return float(value)
        except:
            return float(0)

