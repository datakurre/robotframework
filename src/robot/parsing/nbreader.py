#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from io import BytesIO

from robot.errors import DataError

from .robotreader import RobotReader


def NotebookReader():
    try:
        import nbformat
    except ImportError:
        raise DataError("Using Notebook test data requires having "
                        "'nbformat' module version 4.4.0 or newer installed.")

    class NotebookReader(object):

        def read(self, ipynbfile, rawdata):
            notebook = nbformat.read(ipynbfile, nbformat.NO_CONVERT)
            data = '\n\n'.join([
                cell.source
                for cell in notebook.cells
                if cell.cell_type == 'code'
            ])
            robotfile = BytesIO(data.encode('UTF-8'))
            return RobotReader().read(robotfile, rawdata, ipynbfile.name)

    return NotebookReader()
