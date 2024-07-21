import inspect
import ast

class JIT:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwars):
        fn_src = inspect.getsource(self.fn)
        fn_ast = ast.parse(fn_src)
        print(ast.dump(fn_ast))

def jit(fn):
    return JIT(fn)

@jit
def add():
    print("add")

add()
