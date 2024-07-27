enable_testing()
configure_file(lit.site.cfg.py.in lit.site.cfg.py @ONLY)
configure_file(lit.site.cfg.py.in ${CMAKE_CURRENT_SOURCE_DIR}/lit.site.cfg.py @ONLY)
add_test(NAME baby-triton-test COMMAND lit ${CMAKE_BINARY_DIR})
