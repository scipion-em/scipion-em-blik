import os
from pyworkflow.constants import BETA
from pyworkflow.protocol import params
from tomo.objects import SetOfCoordinates3D
from tomo.protocols import ProtTomoPicking
from tomo.constants import tomoConst
from blik.constants import BLIK


class ProtBlikTomoPicking(ProtTomoPicking):
    """Pick particles using blik."""

    _label = 'blik tomo picking'
    _devStatus = BETA
    _interactiveMode = True
    _possibleOutputs = {'output3DCoordinates': SetOfCoordinates3D}

    def _insertAllSteps(self):
        self._insertFunctionStep(self.runBlikStep, interactive=True)
        self._insertFunctionStep(self.createOutputStep)

    def prepareOutputStep(self):
        output_path = self._getExtraPath()  # where is this defined? how does it work?

    def runBlikStep(self):
        from blik import Plugin, NAPARI
        tomogram_paths = [
            os.path.abspath(tomogram.getFileName())
            for tomogram in self.inputTomograms.get().iterItems()
        ]

        args = '-w %s -- %s' % (BLIK, ' '.join(tomogram_paths))
        Plugin.runBlik(self, NAPARI, args)

    def createOutputStep(self):
        tomograms = self.getInputTomos()

        setOfCoord3D = self._createSetOfCoordinates3D(
            self.getInputTomos(pointer=True),
            self._getOutputSuffix(SetOfCoordinates3D),
        )
        setOfCoord3D.setName("tomoCoord")
        setOfCoord3D.setSamplingRate(tomograms.getSamplingRate())

        for tomogram in tomograms.iterItems():
            filePath = os.path.join(output_path, )
            if os.path.exists(filePath) and os.path.getsize(filePath):
                tomogramClone = tomogram.clone()
                tomogramClone.copyInfo(tomogram)
                convert.readSetOfCoordinates3D(tomogramClone, setOfCoord3D,
                                               filePath, boxSize=None,
                                               origin=tomoConst.BOTTOM_LEFT_CORNER)

        name = self.OUTPUT_PREFIX + suffix
        self._defineOutputs(**{name: setOfCoord3D})
        self._defineSourceRelation(tomograms, setOfCoord3D)
