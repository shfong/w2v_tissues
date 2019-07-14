#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `w2v_tissues` package."""

import os
import json
import unittest
import shutil
import tempfile
import io
import uuid
import re
from werkzeug.datastructures import FileStorage
import w2v_tissues
from w2v_tissues import ErrorResponse


class TestWordtovectortissues(unittest.TestCase):
    """Tests for `w2v_tissues` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self._temp_dir = tempfile.mkdtemp()
        w2v_tissues.app.testing = True
        w2v_tissues.app.config[w2v_tissues.WORDTOVECMODEL] = self._temp_dir
        self._app = w2v_tissues.app.test_client()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        shutil.rmtree(self._temp_dir)

    def test_error_response(self):
        er = ErrorResponse()
        self.assertEqual(er.errorCode, '')
        self.assertEqual(er.message, '')
        self.assertEqual(er.description, '')
        self.assertEqual(er.stackTrace, '')
        self.assertEqual(er.threadId, '')
        self.assertTrue(er.timeStamp is not None)

    def test_baseurl(self):
        """Test something."""
        rv = self._app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('hello' in str(rv.data))