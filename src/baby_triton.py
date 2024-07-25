import inspect
import ast
from typing import Dict, Any
from tvm import relax as rx
from tvm.script import relax as R
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
        # print(ast.dump(fn_ast))
        code_generator = CodeGenerator(fn_ast, self.target)
        code_generator.code_gen()


class CodeGenerator(ast.NodeVisitor):
    def __init__(self, fn_ast, target):
        self.fn_ast = fn_ast
        self.target = target
        self.ib = IB()
        self.ir_module = None
        self.entry = None
        self.ret = None
        self.local_var_table: Dict[str, Any] = {}

    def code_gen(self):
        with self.ib:
            self.visit(self.fn_ast)
        module = self.ib.get()
        print(module)

    def visit(self, node):
        # print("Visit " + node.__class__.__name__)
        return super().visit(node)

    def visit_Module(self, node: ast.Module):
        if self.ir_module:
            raise AssertionError("We should have only one module!")
        self.ir_module = I.ir_module()
        with self.ir_module:
            super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        fn = relax_builder.function()
        self.entry = node.name
        with fn:
            R.func_name(node.name)
            self._visit_compound_stmt(node.body)
            if self.ret is None:
                R.func_ret_value(rx.ShapeExpr([]))
            else:
                R.func_ret_value(self.ret)

    def visit_Pass(self, node: ast.Pass):
        pass

    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) != 1:
            raise NotImplementedError(
                "Doesn't support simultaneous multiple assignment like 'a = b = c' in AST node type: {}".format(
                    type(node).__name__
                )
            )
        target: rx.Var = self.visit(node.targets[0])
        value = self.visit(node.value)
        self.local_var_table[target.name_hint] = value
        self.ib.name(target.name_hint, value)

    def visit_Name(self, node: ast.Name):
        name = node.id
        if isinstance(node.ctx, ast.Store):
            if name not in self.local_var_table.keys():
                self.local_var_table[name] = rx.Var(
                    name, struct_info=rx.ObjectStructInfo()
                )
        return self.local_var_table[name]

    def visit_BinOp(self, node: ast.BinOp):
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        return R.emit(self._binOp_maker(node.op)(lhs, rhs))

    def visit_Return(self, node: ast.Return):
        ret_value = self.visit(node.value)
        return ret_value

    def visit_Constant(self, node: ast.Constant):
        return R.emit(rx.const(node.value))

    def _visit_compound_stmt(self, stmts):
        assert isinstance(stmts, (list, tuple))
        for stmt in stmts:
            ret = self.visit(stmt)
            if ret is not None and isinstance(stmt, ast.Return):
                self.ret = ret

    def _binOp_maker(self, node: ast.operator):
        if isinstance(node, ast.Add):
            return R.add
        else:
            raise NotImplementedError(
                "Unsupported AST node type: {}".format(type(node).__name__)
            )

    def generic_visit(self, node: ast.AST):
        raise NotImplementedError(
            "Unsupported AST node type: {}".format(type(node).__name__)
        )
