# -*- coding: utf-8 -*-


def pytest_generate_tests(metafunc):
    for key, value in getattr(metafunc.function, 'data', {}).items():
        metafunc.parametrize(key, value, indirect=True)
