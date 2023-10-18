# **************************************************************************
# *
# * Authors:     Yunior C. Fonseca Reyna (cfonseca@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
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
import pwem
import pyworkflow.utils as pwutils

from blik.constants import *

__version__ = '3.0.0'


class Plugin(pwem.Plugin):
    _homeVar = BLIK_HOME
    _pathVars = [BLIK_HOME]

    @classmethod
    def _defineVariables(cls):
        cls._defineVar(BLIK_ENV_ACTIVATION, BLIK_ACTIVATION_CMD)
        cls._defineEmVar(BLIK_HOME, 'blik-' + BLIK_DEF_VER)

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch napari. """
        environ = pwutils.Environ(os.environ)
        if 'PYTHONPATH' in environ:
            # this is required for python virtual env to work
            del environ['PYTHONPATH']
        return environ

    @classmethod
    def getDependencies(cls):
        """ Return a list of dependencies. Include conda if
            activation command was not found. """
        condaActivationCmd = cls.getCondaActivationCmd()
        neededProgs = ['wget']
        if not condaActivationCmd:
            neededProgs.append('conda')

        return neededProgs

    @classmethod
    def addBlikPackage(cls, env, version, default=False):
        ENV_NAME = getBlikEnvName(version)
        BLIK_INSTALLED = f"blik_{version}_installed"
        installCmd = [cls.getCondaActivationCmd(),
                      f'conda create -y -n {ENV_NAME} -c conda-forge',
                      'python=3.10 &&',
                      f'conda activate {ENV_NAME} &&',
                      f'pip install blik[all]=={version}']

        # Flag installation finished
        installCmd.append(f'&& touch {BLIK_INSTALLED}')

        blik_commands = [(" ".join(installCmd), BLIK_INSTALLED)]

        envPath = os.environ.get('PATH', "")
        # keep path since conda likely in there
        installEnvVars = {'PATH': envPath} if envPath else None
        env.addPackage(f'blik', version=version,
                       tar='void.tgz',
                       commands=blik_commands,
                       neededProgs=cls.getDependencies(),
                       default=default,
                       vars=installEnvVars)

    @classmethod
    def runBlik(cls, protocol, program, args):
        """ Run Napari boxmanager from a given protocol. """
        fullProgram = '%s %s && %s' % (cls.getCondaActivationCmd(),
                                                BLIK_ACTIVATION_CMD,
                                                program)
        pwutils.runJob(None, fullProgram, args, env=cls.getEnviron(), cwd=None,
                       numberOfMpi=1)

    @classmethod
    def defineBinaries(cls, env):
        cls.addBlikPackage(env, V0_5_5, default=True)


