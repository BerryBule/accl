#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='通过代理上传代码到远程服务器')
    parser.add_argument('--proxy', default='10.83.90.86', help='代理服务器地址')
    parser.add_argument('--remote', default='192.168.9.114', help='远程服务器地址')
    parser.add_argument('--remote-path', default='/mnt/sdb1/jingln/', help='远程服务器上的目标路径')
    parser.add_argument('--exclude', nargs='+', default=['.git', '.vscode', 'build', '__pycache__'], 
                        help='要排除的目录或文件')
    parser.add_argument('--dry-run', action='store_true', help='仅显示将要执行的命令，不实际执行')
    return parser.parse_args()

def build_rsync_command(args, source_dir):
    """构建rsync命令"""
    # 基本rsync命令
    cmd = ['rsync', '-avz', '--progress']
    
    # 添加排除项
    for exclude in args.exclude:
        cmd.extend(['--exclude', exclude])
    
    # 添加源目录
    cmd.append(source_dir)
    
    # 添加远程目标
    remote_target = f"{args.remote}:{args.remote_path}"
    cmd.append(remote_target)
    
    return cmd

def execute_command(cmd, dry_run=False):
    """执行命令"""
    if dry_run:
        print(f"将要执行的命令: {' '.join(cmd)}")
        return 0
    
    print(f"执行命令: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return e.returncode

def setup_ssh_proxy(proxy):
    """设置SSH代理"""
    # 创建或修改SSH配置文件
    ssh_config_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_config_dir, exist_ok=True)
    
    ssh_config_path = os.path.join(ssh_config_dir, "config")
    
    # 检查是否已经存在代理配置
    with open(ssh_config_path, 'a+') as f:
        f.seek(0)
        content = f.read()
        if f"Host {proxy}" not in content:
            # 添加代理配置
            proxy_config = f"""
Host {proxy}
    HostName {proxy}
    User root
    Port 22
    PreferredAuthentications publickey
    PubkeyAuthentication yes
    StrictHostKeyChecking no
"""
            f.write(proxy_config)
    
    # 设置环境变量
    os.environ["RSYNC_RSH"] = f"ssh -J {proxy}"
    
    print(f"已设置SSH代理: {proxy}")

def main():
    """主函数"""
    args = parse_args()
    
    # 获取当前目录
    current_dir = os.getcwd()
    
    # 设置SSH代理
    setup_ssh_proxy(args.proxy)
    
    # 构建rsync命令
    cmd = build_rsync_command(args, current_dir)
    
    # 执行命令
    start_time = time.time()
    result = execute_command(cmd, args.dry_run)
    end_time = time.time()
    
    if result == 0:
        print(f"上传成功! 耗时: {end_time - start_time:.2f} 秒")
    else:
        print(f"上传失败，返回码: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main() 