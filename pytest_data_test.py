# -*- coding: utf-8 -*-

import pytest

from pytest_data import get_data, use_data


def test_only_default():
    data = _get_data({'a': 1})
    assert data == {'a': 1}


def test_module():
    data = _get_data({'a': 1, 'b': 2}, module={'b': 20, 'c': 30})
    assert data == {'a': 1, 'b': 20, 'c': 30}


def test_cls():
    data = _get_data({'a': 1, 'b': 2}, cls={'b': 20, 'c': 30})
    assert data == {'a': 1, 'b': 20, 'c': 30}


def test_function():
    data = _get_data({'a': 1, 'b': 2}, function={'b': 20, 'c': 30})
    assert data == {'a': 1, 'b': 20, 'c': 30}


def test_module_and_cls():
    data = _get_data({'a': 1, 'b': 2}, module={'b': 20, 'c': 30}, cls={'c': 300, 'd': 400})
    assert data == {'a': 1, 'b': 20, 'c': 300, 'd': 400}


def test_module_and_function():
    data = _get_data({'a': 1, 'b': 2}, module={'b': 20, 'c': 30}, function={'c': 300, 'd': 400})
    assert data == {'a': 1, 'b': 20, 'c': 300, 'd': 400}


def test_cls_and_function():
    data = _get_data({'a': 1, 'b': 2}, cls={'b': 20, 'c': 30}, function={'c': 300, 'd': 400})
    assert data == {'a': 1, 'b': 20, 'c': 300, 'd': 400}


def test_module_and_cls_and_function():
    data = _get_data({'a': 1, 'b': 2}, module={'b': 20, 'c': 30}, cls={'c': 300, 'd': 400}, function={'d': 4000, 'e': 5000})
    assert data == {'a': 1, 'b': 20, 'c': 300, 'd': 4000, 'e': 5000}


def test_list_only_default():
    data = _get_data([{'a': 1}])
    assert data == [{'a': 1}]


def test_list_mix_raises_module():
    with pytest.raises(ValueError):
        _get_data({'a': 1}, module=[{'b': 20}])
    with pytest.raises(ValueError):
        _get_data([{'a': 1}], module={'b': 20})


def test_list_mix_raises_cls():
    with pytest.raises(ValueError):
        _get_data({'a': 1}, cls=[{'b': 20}])
    with pytest.raises(ValueError):
        _get_data([{'a': 1}], cls={'b': 20})


def test_list_mix_raises_function():
    with pytest.raises(ValueError):
        _get_data({'a': 1}, function=[{'b': 20}])
    with pytest.raises(ValueError):
        _get_data([{'a': 1}], function={'b': 20})


def test_list_module():
    data = _get_data([{'a': 1, 'b': 2}], module=[{'b': 20, 'c': 30}])
    assert data == [{'a': 1, 'b': 20, 'c': 30}]


def test_list_cls():
    data = _get_data([{'a': 1, 'b': 2}], cls=[{'b': 20, 'c': 30}])
    assert data == [{'a': 1, 'b': 20, 'c': 30}]


def test_list_function():
    data = _get_data([{'a': 1, 'b': 2}], function=[{'b': 20, 'c': 30}])
    assert data == [{'a': 1, 'b': 20, 'c': 30}]


def test_list_more_values_module():
    data = _get_data([{'a': 1, 'b': 2}], module=[{'b': 20, 'c': 30}, {'b': 21, 'c': 31}])
    assert data == [{'a': 1, 'b': 20, 'c': 30}, {'a': 1, 'b': 21, 'c': 31}]


def test_list_more_values_cls():
    data = _get_data([{'a': 1, 'b': 2}], cls=[{'b': 20, 'c': 30}, {'b': 21, 'c': 31}])
    assert data == [{'a': 1, 'b': 20, 'c': 30}, {'a': 1, 'b': 21, 'c': 31}]


def test_list_more_values_function():
    data = _get_data([{'a': 1, 'b': 2}], function=[{'b': 20, 'c': 30}, {'b': 21, 'c': 31}])
    assert data == [{'a': 1, 'b': 20, 'c': 30}, {'a': 1, 'b': 21, 'c': 31}]


def test_list_more_values_module_and_cls():
    data = _get_data(
        [{'a': 1, 'b': 2}],
        module=[{'b': 20, 'c': 30}, {'b': 21, 'c': 31}],
        cls=[{'c': 300, 'd': 400}],
    )
    assert data == [
        {'a': 1, 'b': 20, 'c': 300, 'd': 400},
        {'a': 1, 'b': 21, 'c': 300, 'd': 400},
    ]


def test_list_more_values_module_and_function():
    data = _get_data(
        [{'a': 1, 'b': 2}],
        module=[{'b': 20, 'c': 30}, {'b': 21, 'c': 31}, {'b': 22, 'c': 32}],
        function=[{'c': 300, 'd': 400}, {'c': 301, 'd': 401}],
    )
    assert data == [
        {'a': 1, 'b': 20, 'c': 300, 'd': 400},
        {'a': 1, 'b': 21, 'c': 301, 'd': 401},
        {'a': 1, 'b': 22, 'c': 300, 'd': 400},
    ]


def test_list_more_values_cls_and_function():
    data = _get_data(
        [{'a': 10, 'b': 20}, {'a': 11, 'b': 21}],
        cls=[{'b': 200, 'c': 300}],
        function=[{'c': 3000, 'd': 4000}, {'c': 3001, 'd': 4001}],
    )
    assert data == [
        {'a': 10, 'b': 200, 'c': 3000, 'd': 4000},
        {'a': 11, 'b': 200, 'c': 3001, 'd': 4001},
    ]


def test_list_more_values_module_cls_and_function():
    data = _get_data(
        [{'a': 10, 'b': 20}, {'a': 11, 'b': 21}],
        module=[{'b': 200, 'c': 300}, {'b': 201, 'c': 301}, {'b': 202, 'c': 302}],
        cls=[{'c': 3000, 'd': 4000}],
        function=[{'d': 40000, 'e': 50000}, {'d': 40001, 'e': 50001}],
    )
    assert data == [
        {'a': 10, 'b': 200, 'c': 3000, 'd': 40000, 'e': 50000},
        {'a': 11, 'b': 201, 'c': 3000, 'd': 40001, 'e': 50001},
        {'a': 10, 'b': 202, 'c': 3000, 'd': 40000, 'e': 50000},
    ]


def _get_data(default, module=None, cls=None, function=None):
    class request:
        class module:
            if module:
                foo = module
        class cls:
            if cls:
                foo = cls
        class function:
            if function:
                foo = function

    return get_data(request, 'foo', default)


def test_use_data_func_stays_same():
    def func():
        pass
    res_func = use_data(foo=42)(func)
    assert res_func == func


def test_use_data_func_has_data():
    def func():
        pass
    res_func = use_data(foo=42)(func)
    assert res_func.foo == 42
