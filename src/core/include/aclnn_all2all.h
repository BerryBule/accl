#pragma once

#include <stdint.h>
#include "acl/acl.h"
#include "acl/acl_op_compiler.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief All2All算子的输入参数结构体
 */
typedef struct aclnnAll2AllDesc {
    aclDataType dtype;           // 数据类型
    int32_t* shape;             // 输入shape
    int32_t shape_size;         // shape数组大小
    int32_t* rank_ids;          // 参与通信的rank列表
    int32_t rank_size;          // rank列表大小
} aclnnAll2AllDesc;

/**
 * @brief All2All算子执行函数
 * @param desc 算子描述
 * @param input 输入数据
 * @param output 输出数据
 * @param stream 计算流
 * @return ACL_ERROR_NONE 成功，其他值表示失败
 */
aclError aclnnAll2All(const aclnnAll2AllDesc* desc,
                     const void* input,
                     void* output,
                     aclrtStream stream);

#ifdef __cplusplus
}
#endif 