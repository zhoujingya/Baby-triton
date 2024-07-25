
import os
import platform

import lit.formats
# Global instance of LLVMConfig provided by lit
from lit.llvm import llvm_config
from lit.llvm.subst import ToolSubst
config.name = 'BABY-TRITON'
config.test_format = lit.formats.ShTest(not llvm_config.use_lit_shell)
# suffixes: A list of file extensions to treat as test files. This is overriden
# by individual lit.local.cfg files in the test subdirectories.
config.suffixes = ['.py','.c', '.cpp', 'cc']

# test_source_root: The root path where tests are located.
config.test_source_root = os.path.dirname(__file__)

# The list of tools required for testing - prepend them with the path specified
# during configuration (i.e. LT_LLVM_TOOLS_DIR/bin)
tools = ["opt", "lli","clang", "FileCheck"]
python = ["python3"]
llvm_config.add_tool_substitutions(tools, config.llvm_tools_dir)
llvm_config.add_tool_substitutions(python, config.python_path)
llvm_config.with_environment('PYTHONPATH', [
    os.path.join(config.src_dir,""),os.path.join(config.src_dir,"tvm","python"),
], append_path=True)
