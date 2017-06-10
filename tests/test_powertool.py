#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_powertool
----------------------------------

Tests for `powertool` module.
"""

from __future__ import unicode_literals
import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from powertool import powertool
from powertool import cli
try:
    from unittest.mock import patch, mock_open
except ImportError:
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
        "aa:bb:cc:dd:ee:ff": {
            "hostname": "host",
            "username": "user",
            "broadcast": "192.168.1.1"
        }
    }
    runner = CliRunner()
    result = runner.invoke(cli.main, ["list"])
    assert u'user@host' in result.output
    assert u'aa:bb:cc:dd:ee:ff' in result.output
    assert u'192.168.1.1' in result.output


@patch('json.load')
@patch('json.dump')
def test_rm_should_remove_machine(jsondump, jsonload):
    jsonload.return_value = {
        "aa:bb:cc:dd:ee:ff": {
            "hostname": "host",
            "username": "user",
            "broadcast": "192.168.1.1"
        },
        "aa:bb:cc:dd:ee:ee": {
            "hostname": "host2",
            "username": "user",
            "broadcast": "192.168.1.1"
        }
    }
    runner = CliRunner()
    mo = mock_open()
    with patch('powertool.cli.open', mo):
        runner.invoke(cli.main, ["rm", "--host", "host"])

    args, kwargs = jsondump.call_args
    assert "aa:bb:cc:dd:ee:ff" not in args[0]
    assert "aa:bb:cc:dd:ee:ee" in args[0]


@patch('json.load')
@patch('json.dump')
def test_register_should_add_machines(jsondump, jsonload):
    jsonload.return_value = {}
    runner = CliRunner()
    mo = mock_open()
    with patch('powertool.cli.open', mo):
        runner.invoke(cli.main, ["register",
                                 "-b",
                                 "192.168.1.1",
                                 "aa:bb:cc:dd:ee:ff",
                                 "user@host"])

    args, kwargs = jsondump.call_args
    assert "aa:bb:cc:dd:ee:ff" in args[0]


@patch('json.load')
@patch('wakeonlan.wol.send_magic_packet')
def test_wake_should_send_magic_packet(send_magic_packet, jsonload):
    jsonload.return_value = {
        "aa:bb:cc:dd:ee:ff": {
            "hostname": "host",
            "username": "user",
            "broadcast": "192.168.1.1"
        },
        "aa:bb:cc:dd:ee:ee": {
            "hostname": "host2",
            "username": "user",
            "broadcast": "192.168.1.1"
        }
    }
    runner = CliRunner()
    mo = mock_open()
    with patch('powertool.cli.open', mo):
        runner.invoke(cli.main, ["wake", "host"])

    args, kwargs = send_magic_packet.call_args
    print(args)
    assert args[0] == "aa:bb:cc:dd:ee:ff"
    assert kwargs['ip_address'] == "192.168.1.1"


@patch('json.load')
@patch('powertool.cli.Popen')
def test_sleep_should_invoke_ssh_pm_suspend(popen, jsonload):
    jsonload.return_value = {
        "aa:bb:cc:dd:ee:ff": {
            "hostname": "host",
            "username": "user",
            "broadcast": "192.168.1.1"
        },
        "aa:bb:cc:dd:ee:ee": {
            "hostname": "host2",
            "username": "user",
            "broadcast": "192.168.1.1"
        }
    }
    runner = CliRunner()
    mo = mock_open()
    with patch('powertool.cli.open', mo):
        runner.invoke(cli.main, ["sleep", "host"])

    args, kwargs = popen.call_args
    print(args)
    assert " ".join(args[0]) == "ssh user@host sudo pm-suspend"
