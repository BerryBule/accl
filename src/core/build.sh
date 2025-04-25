#!/bin/bash

# 设置编译环境变量
export ASCEND_OPP_PATH=/usr/local/Ascend/ascend-toolkit/latest/opp
export TOOLCHAIN_HOME=/usr/local/Ascend/ascend-toolkit/latest/toolkit
export LD_LIBRARY_PATH=${TOOLCHAIN_HOME}/lib64:${LD_LIBRARY_PATH}

# 创建编译目录
mkdir -p build
cd build

# 配置CMake
cmake .. \
    -DCMAKE_CXX_COMPILER=${TOOLCHAIN_HOME}/bin/aarch64-linux-gnu-g++ \
    -DCMAKE_BUILD_TYPE=Release \
    -DASCEND_OPP_PATH=${ASCEND_OPP_PATH}

# 编译
make -j$(nproc)

# 复制生成的库文件到指定位置
cp libcust_opapi.so ../lib/

cd .. 