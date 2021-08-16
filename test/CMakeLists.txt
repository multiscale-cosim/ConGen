###############################################
# Add C++ tests
#add_subdirectory(src_test)

###############################################
# Call the python_unittest_runner on the python test dir
add_test(python_tests "python" "python_unittest_runner.py" "-p"  "./python")

################################################
# Add cython tests, they need environment,
# This is set in the the cython_env test runner
#configure_file(cython_env_test_runner.sh.in cython_env_test_runner.sh)
#add_test(cython_tests bash cython_env_test_runner.sh)
