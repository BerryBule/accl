#pragma once

#include <memory>
#include <vector>
#include "common/error/error_code.h"
#include "common/log/ops_log.h"

namespace ascend {
namespace ops {

class All2AllOp {
public:
    All2AllOp();
    ~All2AllOp();

    // 初始化算子
    ErrorCode Init(const std::vector<int>& shape, 
                  const std::vector<int>& rank_ids,
                  DataType dtype);

    // 执行算子
    ErrorCode Execute(const void* input, void* output);

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace ops
} // namespace ascend 