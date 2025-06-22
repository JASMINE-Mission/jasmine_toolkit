#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Validation tests for the table module '''

import os
from tempfile import NamedTemporaryFile
import numpy as np
from pytest import raises
from astropy.units.core import CompositeUnit, IrreducibleUnit, Unit

from jasmine_toolkit.utils.table import (
    dump_table,
    __table_item_template,
    __items__,
)

UnitType = (Unit, CompositeUnit, IrreducibleUnit)

# Simple validation tests - basic parameter access and consistency
def test_parameter_access():
    ''' Test that all parameters in __items__ are accessible '''

    # This test ensures that all parameters can be accessed without error
    for item in __items__:
        # Should be able to access all required attributes
        name = item.name
        value = item.value
        unit = item.unit
        reference = item.reference

        # Name should be a string
        assert isinstance(name, str)
        assert len(name) > 0

        # Unit should be an astropy Unit instance
        assert isinstance(unit, UnitType), \
            f'Unrecognizable type {type(unit)} assigned to {name}'

        # Reference should be a string (could be empty)
        assert isinstance(reference, str)

        # Value can be various types but should exist
        assert value is not None


def test_parameter_consistency():
    ''' Test consistency of parameter definitions across the system '''

    # All parameters should have non-empty names
    names = [item.name for item in __items__]
    assert all([len(name) > 0 for name in names]), \
        'All parameters should have non-empty names'

    # Names should be unique
    assert len(names) == len(set(names)), \
        'Parameter names should be unique'

    # All parameters should have units (astropy Unit instances)
    units = [item.unit for item in __items__]
    assert all(isinstance(unit, UnitType) for unit in units), \
        'Some items contain unrecognizable unit types'

    # All parameters should have references (even if empty string)
    references = [item.reference for item in __items__]
    assert all(isinstance(ref, str) for ref in references), \
        'Some items contain wrong reference types'


def test_items_list_content():
    ''' Test that __items__ contains expected parameter categories '''

    item_names = [item.name for item in __items__]

    # Should contain telescope parameters
    telescope_params = [
        name for name in item_names
        if 'pupil_diameter' in name or 'f_number' in name
    ]
    assert len(telescope_params) > 0

    # Should contain detector parameters
    detector_params = [
        name for name in item_names
        if 'naxis' in name or 'readout_noise' in name
    ]
    assert len(detector_params) > 0

    # Should contain satellite parameters
    satellite_params = [
        name for name in item_names
        if 'attitude_control' in name
    ]
    assert len(satellite_params) > 0

    # Should contain mission parameters
    mission_params = [name for name in item_names if 'gcs_' in name]
    assert len(mission_params) > 0


# Intermediate tests - output generation and formatting
def test_dump_table_print_output(capsys):
    ''' Test dump_table with print output '''

    # Call with no output file (should print)
    dump_table()

    # Capture printed output
    captured = capsys.readouterr()

    # Should contain header
    assert 'Parameter List' in captured.out
    assert '^Name ^Value ^Units ^Comments^' in captured.out

    # Should contain some parameter data
    assert '|' in captured.out

    # Should contain telescope parameters
    assert 'pupil_diameter' in captured.out or 'f_number' in captured.out


def test_different_value_types():
    ''' Test table generation with different parameter value types '''

    # Find examples of different value types in the parameter list
    float_params = []
    int_params = []
    array_params = []
    other_params = []

    for item in __items__:
        if isinstance(item.value, float):
            float_params.append(item)
        elif isinstance(item.value, (int, np.integer)):
            int_params.append(item)
        elif isinstance(item.value, np.ndarray):
            array_params.append(item)
        else:
            other_params.append(item)

    # Should have at least one of float type
    assert len(float_params) > 0, 'Should have float parameters'

    # Test that we have some parameters (even if not all expected types)
    total_params = (
        len(float_params) + len(int_params) +
        len(array_params) + len(other_params)
    )
    assert total_params == len(__items__), (
        'All parameters should be categorized')

    # Test formatting for each type that exists
    if float_params:
        item = float_params[0]
        result = __table_item_template(
            item.name, item.value, item.unit, item.reference)
        assert '.' in result  # Should have decimal point for floats

    if int_params:
        item = int_params[0]
        result = __table_item_template(
            item.name, item.value, item.unit, item.reference)
        assert item.name in result

    if array_params:
        item = array_params[0]
        result = __table_item_template(
            item.name, item.value, item.unit, item.reference)
        assert item.name in result


