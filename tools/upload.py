#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import subprocess
from pathlib import Path

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='上传代码到远程服务器')
    parser.add_argument('-p', '--proxy', default='10.83.90.86',
                      help='代理服务器地址 (默认: 10.83.90.86)')
    parser.add_argument('-r', '--remote', default='192.168.9.114',
                      help='远程服务器地址 (默认: 192.168.9.114)')
    parser.add_argument('-d', '--dest', default='/mnt/sdb1/jingln/',
                      help='远程服务器上的目标路径 (默认: /mnt/sdb1/jingln/)')
    parser.add_argument('-e', '--exclude', action='append',
                      default=['.git', '.vscode', 'build', '__pycache__'],
                      help='要排除的目录或文件 (可多次指定)')
    parser.add_argument('-n', '--dry-run', action='store_true',
                      help='仅显示将要执行的命令，不实际执行')
    parser.add_argument('-m', '--method', choices=['rsync', 'scp'], default='scp',
                      help='上传方法: rsync 或 scp (默认: scp)')
    return parser.parse_args()

def build_command(args):
    """构建上传命令"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.method == 'rsync':
        # 使用rsync方法
        cmd = ['python3', os.path.join(script_dir, 'upload_code.py'),
               '--proxy', args.proxy,
               '--remote', args.remote,
               '--remote-path', args.dest]
        # 添加排除项
        for exclude in args.exclude:
            cmd.extend(['--exclude', exclude])
    else:
        # 使用scp方法
        cmd = ['python3', os.path.join(script_dir, 'upload_code_scp.py'),
               '--proxy', args.proxy,
               '--remote', args.remote,
               '--remote-path', args.dest,
               '--exclude'] + args.exclude
    
    # 添加dry-run参数
    if args.dry_run:
        cmd.append('--dry-run')
    
    return cmd

def main():
    """主函数"""
    args = parse_args()
    
    # 构建命令
    cmd = build_command(args)
    
    # 执行命令
    print(f"执行命令: {' '.join(cmd)}")
    if not args.dry_run:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main() 