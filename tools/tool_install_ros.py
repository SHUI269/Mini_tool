# -*- coding: utf-8 -*-
"""
ROS 一键安装工具
"""

from base import BaseTool, PrintUtils, CmdTask, ChooseTask

class Tool(BaseTool):
    def __init__(self):
        self.type = BaseTool.TYPE_INSTALL
        self.name = "ROS安装"
        self.author = "no-one-wu"
        self.description = "支持ROS1和ROS2的一键安装"
    
    def run(self):
        PrintUtils.print_info("开始安装 ROS...")
        
        ver = osversion.get('version_id', '')
        distro = osversion.get('distro', '')
        PrintUtils.print_info(f"检测到系统: {distro} {ver}")
        
        # 版本映射
        ros_map = {
            '18.04': 'melodic',
            '20.04': 'noetic',
            '22.04': 'humble'
        }
        
        if ver not in ros_map:
            PrintUtils.print_error(f"不支持的 Ubuntu 版本: {ver}")
            return
        
        ros_distro = ros_map[ver]
        PrintUtils.print_info(f"将安装 ROS {ros_distro}")
        
        # 添加清华源
        PrintUtils.print_info("添加 ROS 软件源...")
        source_cmd = 'sudo sh -c \'echo "deb http://mirrors.tuna.tsinghua.edu.cn/ros/ubuntu/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros-latest.list\''
        CmdTask(source_cmd).run()
        
        # 添加密钥
        CmdTask("curl -s https://gitee.com/ohhuo/rosdistro/raw/master/ros.asc | sudo apt-key add -").run()
        
        # 更新并安装
        CmdTask("sudo apt update").run()
        CmdTask(f"sudo apt install -y ros-{ros_distro}-desktop").run()
        
        # 配置环境变量
        setup = f"source /opt/ros/{ros_distro}/setup.bash"
        CmdTask(f"echo '{setup}' >> ~/.bashrc").run()
        
        # 安装依赖工具
        CmdTask("sudo apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential").run()
        CmdTask("sudo rosdep init 2>/dev/null || true").run()
        CmdTask("rosdep update 2>/dev/null || true").run()
        
        PrintUtils.print_success(f"ROS {ros_distro} 安装完成！")
        PrintUtils.print_info("请运行 'source ~/.bashrc' 或重新打开终端")
