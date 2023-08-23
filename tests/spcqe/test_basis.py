import unittest
import numpy as np
import sys
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent
sys.path.append(PROJECT_PATH / "src")
from spcqe.functions import basis, basis_3, basis_2


class TestBasis(unittest.TestCase):
    def test_basis_3(self):
        basis_a = basis(3, 100, [11, 17, 23])
        basis_b = basis_3(3, 100, 11, 17, 23)
        np.testing.assert_array_equal(basis_a, basis_b)

    def test_basis_2(self):
        basis_a = basis(3, 100, [11, 17])
        basis_b = basis_3(3, 100, 11, 17)
        np.testing.assert_array_equal(basis_a, basis_b)