def test_table_formatting():
    ''' Test that the table output is properly formatted '''

    with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name

    try:
        # Remove the file so we can test creation
        os.unlink(temp_filename)

        # Dump to file
        dump_table(output=temp_filename)

        # Read and check formatting
        with open(temp_filename, 'r') as f:
            lines = f.readlines()

        # Should have header lines
        assert len(lines) > 3

        # First line should be title
        assert lines[0].strip() == 'Parameter List'

        # Should have empty line after title
        assert lines[1].strip() == ''

        # Header line should have proper DokuWiki format
        assert lines[2].startswith('^')

        # Data lines should start with |
        data_lines = [line for line in lines[3:] if line.strip()]
        for line in data_lines:
            assert line.startswith('|')
            assert line.rstrip().endswith('|')

    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


# File I/O tests - error handling and overwrite behavior
def test_dump_table_file_exists_no_overwrite():
    ''' Test dump_table with existing file and no overwrite '''

    with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name
        f.write('existing content')

    try:
        # Should raise FileExistsError
        with raises(FileExistsError):
            dump_table(output=temp_filename, overwrite=False)

        # File should still contain original content
        with open(temp_filename, 'r') as f:
            content = f.read()
        assert content == 'existing content'

    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_dump_table_file_exists_with_overwrite():
    ''' Test dump_table with existing file and overwrite=True '''

    with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name
        f.write('existing content')

    try:
        # Should succeed with overwrite=True
        dump_table(output=temp_filename, overwrite=True)

        # File should contain new content
        with open(temp_filename, 'r') as f:
            content = f.read()

        assert 'Parameter List' in content
        assert 'existing content' not in content

    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


# Advanced workflow tests - end-to-end scenarios
def test_full_workflow():
    ''' Test the complete workflow from parameter access to file output '''

    with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name

    try:
        # Remove the file
        os.unlink(temp_filename)

        # Generate table
        dump_table(output=temp_filename)

        # Verify file exists and has content
        assert os.path.exists(temp_filename)

        with open(temp_filename, 'r') as f:
            content = f.read()

        # Should contain expected number of parameter entries
        data_lines = [
            line for line in content.split('\n') if line.startswith('|')]
        assert len(data_lines) == len(__items__)

        # Each parameter should appear in the output
        for item in __items__:
            assert item.name in content

    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_output_file_integration():
    ''' Integration test for file output with various scenarios '''

    with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name

    try:
        # Remove the file so we can test creation
        os.unlink(temp_filename)

        # Test 1: Create new file
        dump_table(output=temp_filename)
        assert os.path.exists(temp_filename)

        # Test 2: Read and verify content structure
        with open(temp_filename, 'r') as f:
            original_content = f.read()

        lines = original_content.strip().split('\n')

        # Verify structure
        assert lines[0] == 'Parameter List'
        assert lines[1] == ''
        assert lines[2].startswith('^Name ^Value ^Units ^Comments^')

        # Count data lines
        data_lines = [line for line in lines[3:] if line.startswith('|')]
        assert len(data_lines) == len(__items__)

        # Test 3: Verify we can't overwrite without permission
        with raises(FileExistsError):
            dump_table(output=temp_filename, overwrite=False)

        # Test 4: Verify we can overwrite with permission
        dump_table(output=temp_filename, overwrite=True)

        with open(temp_filename, 'r') as f:
            new_content = f.read()

        # Content should be the same (since parameters haven't changed)
        assert new_content == original_content

    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


# Comprehensive validation tests - system-wide analysis
def test_comprehensive_parameter_validation():
    ''' Comprehensive validation of all parameters in the system '''

    # Test that all expected parameter categories are present
    telescope_count = 0
    detector_count = 0
    satellite_count = 0
    mission_count = 0

    for item in __items__:
        # Categorize parameters
        name_lower = item.name.lower()
        telescope_keywords = [
            'pupil', 'focal', 'spider', 'obscuration', 'field']
        detector_keywords = [
            'naxis', 'channel', 'readout', 'dark', 'sampling']
        satellite_keywords = ['attitude', 'avoidance', 'separation']
        mission_keywords = ['gcs', 'longitude', 'latitude', 'magnitude']

        if any(keyword in name_lower for keyword in telescope_keywords):
            telescope_count += 1
        elif any(keyword in name_lower for keyword in detector_keywords):
            detector_count += 1
        elif any(keyword in name_lower for keyword in satellite_keywords):
            satellite_count += 1
        elif any(keyword in name_lower for keyword in mission_keywords):
            mission_count += 1

    # Verify we have reasonable numbers of each type
    assert telescope_count >= 5, (
        f'Expected at least 5 telescope parameters, got {telescope_count}')
    assert detector_count >= 10, (
        f'Expected at least 10 detector parameters, got {detector_count}')
    assert satellite_count >= 2, (
        f'Expected at least 2 satellite parameters, got {satellite_count}')
    assert mission_count >= 2, (
        f'Expected at least 2 mission parameters, got {mission_count}')
