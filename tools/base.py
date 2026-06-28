# -*- coding: utf-8 -*-
"""
一键安装工具基础类
"""

import os
import sys
import subprocess
import platform

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

class PrintUtils:
    @staticmethod
    def print_success(msg):
        print(f"{Colors.GREEN}[-] {msg}{Colors.NC}")
    
    @staticmethod
    def print_error(msg):
        print(f"{Colors.RED}[!] {msg}{Colors.NC}")
    
    @staticmethod
    def print_warning(msg):
        print(f"{Colors.YELLOW}[*] {msg}{Colors.NC}")
    
    @staticmethod
    def print_info(msg):
        print(f"{Colors.BLUE}[+] {msg}{Colors.NC}")
    
    @staticmethod
    def print_banner():
        print("""
╔══════════════════════════════════════════════════════╗
║        欢迎使用一键安装工具                          ║
║        人生苦短，三省吾身，省时省力省心!             ║
╚══════════════════════════════════════════════════════╝
        """)

class CmdTask:
    def __init__(self, cmd, timeout=300):
        self.cmd = cmd
        self.timeout = timeout
    
    def run(self):
        PrintUtils.print_info(f"执行: {self.cmd}")
        try:
            r = subprocess.run(
                self.cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if r.returncode == 0:
                PrintUtils.print_success("成功")
                if r.stdout:
                    print(r.stdout.strip())
                return True
            else:
                PrintUtils.print_error(f"失败 (code:{r.returncode})")
                if r.stderr:
                    print(r.stderr.strip())
                return False
        except Exception as e:
            PrintUtils.print_error(f"错误: {str(e)}")
            return False

class ChooseTask:
    def __init__(self, title, options):
        self.title = title
        self.options = options
    
    def run(self):
        print(f"\n{Colors.YELLOW}[{self.title}]{Colors.NC}")
        print("-" * 40)
        for i, o in enumerate(self.options):
            print(f"[{i}]: {o['name']}")
        print("-" * 40)
        
        while True:
            try:
                c = input("请输入数字选择: ").strip()
                idx = int(c)
                if 0 <= idx < len(self.options):
                    return idx
            except (ValueError, EOFError, KeyboardInterrupt):
                pass
            PrintUtils.print_warning("无效输入，请重新选择")

class BaseTool:
    TYPE_INSTALL = "install"
    TYPE_CONFIG = "config"
    
    def __init__(self):
        self.type = self.TYPE_INSTALL
        self.name = "基础工具"
        self.author = "匿名"
        self.description = ""
    
    def run(self):
        raise NotImplementedError("子类必须实现 run 方法")

def get_os_info():
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "distro": "",
        "version_id": ""
    }
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('ID='):
                    info['distro'] = line.split('=')[1].strip().strip('"')
                elif line.startswith('VERSION_ID='):
                    info['version_id'] = line.split('=')[1].strip().strip('"')
    except:
        pass
    return info

osversion = get_os_info()
