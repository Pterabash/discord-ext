import os
from blurpo import func


def test_clamp():
    f = func.clamp
    assert f(0) == 1 
    assert f(50) == 50
    assert f(101) == 100


def test_list_attrs():
    class A:
        a = 0
        b = 1
    f = func.list_attrs
    assert f(A, ['a']) == 'a: 0'


def test_subprocess_log():
    f = func.subprocess_log
    t = f(['echo', '0'])
    assert type(t[0]) is str
    assert type(t[1]) is float
    assert t[0] == '0\n'


def test_send_embed():
    r = func.send_embed(
        os.environ['CHANNEL'], ['Test Message'], 
        title='Test Embed', color=0x7289da
    )
    assert r.status_code == 200
