# AscendOps

AscendOps是一个高性能的算子库，提供了丰富的通信算子和计算算子实现。

## 项目结构

```
project_root/
├── src/                    # 源代码
│   ├── core/              # 核心实现
│   ├── api/               # API接口
│   └── third_party/       # 第三方依赖
├── tests/                 # 测试代码
├── tools/                 # 工具和脚本
├── docs/                  # 文档
└── cmake/                 # CMake配置
```

## 编译要求

- CMake 3.14+
- C++17 兼容的编译器
- Python 3.7+ (用于Python绑定)

## 编译步骤

```bash
mkdir build
cd build
cmake ..
make
```

## 使用示例

### C++ API

```cpp
#include "ascend_ops/all2all.h"

int main() {
    ascend::ops::All2AllOp op;
    // 初始化算子
    op.Init(shape, rank_ids, dtype);
    // 执行算子
    op.Execute(input, output);
    return 0;
}
```

### Python API

```python
import ascend_ops

op = ascend_ops.All2AllOp()
# 初始化算子
op.init(shape, rank_ids, dtype)
# 执行算子
op.execute(input, output)
```

## 文档

详细文档请参考 `docs/` 目录。

## 许可证

[许可证类型] 