"""
Unit and regression test for the dftmp2bench package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import dftmp2bench


def test_dftmp2bench_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "dftmp2bench" in sys.modules
