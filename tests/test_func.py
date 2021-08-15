from dscord import func

def test_clamp():
    c = func.clamp
    assert c(0) == 1 
    assert c(50) == 50
    assert c(101) == 100

def test_code_wrap():
    w = func.code_wrap
    h, t = '```\n', '\n```'
    a, f = 'abcde', 'f'
    assert w(a, 5) == [h+a+t]
    assert w(a+f, 5) == [h+x+t for x in [a,f]]

