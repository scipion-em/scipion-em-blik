import os
from pathlib import Path
from pyworkflow.constants import BETA
from tomo.protocols import ProtTomoPicking


class ProtBlikTomoPicking(ProtTomoPicking):
    """Pick particles using blik."""

    _label = 'blik tomo picking'
    _devStatus = BETA

    def _insertAllSteps(self):
        self._insertFunctionStep(self.runBlikStep, interactive=True)
        self._insertFunctionStep(self.createOutputStep)

    def runBlikStep(self):
        from blik import Plugin

        tomogram_paths = [
            Path(tomogram.getFileName()).absolute()
            for tomogram in self.inputTomograms.get().iterItems()
        ]

        output_path = self._getExtraPath()

        Plugin.runBlik(protocol=self, output_path=output_path, tomograms=tomogram_paths)

    def createOutputStep(self):
        output_path = Path(self._getExtraPath())
        particle_picks = output_path.glob('*_particle_picks_*.star')

        tomograms = self.getInputTomos()

        # somehow get propert relations between tomos and particles
