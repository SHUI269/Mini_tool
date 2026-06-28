# -*- coding: utf-8 -*-
"""
ROS 安装工具
"""

from base import BaseTool, PrintUtils, CmdTask, osversion


class Tool(BaseTool):
    def __init__(self):
        self.name = "ROS安装"
    
    def run(self):
        ver = osversion.get('version_id', '')
        
        ros_map = {
            '18.04': 'melodic',
            '20.04': 'noetic',
            '22.04': 'humble'
        }
        
        if ver not in ros_map:
            PrintUtils.print_error(f"不支持的版本: {ver}")
            return
        
        ros_distro = ros_map[ver]
        PrintUtils.print_info(f"将安装 ROS {ros_distro}")
        
        # 添加源
        CmdTask('sudo sh -c \'echo "deb http://mirrors.tuna.tsinghua.edu.cn/ros/ubuntu/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros-latest.list\'').run()
        CmdTask("curl -s https://gitee.com/ohhuo/rosdistro/raw/master/ros.asc | sudo apt-key add -").run()
        
        # 安装
        CmdTask("sudo apt update").run()
        CmdTask(f"sudo apt install -y ros-{ros_distro}-desktop").run()
        
        # 配置环境
        CmdTask(f"echo 'source /opt/ros/{ros_distro}/setup.bash' >> ~/.bashrc").run()
        
        PrintUtils.print_success(f"ROS {ros_distro} 安装完成！")
