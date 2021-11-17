# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "05/04/2019"


import unittest
import tempfile
import shutil
import time
import os
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.process.control.datatransfert import FolderTransfert
from tomwer.test.utils import UtilsTest
from tomwer.synctools.rsyncmanager import RSyncManager
from tomwer.core.process.control.datalistener import DataListener
import pytest


class TestDataTransferIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    def setUp(self):
        super().setUp()
        self._used_folders = []
        self.origin_folder = None
        self.output_folder = None

    def tearDown(self):
        for folder in self._used_folders:
            shutil.rmtree(folder)
        super().tearDown()

    def testInputOutput(self):
        """Test that io using TomoBase instance work"""
        for input_type in (dict, TomwerScanBase):
            for return_dict in (True, False):
                with self.subTest(
                    return_dict=return_dict,
                    input_type=input_type,
                ):
                    output_folder = tempfile.mkdtemp()
                    origin_folder = tempfile.mkdtemp()
                    scan_folder = os.path.join(origin_folder, "scan_toto")
                    os.makedirs(scan_folder)
                    os.makedirs(os.path.join(output_folder, "scan_toto"))
                    self._used_folders.append(output_folder)
                    self._used_folders.append(origin_folder)

                    scan = MockEDF.mockScan(
                        scanID=scan_folder,
                        nRadio=10,
                        nRecons=1,
                        nPagRecons=4,
                        dim=10,
                    )

                    transfert_process = FolderTransfert(
                        inputs={
                            "data": scan,
                            "dest_dir": output_folder,
                            "return_dict": return_dict,
                        }
                    )

                    self.assertTrue(os.path.exists(output_folder))
                    input_obj = scan
                    if input_obj is dict:
                        input_obj = input_obj.to_dict()
                    transfert_process.run()
                    out = transfert_process.outputs.data
                    if return_dict:
                        self.assertTrue(isinstance(out, dict))
                    else:
                        self.assertTrue(isinstance(out, TomwerScanBase))


@pytest.mark.skipif(not RSyncManager().has_rsync(), reason="requires rsync")
class TestBlissDataTransfer(unittest.TestCase):
    """Make sure we can transfer data from bliss acquisition"""

    def setUp(self):
        self.input_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()
        shutil.copytree(
            UtilsTest.getBlissDataset(folderID="sample"),
            os.path.join(self.input_dir, "sample"),
        )

        self._proposal_file = os.path.join(
            self.input_dir, "sample", "ihpayno_sample.h5"
        )
        self._sample_file = os.path.join(
            self.input_dir, "sample", "sample_29042021", "sample_29042021.h5"
        )
        self._sample_file_entry = "1.1"
        assert os.path.exists(self._sample_file)

        # mock data listener: the processing of the Data transfer requires
        # knowledge of bliss files origin.
        self.assertTrue(os.path.exists(self._proposal_file))
        data_listener = DataListener()
        scans = data_listener.process_sample_file(
            sample_file=self._sample_file,
            entry=self._sample_file_entry,
            proposal_file=self._proposal_file,
            master_sample_file=None,
        )
        self.scan = scans[0]
        self.assertTrue(os.path.exists(self.scan.process_file))

    def tearDown(self):
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)

    def testDataTransfer(self):
        """Make sure the data transfer is able to retrieve the scan,
        proposal file and scan file to transfer.
        Check that only the specific scan folders will be copy and removed
        and the other won't be affected.
        """
        out_nx = os.path.join(
            self.output_dir, "sample_29042021", "sample_29042021_1_1.nx"
        )
        self.assertFalse(os.path.exists(out_nx))
        out_proposal = os.path.join(self.output_dir, "ihpayno_sample.h5")
        self.assertFalse(os.path.exists(out_proposal))
        out_sample_file = os.path.join(
            self.output_dir, "sample_29042021", "sample_29042021.h5"
        )
        self.assertFalse(os.path.exists(out_sample_file))
        out_included_scans = [
            os.path.join(self.output_dir, "sample_29042021", "scan0002")
        ]
        for scan_path in out_included_scans:
            self.assertFalse(os.path.exists(scan_path))
        out_not_included_scans = [
            os.path.join(self.output_dir, "sample_29042021", "scan0004"),
            os.path.join(self.output_dir, "sample_29042021", "scan0006"),
            os.path.join(self.output_dir, "sample_29042021", "scan0008"),
        ]
        for scan_path in out_not_included_scans:
            self.assertFalse(os.path.exists(scan_path))

        process = FolderTransfert(
            inputs={
                "data": self.scan,
                "block": True,
                "dest_dir": self.output_dir,
            }
        )
        process.run()

        time.sleep(1)
        self.assertTrue(os.path.exists(out_nx), f"{out_nx} does not exists")
        # self.assertTrue(os.path.exists(out_proposal), f"{out_proposal} does not exists")
        self.assertTrue(
            os.path.exists(out_sample_file), f"{out_sample_file} does not exists"
        )
        for scan_path in out_included_scans:
            self.assertTrue(os.path.exists(scan_path))
        for scan_path in out_not_included_scans:
            self.assertFalse(os.path.exists(scan_path))
