# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     Y.C. Fonseca Reyna (cfonseca@cnb.csic.es )
# *
# * your institution
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
import os
from pwem.protocols import EMProtocol
from pyworkflow.constants import BETA
from pyworkflow.protocol import params

from tomo.protocols import ProtTomoBase
from blik.constants import BLIK


class ProtBlikTomo(EMProtocol, ProtTomoBase):
    """
    Tool for visualising and interacting with cryo-ET and subtomogram averaging
    data using napari viewer
    """
    _label = 'tomo blik'
    _devStatus = BETA

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label='Input')

        form.addParam('inputTomograms', params.PointerParam, pointerClass='SetOfTomograms',
                      label="Tomograms", important=True,
                      help='Select the input tomograms')

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        self._insertFunctionStep(self.runNapariBlikStep, interactive=True)
        self._insertFunctionStep(self.createOutputStep)

    def runNapariBlikStep(self):
        from blik import Plugin, NAPARI
        import time
        time.sleep(10)
        startFilesPath = ''
        tomogramsPath = ' '.join(os.path.abspath(tomogram.getFileName()) for tomogram in self.inputTomograms.get().iterItems())

        # Assuming that the .star files are in the same directory where the tomogram is
        tomogramList = tomogramsPath.split(' ')
        for tomogram in tomogramList:
            starFile, _ = os.path.splitext(tomogram)
            starFile += '.star'
            if os.path.exists(starFile):
                startFilesPath += starFile + ' '

        args = '-w %s -- %s %s' % (BLIK, startFilesPath, tomogramsPath)
        Plugin.runBlik(self, NAPARI, args)

    def createOutputStep(self):
        pass

    # --------------------------- INFO functions ----------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []
        return summary

    def _methods(self):
        methods = []
        return methods
