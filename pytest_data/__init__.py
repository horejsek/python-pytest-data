# -*- coding: utf-8 -*-

"""
Useful functions for managing data for pytest fixtures.
"""

from functools import partial
try:
    from itertools import cycle, islice, izip_longest as zip_longest
except ImportError:
    from itertools import cycle, islice, zip_longest

__all__ = ('get_data', 'use_data')


def get_data(request, attribute_name, default_data={}):
    """
    Returns merged data from module, class and function. The most highest
    priority have data nearest to test code. It means that data on function
    have top priority, then class, then module and at last ``default_data``.

    Example of fixture:

    .. code-block:: python

        @pytest.fixture
        def client(request):
            client_data = get_data(reqeust, 'client_data', {'name': 'Jerry', 'address': 'somewhere'})
            return Client(client_data)

    And example how to use data in your test:

    .. code-block:: python

        client_data = {'name': 'Sheldon', 'age': 30}

        class ClientTest:
            client_data = {'iq': 200, 'foo': 'bar'}

            @use_data(client_data={'foo': 'baz'})
            def test_foo(self, client):
                assert client.name == 'Sheldon'
                assert client.address == 'somewhere'
                assert client.age == 30
                assert client.iq == 200
                assert client.foo == 'baz'

    Most of the time you will need only dictionary but sometimes is needed
    list of dictionaries. It is supported as well but you need to know how
    it works. It will find longest list and rest of them will just cycle around.

    .. code-block:: python

        @pytest.fixture
        def clients(request):
            clients_data = get_data(reqeust, 'client_data', {'name': 'Jerry'})
            return [Client(client_data) for client_data in clients_data]

        client_data = [{'age': 20}, {'age': 30}, {'age': 40}]

        @use_data(client_data=[{'foo': 'bar', 'foo': 'baz'}])
        def test_foo(self, clients):
            assert clients[0].name == clients[1].name == clients[2].name
            assert clients[0].age == 20
            assert clients[0].foo == 'bar'
            assert clients[1].age == 30
            assert clients[1].foo == 'baz'
            assert clients[2].age == 40
            assert clients[2].foo == 'bar'
    """
    TARGETS = (request.module, request.cls, request.function)

    if isinstance(default_data, dict):
        getter = partial(_getter, attribute_name=attribute_name, default={})
        data = _merge(default_data, *map(getter, TARGETS))

    elif isinstance(default_data, list):
        getter = partial(_getter, attribute_name=attribute_name, default=[])
        data_list = [default_data] + list(map(getter, TARGETS))
        max_len = max(map(len, data_list))
        data = [_merge(*datas) for datas in islice(zip_longest(*map(cycle, data_list)), max_len)]

    else:
        raise ValueError('{} is not supported'.format(type(default_data)))

    return data


def _getter(target, attribute_name, default):
    """
    Get value of ``attribute_name`` from ``target``. If it's not specified,
    return ``default``. Also check that value is of same type as ``default``.
    """
    value_type = type(default)
    value = getattr(target, attribute_name, default)
    if not isinstance(value, value_type):
        raise ValueError('{}.{} should be {}'.format(target, attribute_name, value_type))
    return value


def _merge(*dicts):
    """
    Merge dictionaries together. Last one have the biggest priority.
    Order should be: default_data, module_data, cls_data, function_data.
    """
    data = {}
    for item in dicts:
        if item:
            data.update(item)
    return data


def use_data(**data):
    """
    Decorator make sexier assaigning of fixture data on function. Instead of
    writing this code:

    .. code-block:: python

        def test_foo():
            pass
        test_foo.client_data = {...}

    you can write this one. It's good that used data are visible on top of
    test function and not somewhere at the end.

    .. code-block:: python

        @use_data(client_data={...})
        def test_foo():
            pass
    """
    def wrapper(func):
        for key, value in data.items():
            setattr(func, key, value)
        return func
    return wrapper
