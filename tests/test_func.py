from dscord import func

def test_clamp():
    c = func.clamp
    assert c(1) is int
    assert c(0) == 1 
    assert c(50) == 50
    assert c(101) == 100

def test_code_wrap():
    w = func.code_wrap
    assert w('test') is list

