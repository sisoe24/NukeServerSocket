"""Test sending messages via TCP when app is connected."""
import json
import socket

import pytest


STRING = 'nss test msg'
TEXT = "print('%s'.upper())" % STRING
FILE = 'tmp/path/nss.py'


def _socket_send(data):
    """Create a socket to send data.

    Socket will connect automatically to the localhost and port 54321.

    Args:
        data (str): data to send.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 54321))
    s.sendall(bytearray(data, encoding='utf-8'))
    s.close()


@pytest.fixture(autouse=True)
def auto_start_connection(_start_connection):
    """Auto start connection for each test."""


@pytest.fixture()
def _check_log_widget(_main_ui):
    """Check if log text has message based on connection status."""
    # TODO: not sure if this is more confusing to understand than writing a
    # method to each test that checks the log.

    def _inspect_log(log, msg):
        """Inspect the various log widget text.

        Asserts if msg is inside the log text.

        Args:
            log (str): the name of the log widget to inspect. Valid names are:
            `status`, `received` and `output`.
            msg (str): the message to check inside the log.
        """
        if log == 'status':
            log = _main_ui.log_widgets.status_text
        elif log == 'received':
            log = _main_ui.log_widgets.received_text
        elif log == 'output':
            log = _main_ui.log_widgets.output_text

        assert msg in log

    return _inspect_log


def test_data_has_json_error(_check_log_widget, qtbot):
    """Check status log text when data has json error."""
    # Data will have a missing enclosing quote
    _socket_send('{text":"print("hello")"}')

    msg = 'Error json deserialization.'
    qtbot.waitUntil(lambda: _check_log_widget('status', msg))


@pytest.mark.parametrize('data', [' ', '{"name": true}', '{"text":""}'],
                         ids=['no data', 'wrong key', 'empty data'])
def test_data_is_invalid(data, qtbot, _check_log_widget):
    """Check if status log has right text."""
    _socket_send(data)

    msg = 'Error. Invalid data:'
    qtbot.waitUntil(lambda: _check_log_widget('status', msg))


@pytest.fixture()
def _send_test_msg(_main_ui):
    _main_ui._send_test()


def test_tester_message_status(qtbot, _send_test_msg, _check_log_widget):
    """Send a test message and check status log text."""
    msg = 'Connection successful'
    qtbot.waitUntil(lambda: _check_log_widget('status', msg))


def test_tester_message_received(qtbot, _send_test_msg, _check_log_widget):
    """Send a test message and check received log text."""
    msg = "from __future__ import print_function; print('Hello from Test Client'"
    qtbot.waitUntil(lambda: _check_log_widget('received', msg))


def test_tester_message_output(qtbot, _send_test_msg, _check_log_widget):
    """Send a test message and check output log text."""
    msg = "Hello from Test Client"
    qtbot.waitUntil(lambda: _check_log_widget('output', msg))


@pytest.fixture(params=[TEXT, json.dumps({"text": TEXT, "file": FILE})],
                ids=['simple string', 'stringified array'])
def _send_data(request):
    """Send valid data via socket connection.

    Data sent will be a simple string and a stringified array.
    """
    _socket_send(request.param)


def test_message_status(_send_data, qtbot, _check_log_widget):
    """Check if status log has right text."""
    msg = 'Message received'
    qtbot.waitUntil(lambda: _check_log_widget('status', msg))


def test_message_received(_send_data, qtbot, _check_log_widget):
    """Check if received log has right text."""
    qtbot.waitUntil(lambda: _check_log_widget('received', TEXT))


def test_message_output(_send_data, qtbot, _check_log_widget):
    """Check if output log has right text."""
    qtbot.waitUntil(lambda: _check_log_widget('output', STRING.upper()))
