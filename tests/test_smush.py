#!/usr/bin/env python

import unittest
import os, os.path, sys, shutil, time, subprocess
sys.path.insert(0, os.path.abspath('./smush'))
from smush import Smush

# import logging
# project_name = 'test_smush'
# logger = logging.getLogger(project_name)
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# logpath = os.path.expanduser('~/Library/Logs/%s.log' % (project_name))
# if os.path.isfile(logpath) == False:
#     open(logpath, 'w').close()
# mylog = logging.FileHandler(logpath)
# mylog.setFormatter(formatter)
# logger.addHandler(mylog)
# logger.setLevel(logging.INFO)

script_path = os.path.join(os.getcwd(), __file__)
script_dir = os.path.dirname(script_path)
materials_dir = os.path.join(script_dir, 'materials')
filename_gif = 'exam_gif_to_png.gif'

class TestSetup(object):
    working_dir = ''
    working_dirname = ''
    working_files = ''

    def setUp(self):
        # logger.info('Setup')
        # logger.info(materials_dir)
        # logger.info(os.listdir(materials_dir))
        self.working_dirname = '%s' % time.time()
        self.working_dir = os.path.join(script_dir, self.working_dirname)
        shutil.copytree(materials_dir, self.working_dir)
        # logger.info(os.listdir(materials_dir))
        # logger.info('DIR: %s' % self.working_dir)
        files = subprocess.check_output(
            ' '.join(['cd', self.working_dir, '&&', 'find', '.', '-type', 'f', '-regex', '".*[^DS_Store]"']),
            shell=True
        )
        self.working_files = str.splitlines(files);
        i = 0
        for each_file in self.working_files:
            self.working_files[i] = each_file[2:]
            i = i + 1

    def tearDown(self):
        # logger.info('teardown')
        if os.path.isdir(self.working_dir) == True:
            shutil.rmtree(self.working_dir)
            self.working_dir = ''

class SmushTestSuite(TestSetup, unittest.TestCase):
    def test_smush_file (self):
        smushing_path = os.path.join(self.working_dir, filename_gif)
        smush = Smush(strip_jpg_meta=False, list_only=False, quiet=True, exclude='.bzr,.git,.hg,.svn,.DS_Store')
        smush.process(smushing_path, False)

        for each_file in self.working_files:
            if each_file == filename_gif:
                src_size = os.path.getsize(os.path.join(materials_dir, each_file))
                dest_size = os.path.getsize(smushing_path)
                self.assertTrue(src_size > dest_size)
            else:
                src_size = os.path.getsize(os.path.join(materials_dir, each_file))
                dest_size = os.path.getsize(os.path.join(self.working_dir, each_file))
                self.assertTrue(src_size == dest_size)
        return True

    def test_smush_dir_not_recursive (self):
        smush = Smush(strip_jpg_meta=False, list_only=False, quiet=True, exclude='.bzr,.git,.hg,.svn,.DS_Store')
        smush.process(self.working_dir, False)

        for each_file in self.working_files:
            if each_file == filename_gif:
                src_size = os.path.getsize(os.path.join(materials_dir, each_file))
                dest_size = os.path.getsize(os.path.join(self.working_dir, each_file))
                self.assertTrue(src_size > dest_size)
            else:
                src_size = os.path.getsize(os.path.join(materials_dir, each_file))
                dest_size = os.path.getsize(os.path.join(self.working_dir, each_file))
                self.assertTrue(src_size == dest_size)
        return True

    def test_smush_dir_recursive (self):
        smush = Smush(strip_jpg_meta=False, list_only=False, quiet=True, exclude='.bzr,.git,.hg,.svn,.DS_Store')
        smush.process(self.working_dir, True)

        for each_file in self.working_files:
            src_size = os.path.getsize(os.path.join(materials_dir, each_file))
            dest_size = os.path.getsize(os.path.join(self.working_dir, each_file))
            self.assertTrue(src_size > dest_size)
        return True

if __name__ == '__main__':
    # logger.info('%s started at %d' % (project_name, time.time()))
    unittest.main()
