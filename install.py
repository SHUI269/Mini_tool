#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键安装主程序
提供菜单选择和工具调度
"""

import os
import sys
import importlib.util

# 添加 tools 目录到路径
TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
sys.path.insert(0, TOOLS_DIR)

from base import BaseTool, PrintUtils, ChooseTask

# 工具注册表
TOOLS_REGISTRY = [
    {"name": "退出", "file": None},
    {"name": "一键安装:ROS (支持ROS1/ROS2)", "file": "tool_install_ros.py"},
    {"name": "一键配置:系统源 (清华/阿里/中科大)", "file": "tool_config_source.py"},
    {"name": "一键安装:Docker", "file": "tool_install_docker.py"},
]

def load_tool(tool_info):
    """动态加载工具模块"""
    if not tool_info["file"]:
        return None
    
    path = os.path.join(TOOLS_DIR, tool_info["file"])
    if not os.path.exists(path):
        PrintUtils.print_warning(f"工具文件不存在: {tool_info['file']}")
        return None
    
    try:
        spec = importlib.util.spec_from_file_location("tool", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.Tool() if hasattr(mod, 'Tool') else None
    except Exception as e:
        PrintUtils.print_error(f"加载工具失败: {str(e)}")
        return None

def main():
    PrintUtils.print_banner()
    
    while True:
        options = [{"name": t["name"]} for t in TOOLS_REGISTRY]
        choice = ChooseTask("请选择要执行的任务", options).run()
        
        if choice == 0:
            PrintUtils.print_info("感谢使用，再见！")
            break
        
        tool = load_tool(TOOLS_REGISTRY[choice])
        if tool:
            try:
                tool.run()
            except Exception as e:
                PrintUtils.print_error(f"工具执行出错: {str(e)}")
        else:
            PrintUtils.print_error("工具加载失败，请检查网络连接")
        
        print("\n" + "=" * 50)
        input("按 Enter 键返回主菜单...")

if __name__ == "__main__":
    main()
