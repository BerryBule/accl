# 查找OpenMPI
find_package(MPI REQUIRED)

# 添加common库
add_library(benchmark_common
    common/benchmark_utils.cpp
)

target_include_directories(benchmark_common
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${MPI_INCLUDE_PATH}
)

target_link_libraries(benchmark_common
    PUBLIC
    ${MPI_LIBRARIES}
)

# 添加OpenMPI基准测试
add_executable(openmpi_all2all_benchmark
    openmpi/all2all_benchmark.cpp
)

target_link_libraries(openmpi_all2all_benchmark
    PRIVATE
    benchmark_common
)

# 添加AscendOps基准测试
add_executable(ascend_ops_all2all_benchmark
    ascend_ops/all2all_benchmark.cpp
)

target_link_libraries(ascend_ops_all2all_benchmark
    PRIVATE
    benchmark_common
    ascend_ops
) 