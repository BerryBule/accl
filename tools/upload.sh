#!/bin/bash

# 设置脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 默认参数
PROXY="10.83.90.86"
REMOTE="192.168.9.114"
REMOTE_PATH="/mnt/sdb1/jingln/"
EXCLUDE=(".git" ".vscode" "build" "__pycache__")
DRY_RUN=false

# 显示帮助信息
function show_help {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  -p, --proxy PROXY       代理服务器地址 (默认: $PROXY)"
    echo "  -r, --remote REMOTE     远程服务器地址 (默认: $REMOTE)"
    echo "  -d, --dest PATH         远程服务器上的目标路径 (默认: $REMOTE_PATH)"
    echo "  -e, --exclude DIR       要排除的目录或文件 (可多次指定)"
    echo "  -n, --dry-run           仅显示将要执行的命令，不实际执行"
    echo "  -h, --help              显示此帮助信息"
    echo "  -m, --method METHOD     上传方法: rsync 或 scp (默认: scp)"
    exit 0
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        -p|--proxy)
            PROXY="$2"
            shift 2
            ;;
        -r|--remote)
            REMOTE="$2"
            shift 2
            ;;
        -d|--dest)
            REMOTE_PATH="$2"
            shift 2
            ;;
        -e|--exclude)
            EXCLUDE+=("$2")
            shift 2
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        -m|--method)
            METHOD="$2"
            shift 2
            ;;
        *)
            echo "未知选项: $1"
            show_help
            ;;
    esac
done

# 设置默认方法
if [ -z "$METHOD" ]; then
    METHOD="scp"
fi

# 构建排除参数
EXCLUDE_ARGS=""
for item in "${EXCLUDE[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude $item"
done

# 构建命令
if [ "$METHOD" = "rsync" ]; then
    # 使用rsync方法
    CMD="python3 $SCRIPT_DIR/upload_code.py --proxy $PROXY --remote $REMOTE --remote-path $REMOTE_PATH $EXCLUDE_ARGS"
else
    # 使用scp方法
    CMD="python3 $SCRIPT_DIR/upload_code_scp.py --proxy $PROXY --remote $REMOTE --remote-path $REMOTE_PATH --exclude ${EXCLUDE[@]}"
fi

# 添加dry-run参数
if [ "$DRY_RUN" = true ]; then
    CMD="$CMD --dry-run"
fi

# 执行命令
echo "执行命令: $CMD"
eval $CMD 