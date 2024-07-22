#!env bash
mkdir -p tvm/build || true

cp tvm/configs/config.cmake tvm/build/config.cmake || true

export TVM_LOG_DEBUG="ir/transform.cc=1,relay/ir/transform.cc=1"

cmake -S tvm -B tvm/build -GNinja \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++

ninja -C tvm/build
