# **************************************************************************
# *
# * Authors:  Yunior C. Fonseca Reyna (coss@cnb.csic.es), Aug 2018
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

BLIK_HOME = 'BLIK_HOME'


def getBlikEnvName(version):
    return f"blik-{version}"


V0_6_1 = '0.6.1'

BLIK_DEF_VER = V0_6_1
BLIK_ACTIVATION_CMD = 'conda activate %s' % getBlikEnvName(BLIK_DEF_VER)
BLIK_ENV_ACTIVATION = 'BLIK_ENV_ACTIVATION'
BLIK = 'blik'
