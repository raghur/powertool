#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_powertool
----------------------------------

Tests for `powertool` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from powertool import powertool
from powertool import cli
try:
    from unittest.mock import patch, mock_open
except NameError:
    from mock import patch, mock_open


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main, {})
    # assert result.exit_code == 0
    assert '--help' in result.output
    # assert 'powertool.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output


@patch('json.load')
def test_list_should_return_machines(jsonload):
    jsonload.return_value = {
        "aa:bb:cc:dd:ee:ff" : {
            "hostname" : "host",
            "username" : "user",
            "broadcast" : "192.168.1.1"
        }
    }
    runner = CliRunner()
    result = runner.invoke(cli.main, ["list"])
    assert 'user@host' in result.output
    assert 'aa:bb:cc:dd:ee:ff' in result.output
    assert '192.168.1.1' in result.output


@patch('json.load')
@patch('json.dump')
def test_list_should_remove_machine(jsondump, jsonload):
    jsonload.return_value = {
        "aa:bb:cc:dd:ee:ff" : {
            "hostname" : "host",
            "username" : "user",
            "broadcast" : "192.168.1.1"
        },
        "aa:bb:cc:dd:ee:ee" : {
            "hostname" : "host2",
            "username" : "user",
            "broadcast" : "192.168.1.1"
        }
    }
    runner = CliRunner()
    mo = mock_open()
    with patch('powertool.cli.open', mo):
        runner.invoke(cli.main, ["rm", "--host", "host"])

    args, kwargs = jsondump.call_args
    assert "aa:bb:cc:dd:ee:ff" not in args[0]
    assert "aa:bb:cc:dd:ee:ee" in args[0]
