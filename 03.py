import inspect
import ast

class JIT:
    def __init__(self, fn, target="cpu"):
        self.fn = fn
        self.target = target

    def __call__(self, *args, **kwars):
        fn_src = inspect.getsource(self.fn)
        fn_ast = ast.parse(fn_src)
        print(ast.dump(fn_ast))
        code_generator = CodeGenerator(fn_ast, self.target)
        code_generator.code_gen()

def jit(target="cpu"):
    assert(target in ["cpu", "gpu"]) # any other target
    def inner_jit(fn):
        return JIT(fn, target)
    return inner_jit

class CodeGenerator(ast.NodeVisitor):
  def __init__(self, fn_ast, target):
      self.fn_ast = fn_ast
      self.target = target

  def code_gen(self):
      self.visit(self.fn_ast)

  def visit(self, Node: ast.Module):
      print("Visit: " + Node.__class__.__name__)
      return super().visit(Node)

@jit(target="cpu")
def add():
    print("add")

add()
