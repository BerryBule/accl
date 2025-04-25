cmake_minimum_required(VERSION 3.14)
project(cust_opapi)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 设置编译选项
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -fPIC")

# 添加头文件目录
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${ASCEND_OPP_PATH}/include
)

# 添加源文件
file(GLOB_RECURSE SOURCES 
    "operators/*.cpp"
    "common/*.cpp"
    "kernel/*.cpp"
)

# 创建动态库
add_library(cust_opapi SHARED ${SOURCES})

# 设置库的属性
set_target_properties(cust_opapi PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    OUTPUT_NAME "cust_opapi"
)

# 链接依赖库
target_link_libraries(cust_opapi
    PRIVATE
    ascend_opp
    ascend_runtime
)

# 安装规则
install(TARGETS cust_opapi
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

# 安装头文件
install(DIRECTORY include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
) 