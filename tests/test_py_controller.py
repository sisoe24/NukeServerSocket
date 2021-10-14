import re
from typing import MutableMapping

import pytest
from collections import namedtuple

from src.script_editor import nuke_se_controllers as nse
from src.utils import AppSettings

BEGIN_PATTERN = r'(\[\d\d:\d\d:\d\d\] \[Nuke Tools\]) '
END_PATTERN = '\nHello'
OUTPUT_PATTERN = BEGIN_PATTERN + r'.+?py (↴)?\n'

SAMPLE_TEXT = 'Random Code Result: {}'.format(END_PATTERN.strip())

# TODO: test clean_output and append
# BUG: something happens when toggling options to clean text


@pytest.fixture()
def settings(scope='session'):
    yield AppSettings()


# @pytest.fixture(scope='session')
# def se_controller():
#     """Get the ScriptEditorController Class"""
#     controller = nse.ScriptEditorController()
#     yield controller


@pytest.fixture()
def py_controller():
    """Get the PyController Class"""
    controller = nse._PyController('path/to/file.py')
    yield controller


def show_path_settings():
    ShowPath = namedtuple('ShowPath', ['setting', 'expected'])
    return (ShowPath(True, 'path/to/file.py'), ShowPath(False, 'file.py'))


@pytest.mark.parametrize('show_path', show_path_settings(), ids=['fullpath', 'basename'])
def test_show_filename(show_path, settings, py_controller):
    """Check if file path is displayed correctly based on settings."""
    settings.setValue('options/show_file_path', show_path.setting)
    assert py_controller._show_file() == show_path.expected


@pytest.mark.parametrize('msg', ['RandomCode Result: Hello', 'Hello'],
                         ids=['With Result', 'No Result'])
def test_clean_output(py_controller, msg):
    """Check if output text is getting cleaned from Result."""
    assert py_controller._clean_output(msg) == 'Hello'


def output_format_settings():
    """UGLY STUFF."""
    def pattern(s):
        return BEGIN_PATTERN + s + END_PATTERN

    Format = namedtuple('Format', ['show_file', 'show_unicode', 'pattern'])
    return (
        Format(True, True, pattern(r'path/to/file\.py ↴')),
        Format(True, False, pattern(r'path/to/file\.py ')),
        Format(False, True, pattern(r'file\.py ↴')),
        Format(False, False, pattern(r'file\.py ')),
    )


@pytest.mark.parametrize('output', output_format_settings(),
                         ids=['filepath + unicode', 'filepath no unicode',
                              'filename + unicode', 'filename no unicode'])
def test_output_format(py_controller, settings, output):
    """Test various format output settings"""
    settings.setValue('options/show_file_path', output.show_file)
    settings.setValue('options/show_unicode', output.show_unicode)

    result = py_controller._format_output(SAMPLE_TEXT)
    assert re.match(output.pattern, result)


def test_append_output(py_controller):
    """Append output to class attribute."""
    py_controller._append_output(SAMPLE_TEXT)
    assert py_controller.history == [SAMPLE_TEXT]


def test_clear_history(py_controller):
    """Clear history"""
    py_controller._clear_history()
    assert py_controller.history == []


@pytest.fixture()
def override_input_editor(py_controller, settings):
    """Override input editor fixture factory."""

    def _override_input_editor(value):
        settings.setValue('options/override_input_editor', value)
        py_controller.restore_input()
        return py_controller.input()

    py_controller.set_input(SAMPLE_TEXT)
    return _override_input_editor


def test_restore_input(override_input_editor, py_controller):
    """Check if input was restored."""
    input_text = override_input_editor(False)
    assert input_text == py_controller.initial_input


def test_override_input(override_input_editor):
    """Check if input was overridden."""
    input_text = override_input_editor(True)
    assert input_text == SAMPLE_TEXT


@pytest.fixture()
def output_to_console(py_controller, settings):
    """Restore output fixture factory."""

    def _restore_output(value):
        py_controller.set_input("print('nukeserversocket'.upper())")
        py_controller.execute()

        settings.setValue('options/output_to_console', value)
        py_controller.restore_output()

        return py_controller.output()

    return _restore_output


def test_override_output(output_to_console, py_controller):
    """Check if output was not sent to console."""
    output_text = output_to_console(False)
    assert output_text == py_controller.initial_output


def test_restore_output(output_to_console):
    """Check if output was sent to console."""
    output_text = output_to_console(True)
    assert re.search(OUTPUT_PATTERN + 'NUKESERVERSOCKET', output_text)


@pytest.fixture()
def clear_output(output_to_console, settings):
    """Execute code a two times to check if based on clear_output settings, the
    widget will register the clean."""

    def _clear_output(value):
        """Return True if there is only one Nuke Tools line, False otherwise"""
        settings.setValue('options/clear_output', value)
        for _ in range(2):
            output = output_to_console(True)

        return len(re.findall('Nuke Tools', output)) <= 1

    return _clear_output


@pytest.mark.rapidtest
def test_no_clear_output(clear_output):
    """Check if output widget was not cleaned and has different lines of text."""
    assert not clear_output(False)


@pytest.mark.rapidtest
def test_clear_output(clear_output):
    """Check if output widget was cleaned."""
    assert clear_output(True)