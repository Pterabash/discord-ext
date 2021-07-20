from descord import func

def test_clamp():
    assert func.clamp(50) == 50
    assert func.clamp(0) == 1
    assert func.clamp(101) == 100

def test_code_wrap():
    xs = 'x'*1950
    assert len(func.code_wrap(xs)) == 1
    assert len(func.code_wrap(xs+' '+xs)) == 2

def test_log_proc():
    assert func.log_proc(['echo', 'Hello Bash!']) != []
