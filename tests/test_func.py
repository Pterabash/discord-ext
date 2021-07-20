from descord import func

def test_clamp():
    assert func.clamp(50) == 50
    assert func.clamp(0) == 1
    assert func.clamp(101) == 100

def test_code_wrap():
    assert len(func.code_wrap('0'*1950)) != 1
