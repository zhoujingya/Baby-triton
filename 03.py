import inspect
import ast
from tvm.script.ir_builder import relax as relax_builder, ir as I, IRBuilder as IB
def jit(target="cpu"):
    assert target in ["cpu", "gpu"]
    def inner(fn):
        return JIT(fn, target=target)
    return inner

class JIT:
    def __init__(self, fn, target="cpu"):
        self.fn = fn
        self.target = target

    def __call__(self, *args, **kwargs):
        fn_src = inspect.getsource(self.fn)
        fn_ast = ast.parse(fn_src)
        print(ast.dump(fn_ast))
        code_generator = CodeGenerator(fn_ast, self.target)
        code_generator.code_gen()

class CodeGenerator(ast.NodeVisitor):
    def __init__(self, fn_ast, target):
        self.fn_ast = fn_ast
        self.target = target
        self.ib = IB()
        self.ir_module = None

    def code_gen(self):
        with self.ib:
            self.visit(self.fn_ast)
        module = self.ib.get()
        print(module)


    def visit(self, node):
        print("Visit " + node.__class__.__name__)
        return super().visit(node)

    def visit_Module(self, node: ast.Module):
        if self.ir_module:
            raise AssertionError("We should have only one module!")
        self.ir_module = I.ir_module()
        with self.ir_module:
            super().generic_visit(node)


    def visit_FunctionDef(self, node: ast.FunctionDef):
        pass

    def generic_visit(self, node: ast.AST):
        raise NotImplementedError("Unsupported AST node type: {}".format(type(node).__name__))


@jit(target="cpu")
def add():
    print("add")

add()
