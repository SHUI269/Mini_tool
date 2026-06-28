#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键安装主程序
"""

import os
import sys
import importlib.util

# 配置
URL_PREFIX = "https://raw.githubusercontent.com/SHUI269/Mini_tool/main/"
TOOLS_DIR = "/tmp/myinstall/tools"

# 工具注册表
TOOLS = {
    0: {"tip": "退出", "type": "quit", "tool": None},
    1: {"tip": "一键安装:ROS (支持ROS1/ROS2)", "type": "ROS", "tool": "tools/tool_install_ros.py"},
    2: {"tip": "一键配置:系统源 (更换国内镜像)", "type": "配置", "tool": "tools/tool_config_source.py"},
    3: {"tip": "一键安装:Docker", "type": "软件", "tool": "tools/tool_install_docker.py"},
    4: {"tip": "一键安装:VSCode", "type": "软件", "tool": "tools/tool_install_vscode.py"},
}

# 按类型分组
TYPE_NAMES = {
    "ROS": "🤖 ROS相关",
    "软件": "💻 常用软件",
    "配置": "⚙️ 配置工具",
}


def download_file(url, output):
    """下载文件"""
    print(f"  ↓ 下载 {os.path.basename(output)}...")
    ret = os.system(f"wget -q {url} -O {output}")
    return ret == 0


def download_tool(tool_path):
    """下载工具模块"""
    url = URL_PREFIX + tool_path
    output = os.path.join("/tmp/myinstall", tool_path)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    return download_file(url, output)


def run_tool(tool_path):
    """动态加载并运行工具"""
    full_path = os.path.join("/tmp/myinstall", tool_path)
    if not os.path.exists(full_path):
        print(f"[!] 工具文件不存在: {tool_path}")
        return False
    
    try:
        spec = importlib.util.spec_from_file_location("tool", full_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, 'Tool'):
            tool = mod.Tool()
            tool.run()
            return True
    except Exception as e:
        print(f"[!] 运行工具出错: {e}")
    return False


def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║        欢迎使用一键安装工具                          ║
║        人生苦短，三省吾身，省时省力省心!             ║
╚══════════════════════════════════════════════════════╝
    """)


def print_menu():
    """打印分类菜单"""
    print("请选择要执行的任务：\n")
    
    # 按类型分组显示
    current_type = None
    for code, info in sorted(TOOLS.items()):
        if info["type"] == "quit":
            print(f"[{code}] {info['tip']}")
            continue
        
        if info["type"] != current_type:
            current_type = info["type"]
            type_name = TYPE_NAMES.get(current_type, current_type)
            print(f"\n--- {type_name} ---")
        
        print(f"[{code}] {info['tip']}")
    
    print("")


def main():
    # 下载基础模块
    print("[0/2] 下载基础模块...")
    download_file(URL_PREFIX + "tools/base.py", os.path.join(TOOLS_DIR, "base.py"))
    
    # 下载主程序需要的其他文件...
    
    print_banner()
    print_menu()
    
    while True:
        try:
            choice = input("请输入数字选择: ").strip()
            code = int(choice)
            
            if code not in TOOLS:
                print("无效选择，请重新输入")
                continue
            
            tool_info = TOOLS[code]
            
            if tool_info["type"] == "quit":
                print("感谢使用，再见！")
                break
            
            print(f"\n>>> {tool_info['tip']}\n")
            
            # 下载并运行工具
            if download_tool(tool_info["tool"]):
                run_tool(tool_info["tool"])
            else:
                print("[!] 下载工具失败")
            
            print("\n" + "="*50)
            input("按 Enter 键返回主菜单...")
            print_banner()
            print_menu()
            
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\n感谢使用，再见！")
            break


if __name__ == "__main__":
    main()
