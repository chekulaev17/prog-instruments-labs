"""
Общие фикстуры для тестов.
"""
import pytest
import numpy as np


@pytest.fixture
def sample_parameters():
    """Фикстура с параметрами для генерации выборки."""
    return {
        'a': 1.0,
        'sigma': np.sqrt(2.0),
        'n': 10,
        'seed': 42
    }


@pytest.fixture
def ci_parameters():
    """Фикстура с параметрами для доверительных интервалов."""
    return {
        'x_bar': 5.0,
        'sigma': 2.0,
        's': 2.1,
        'n': 30,
        'gamma': 0.95
    }