import json
import os
import pytest
import yaml


def is_req_satisfied(*args):
    return False


@pytest.mark.parametrize(('minimum_ver', 'current', 'desired_bool'), [
    ("1.10.0", "1.10.0", True),
    ("1.10.0", "1.10.1", True),
    ("1.10.0", "1.12.0", True),
    ("1.10.0", "2.0.0", True),
    ("1.10.0", "1.9.9", False),
    ("1.10.0", "0.9.9", False),
    ("1.10.1", "1.10.0", False)
])
def test_is_req_satisfied(minimum_ver, current, desired_bool):
        assert desired_bool == is_req_satisfied(minimum_ver, current)


def simple_read(some_file):
    with open(some_file) as f:
        return f.read()


def param_read(some_file):
    try:
        with open(some_file) as f:
            if some_file.endswith('txt'):
                return f.read()
            elif some_file.endswith('json'):
                return json.load(f).get('message')
            elif some_file.endswith('yaml'):
                return yaml.load(f).get('mEssage')
            else:
                raise TypeError("I don't know how to read this file!")
    except IOError:
        raise


@pytest.fixture
def simple_file(tmpdir):
    p = tmpdir.mkdir('foo').join('bar.txt')
    p.write('Fixtures improve tests')
    return p.strpath


def test_simple_fixture(simple_file):
    assert simple_read(simple_file) == 'Fixtures improve tests'


APPROVED_EXTS = [".txt", ".json", ".yaml"]


@pytest.fixture(params=APPROVED_EXTS + [".unknown"])
def param_file(request, tmpdir):
    file_type = request.param
    message = 'Fixtures improve tests'
    p = tmpdir.mkdir('foo').join('bar{}'.format(file_type))
    if file_type == '.txt':
        p.write(message)
    elif file_type == '.json':
        p.write(json.dumps({'message': message}))
    elif file_type == '.yaml':
        p.write(yaml.dump({'mEssage': message}))
    else:
        p.write('Unknown file type')
    return p.strpath


def test_param_fixture(param_file):
    if os.path.splitext(param_file)[-1] not in APPROVED_EXTS:
        with pytest.raises(TypeError):
           param_read(param_file)
    else:
        assert param_read(param_file) == 'Fixtures improve tests'


@pytest.fixture(params=['api_v1', 'api_v2'])
def finalizer_fixture(request):

    def _cleanup_something():
        raise ZeroDivisionError

    request.addfinalizer(_cleanup_something)
    return request.param


def test_show_finalizer(finalizer_fixture):
    assert True


@pytest.fixture(params=['North', 'East', 'West', 'South'])
def direction(request):
    return request.param


@pytest.fixture(params=['Carolina', 'Dakota'])
def state(request):
    return request.param


@pytest.yield_fixture
def composed_fixture(direction, state):
    directory = '/tmp/states/{} {}'.format(direction, state)
    try:
        os.makedirs(directory)
        yield directory
    finally:
        os.rmdir(directory)


def test_directional_state(composed_fixture):
    assert os.path.exists(composed_fixture)
    assert len(os.listdir('/tmp/states')) == 1
