import sys

config.llvm_obj_root = "/home/triton/tools/clang16"
config.llvm_lib_dir = "/home/triton/tools/clang16/lib"
config.llvm_tools_dir = "/home/triton/tools/clang16/bin"
config.python_path="/home/triton/work/Baby-triton/.venv/bin"
config.src_dir="/home/triton/work/Baby-triton"
import lit.llvm
# lit_config is a global instance of LitConfig
lit.llvm.initialize(lit_config, config)

# test_exec_root: The root path where tests should be run.
config.test_exec_root = os.path.join("/home/triton/work/Baby-triton/test")

# Let the main config do the real work.
lit_config.load_config(config, "/home/triton/work/Baby-triton/test/lit.cfg.py")
