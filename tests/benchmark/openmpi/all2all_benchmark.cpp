#include "../common/benchmark_utils.h"
#include <mpi.h>
#include <vector>
#include <iostream>

using namespace benchmark;

void RunOpenMPIAll2All(const std::vector<float>& input, std::vector<float>& output) {
    int rank = BenchmarkUtils::GetRank();
    int size = BenchmarkUtils::GetSize();
    
    // 计算每个进程的数据大小
    size_t local_size = input.size();
    std::vector<int> recv_counts(size, local_size);
    std::vector<int> recv_displs(size);
    
    for (int i = 0; i < size; ++i) {
        recv_displs[i] = i * local_size;
    }
    
    // 执行All2All操作
    MPI_Alltoallv(input.data(), 
                  recv_counts.data(), 
                  recv_displs.data(),
                  MPI_FLOAT,
                  output.data(),
                  recv_counts.data(),
                  recv_displs.data(),
                  MPI_FLOAT,
                  MPI_COMM_WORLD);
}

int main(int argc, char** argv) {
    // 初始化MPI
    BenchmarkUtils::InitMPI(&argc, &argv);
    
    int rank = BenchmarkUtils::GetRank();
    int size = BenchmarkUtils::GetSize();
    
    // 生成测试数据
    const size_t data_size = 1024 * 1024; // 1M个float
    auto input_data = BenchmarkUtils::GenerateTestData(data_size);
    std::vector<float> output_data(data_size);
    
    // 预热
    RunOpenMPIAll2All(input_data, output_data);
    
    // 同步所有进程
    BenchmarkUtils::Synchronize();
    
    // 执行基准测试
    const int iterations = 10;
    double total_time = 0.0;
    
    for (int i = 0; i < iterations; ++i) {
        double time = BenchmarkUtils::MeasureTime(
            [&]() { RunOpenMPIAll2All(input_data, output_data); }
        );
        total_time += time;
        
        // 验证结果
        if (i == 0) {
            bool is_correct = BenchmarkUtils::VerifyResults(input_data, output_data);
            if (rank == 0) {
                std::cout << "Result verification: " 
                         << (is_correct ? "PASSED" : "FAILED") << std::endl;
            }
        }
    }
    
    // 计算平均时间
    double avg_time = total_time / iterations;
    
    // 打印性能结果
    size_t data_size_bytes = data_size * sizeof(float);
    BenchmarkUtils::PrintPerformanceResults("OpenMPI All2All", avg_time, data_size_bytes);
    
    // 清理MPI
    BenchmarkUtils::FinalizeMPI();
    return 0;
} 