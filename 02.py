import inspect
import ast

def jit(fn):
    def inner():
        fn_src = inspect.getsource(fn)
        fn_ast = ast.parse(fn_src)
        print(ast.dump(fn_ast))
    return inner

@jit
def add():
    print("add")

add()
