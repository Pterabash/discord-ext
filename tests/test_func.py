import os
from dscord import func


def test_clamp():
    f = func.clamp
    assert f(0) == 1 
    assert f(50) == 50
    assert f(101) == 100

def test_send_embed():
    r = func.send_embed(
        os.environ['CHANNEL'], 'Test Message', title='Test Embed'
    )
    assert r == 200