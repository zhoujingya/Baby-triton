import sys

config.llvm_obj_root = ""
config.llvm_lib_dir = ""
config.llvm_tools_dir = "/bin"
config.cus_build_dir="/home/triton/work/Baby-triton/bin"

import lit.llvm
# lit_config is a global instance of LitConfig
lit.llvm.initialize(lit_config, config)

# test_exec_root: The root path where tests should be run.
config.test_exec_root = os.path.join("/home/triton/work/Baby-triton/test")

# Let the main config do the real work.
lit_config.load_config(config, "/home/triton/work/Baby-triton/test/lit.cfg.py")
