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

## 工具使用

### 代码上传工具

项目提供了代码上传工具，支持通过代理服务器将代码上传到远程服务器。

#### 使用方法

```bash
python tools/upload.py [选项]
```

#### 选项说明

- `-p, --proxy PROXY`：设置代理服务器地址（默认：10.83.90.86）
- `-r, --remote REMOTE`：设置远程服务器地址（默认：192.168.9.114）
- `-d, --dest PATH`：设置远程服务器上的目标路径（默认：/mnt/sdb1/jingln/）
- `-e, --exclude DIR`：要排除的目录或文件（可多次指定）
- `-n, --dry-run`：仅显示将要执行的命令，不实际执行
- `-m, --method METHOD`：选择上传方法：rsync 或 scp（默认：scp）

#### 使用示例

```bash
# 使用默认设置上传
python tools/upload.py

# 指定不同的远程服务器
python tools/upload.py -r 192.168.1.100

# 指定不同的目标路径
python tools/upload.py -d /path/to/destination

# 添加要排除的目录
python tools/upload.py -e "node_modules" -e "dist"

# 使用rsync方法上传
python tools/upload.py -m rsync

# 先测试命令（不实际执行）
python tools/upload.py -n
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