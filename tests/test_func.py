from dscord import func


def test_clamp():
    c = func.clamp
    assert c(0) == 1 
    assert c(50) == 50
    assert c(101) == 100
