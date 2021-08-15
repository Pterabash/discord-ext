from dscord import func

def test_clamp():
    c = func.clamp
    assert c(0) == 1 
    assert c(50) == 50
    assert c(101) == 100

def test_code_wrap():
    w = func.code_wrap
    x = 'x' * 1950
    y, z = x + 'x', x * 2
    assert w(x) = [x]
    assert w(y) = [x, 'x']
    assert w(z) = [x, x]

