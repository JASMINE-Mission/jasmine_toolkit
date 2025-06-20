#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the table module '''

import os
from tempfile import NamedTemporaryFile
import numpy as np
from pytest import raises

from jasmine_toolkit.utils.table import (
    dump_table,
    setup_parser,
    __table_header,
    __table_item_template,
    __items__,
)


def test_table_header():
    ''' Test the table header generation '''

    header = __table_header()

    # Should contain expected DokuWiki format
    assert 'Parameter List' in header
    assert '^Name ^Value ^Units ^Comments^' in header
    assert header.endswith('\n')


def test_table_item_template_float():
    ''' Test table item template with float values '''

    name = 'test_param'
    value = 3.14159
    unit = 'm'
    ref = 'test reference'

    result = __table_item_template(name, value, unit, ref)

    # Should format float with 2 decimal places
    assert '3.14' in result
    assert name in result
    assert unit in result
    assert ref in result
    assert result.startswith('|')
    assert result.endswith('|\n')


def test_table_item_template_int():
    ''' Test table item template with integer values '''

    name = 'test_param'
    value = 42
    unit = 'pixels'
    ref = 'test reference'

    result = __table_item_template(name, value, unit, ref)

    assert '42' in result
    assert name in result
    assert unit in result
    assert ref in result


def test_table_item_template_string():
    ''' Test table item template with string values '''

    name = 'test_param'
    value = 'test_value'
    unit = ''
    ref = 'test reference'

    result = __table_item_template(name, value, unit, ref)

    assert 'test_value' in result
    assert name in result
    assert ref in result


def test_table_item_template_array():
    ''' Test table item template with numpy array values '''

    name = 'test_param'
    value = np.array([1, 2, 3])
    unit = 'm'
    ref = 'test reference'

    result = __table_item_template(name, value, unit, ref)

    # Array should be converted to string
    assert '[1 2 3]' in result
    assert name in result
    assert unit in result
    assert ref in result


def test_items_list_exists():
    ''' Test that the __items__ list is properly defined '''

    # Should be a list
    assert isinstance(__items__, list)

    # Should not be empty
    assert len(__items__) > 0

    # All items should have required attributes
    for item in __items__:
        assert hasattr(item, 'name')
        assert hasattr(item, 'value')
        assert hasattr(item, 'unit')
        assert hasattr(item, 'reference')


def test_dump_table_file_output():
    ''' Test dump_table with file output '''

    with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name

    try:
        # Remove the file so we can test creation
        os.unlink(temp_filename)

        # Dump to file
        dump_table(output=temp_filename)

        # Check file was created
        assert os.path.exists(temp_filename)

        # Check file content
        with open(temp_filename, 'r') as f:
            content = f.read()

        assert 'Parameter List' in content
        assert '^Name ^Value ^Units ^Comments^' in content
        assert '|' in content

    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_setup_parser():
    ''' Test the setup_parser function '''

    from argparse import ArgumentParser

    parser = ArgumentParser()
    setup_parser(parser)

    # Test parsing with no arguments
    args = parser.parse_args([])
    assert args.output is None
    assert args.overwrite is False

    # Test parsing with output file
    args = parser.parse_args(['output.txt'])
    assert args.output == 'output.txt'
    assert args.overwrite is False

    # Test parsing with overwrite flag
    args = parser.parse_args(['-f', 'output.txt'])
    assert args.output == 'output.txt'
    assert args.overwrite is True

    # Test parsing with long overwrite flag
    args = parser.parse_args(['--overwrite', 'output.txt'])
    assert args.output == 'output.txt'
    assert args.overwrite is True
