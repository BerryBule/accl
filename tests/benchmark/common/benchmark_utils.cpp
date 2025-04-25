#include "benchmark_utils.h"
#include <random>
#include <iostream>
#include <iomanip>
#include <algorithm>

namespace benchmark {

void BenchmarkUtils::InitMPI(int* argc, char*** argv) {
    MPI_Init(argc, argv);
}

void BenchmarkUtils::FinalizeMPI() {
    MPI_Finalize();
}

int BenchmarkUtils::GetRank() {
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    return rank;
}

int BenchmarkUtils::GetSize() {
    int size;
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    return size;
}

std::vector<float> BenchmarkUtils::GenerateTestData(size_t size) {
    std::vector<float> data(size);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dis(-1.0f, 1.0f);
    
    for (size_t i = 0; i < size; ++i) {
        data[i] = dis(gen);
    }
    return data;
}

bool BenchmarkUtils::VerifyResults(const std::vector<float>& expected,
                                 const std::vector<float>& actual,
                                 float tolerance) {
    if (expected.size() != actual.size()) {
        return false;
    }
    
    for (size_t i = 0; i < expected.size(); ++i) {
        if (std::abs(expected[i] - actual[i]) > tolerance) {
            return false;
        }
    }
    return true;
}

double BenchmarkUtils::MeasureTime(std::function<void()> func, int iterations) {
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < iterations; ++i) {
        func();
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    return duration.count() / 1000.0; // 转换为毫秒
}

void BenchmarkUtils::Synchronize() {
    MPI_Barrier(MPI_COMM_WORLD);
}

void BenchmarkUtils::PrintPerformanceResults(const std::string& op_name,
                                           double time_ms,
                                           size_t data_size_bytes) {
    int rank = GetRank();
    if (rank == 0) {
        double bandwidth = (data_size_bytes / 1024.0 / 1024.0) / (time_ms / 1000.0); // MB/s
        std::cout << std::fixed << std::setprecision(2)
                  << "Operation: " << op_name << "\n"
                  << "Time: " << time_ms << " ms\n"
                  << "Bandwidth: " << bandwidth << " MB/s\n"
                  << "Data size: " << (data_size_bytes / 1024.0 / 1024.0) << " MB\n"
                  << std::endl;
    }
}

} // namespace benchmark 