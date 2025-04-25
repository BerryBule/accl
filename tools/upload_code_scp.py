#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
import time
import tarfile
import tempfile
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

def create_tar_archive(source_dir, exclude_dirs):
    """创建tar归档文件，排除指定目录"""
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tar.gz')
    temp_file.close()
    
    # 创建tar归档
    with tarfile.open(temp_file.name, 'w:gz') as tar:
        # 获取源目录的绝对路径
        source_abs = os.path.abspath(source_dir)
        
        # 遍历目录
        for root, dirs, files in os.walk(source_dir):
            # 排除指定目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # 获取文件的完整路径
                file_path = os.path.join(root, file)
                
                # 计算相对路径
                arcname = os.path.relpath(file_path, source_abs)
                
                # 添加到归档
                tar.add(file_path, arcname=arcname)
    
    return temp_file.name

def setup_ssh_config(proxy):
    """设置SSH配置"""
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
    
    print(f"已设置SSH配置: {proxy}")

def execute_scp_command(archive_path, proxy, remote, remote_path, dry_run=False):
    """执行scp命令"""
    # 设置SSH配置
    setup_ssh_config(proxy)
    
    # 构建scp命令
    cmd = ['scp', '-o', f'ProxyJump={proxy}', archive_path, f'{remote}:{remote_path}']
    
    if dry_run:
        print(f"将要执行的命令: {' '.join(cmd)}")
        return 0
    
    print(f"执行命令: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return result.returncode

def execute_remote_command(proxy, remote, remote_path, archive_name, dry_run=False):
    """在远程服务器上执行命令"""
    # 设置SSH配置
    setup_ssh_config(proxy)
    
    # 构建SSH命令
    cmd = ['ssh', '-J', proxy, remote, f'cd {remote_path} && tar -xzf {archive_name}']
    
    if dry_run:
        print(f"将要执行的命令: {' '.join(cmd)}")
        return 0
    
    print(f"执行命令: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return result.returncode

def main():
    """主函数"""
    args = parse_args()
    
    # 获取当前目录
    current_dir = os.getcwd()
    
    print(f"开始上传代码到 {args.remote}:{args.remote_path}")
    print(f"排除目录: {args.exclude}")
    
    # 创建tar归档
    print("创建tar归档...")
    start_time = time.time()
    archive_path = create_tar_archive(current_dir, args.exclude)
    print(f"归档创建完成: {archive_path}")
    
    # 获取归档文件名
    archive_name = os.path.basename(archive_path)
    
    # 执行scp命令
    print("上传归档文件...")
    result = execute_scp_command(archive_path, args.proxy, args.remote, args.remote_path, args.dry_run)
    
    if result != 0:
        print(f"上传失败，返回码: {result}")
        os.unlink(archive_path)  # 清理临时文件
        sys.exit(1)
    
    # 在远程服务器上解压归档
    print("在远程服务器上解压归档...")
    result = execute_remote_command(args.proxy, args.remote, args.remote_path, archive_name, args.dry_run)
    
    # 清理临时文件
    os.unlink(archive_path)
    
    end_time = time.time()
    
    if result == 0:
        print(f"上传和解压成功! 耗时: {end_time - start_time:.2f} 秒")
    else:
        print(f"解压失败，返回码: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main() 