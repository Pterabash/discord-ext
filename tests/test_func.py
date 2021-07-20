from descord import func

def test_clamp():
    assert func.clamp(50) == 50
    assert func.clamp(0) == 1
    assert func.clamp(101) == 100

def test_code_wrap():
    assert len(func.code_wrap('x'*1950)) == 1
    assert len(func.code_wrap('x'*3900)) == 2

def test_log_proc():
    assert len(func.log_proc(['echo', 'Hello Bash!']) == 'Hello Bash!'
