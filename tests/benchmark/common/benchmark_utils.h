#pragma once

#include <vector>
#include <string>
#include <chrono>
#include <mpi.h>

namespace benchmark {

class BenchmarkUtils {
public:
    // 初始化MPI环境
    static void InitMPI(int* argc, char*** argv);
    
    // 清理MPI环境
    static void FinalizeMPI();
    
    // 获取当前进程的rank
    static int GetRank();
    
    // 获取总进程数
    static int GetSize();
    
    // 生成测试数据
    static std::vector<float> GenerateTestData(size_t size);
    
    // 验证结果正确性
    static bool VerifyResults(const std::vector<float>& expected, 
                            const std::vector<float>& actual,
                            float tolerance = 1e-5);
    
    // 测量执行时间
    static double MeasureTime(std::function<void()> func, int iterations = 1);
    
    // 同步所有进程
    static void Synchronize();
    
    // 打印性能结果
    static void PrintPerformanceResults(const std::string& op_name,
                                      double time_ms,
                                      size_t data_size_bytes);
};

} // namespace benchmark 