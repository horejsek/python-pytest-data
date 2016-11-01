# -*- coding: utf-8 -*-

"""
Useful functions for managing data for pytest fixtures.
"""

from functools import partial
try:
    from itertools import cycle, islice, izip_longest as zip_longest
except ImportError:
    from itertools import cycle, islice, zip_longest

__all__ = ('get_data', 'use_data', 'use_data_parametrize')


def get_data(request, attribute_name, default_data={}):
    """
    Returns merged data from module, class and function. The most highest
    priority have data nearest to test code. It means that data on function
    have top priority, then class, then module, then param of request
    and at last ``default_data``.

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

    It also works with parametrized fixture. Following fixture will then call each
    test twice for two different types of user and you are still able to modify some
    data of user when needed:

    .. code-block:: python

        @pytest.fixture(params=[{'registred': True}, {'registred': False}])
        def user(request):
            user_data = get_dat(request, 'user_data', {'name': 'Jerry'})
            return User(user_data)
    """
    TARGETS = (request.module, request.cls, request.function)

    if isinstance(default_data, dict):
        getter = partial(_getter, attribute_name=attribute_name, default={})
        dicts = [default_data] + list(map(getter, TARGETS)) + [_getter(request, 'param', {})]
        data = _merge(*dicts)

    elif isinstance(default_data, list):
        getter = partial(_getter, attribute_name=attribute_name, default=[])
        dicts = [default_data] + list(map(getter, TARGETS)) + [_getter(request, 'param', [])]
        max_len = max(map(len, dicts))
        data = [_merge(*datas) for datas in islice(zip_longest(*map(cycle, dicts)), max_len)]

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

    .. versionchanged:: 0.3
        ``use_data`` can be used only for tests, not fixtures. So since version 0.3
        there is check that it's used only with tests (function starts with `test`).
    """
    def wrapper(func):
        assert func.__name__.startswith('test'), 'use_data can be used only for tests'

        for key, value in data.items():
            setattr(func, key, value)
        return func
    return wrapper


def use_data_parametrize(**data):
    """
    :py:func:`use_data` mixed with pytest's parametrize. The best way how to
    descrabe it is to show some code:

    .. code-block:: python

        @use_data_parametrize(client=[{...}, {...}], user=[{...}, {...}])
        def test_foo(client, user):
            assert 0

        @pytest.fixture
        def client(request):
            return get_data(request, 'client_data', {...})

        @pytest.fixture
        def user(request):
            return get_data(request, 'user_data', {...})

    And it will call test ``test_foo`` four times, for every combination of
    client and user. As you would expect by pytest's mark parametrize.

    .. code-block:: none

        ========= FAILURES ==========
        -- test_foo[client0-user0] --
        -- test_foo[client0-user1] --
        -- test_foo[client1-user0] --
        -- test_foo[client1-user1] --

    Just note that in :py:func:`use_data` is used as key ``atribute_name``
    defined in fixture by calling :py:func:`get_data` whereas here is used
    fixture name. Because pytest need to assign params to fixtures. Data passed
    to this method is then found in fixture's ``request.param`` instead of
    ``request.function.attribute_name``.

    .. versionadded:: 0.2
    """
    def wrapper(func):
        func.data = data
        return func
    return wrapper
