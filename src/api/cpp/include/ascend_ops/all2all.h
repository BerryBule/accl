#pragma once

#include <vector>
#include <memory>
#include "aclnn_all2all.h"

namespace ascend {
namespace ops {

class All2AllOp {
public:
    All2AllOp();
    ~All2AllOp();

    /**
     * @brief 初始化All2All算子
     * @param shape 输入shape
     * @param rank_ids 参与通信的rank列表
     * @param dtype 数据类型
     * @return 0表示成功，非0表示失败
     */
    int Init(const std::vector<int32_t>& shape,
            const std::vector<int32_t>& rank_ids,
            aclDataType dtype);

    /**
     * @brief 执行All2All操作
     * @param input 输入数据
     * @param output 输出数据
     * @param stream 计算流
     * @return 0表示成功，非0表示失败
     */
    int Execute(const void* input,
               void* output,
               aclrtStream stream);

private:
    aclnnAll2AllDesc desc_;
    bool initialized_;
};

} // namespace ops
} // namespace ascend 