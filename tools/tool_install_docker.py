# -*- coding: utf-8 -*-
"""
Docker 一键安装工具
"""

from base import BaseTool, PrintUtils, CmdTask

class Tool(BaseTool):
    def __init__(self):
        self.type = BaseTool.TYPE_INSTALL
        self.name = "Docker安装"
        self.author = "no-one-wu"
        self.description = "安装Docker和Docker Compose"
    
    def run(self):
        PrintUtils.print_info("开始安装 Docker...")
        
        # 卸载旧版本
        CmdTask("sudo apt remove docker docker-engine docker.io containerd runc 2>/dev/null || true").run()
        
        # 安装依赖
        CmdTask("sudo apt update").run()
        CmdTask("sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release").run()
        
        # 添加GPG密钥（中科大镜像）
        CmdTask("curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg").run()
        
        # 添加软件源
        arch = osversion.get('machine', 'amd64')
        source = f'deb [arch={arch} signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu $(lsb_release -cs) stable'
        CmdTask(f'sudo sh -c \'echo "{source}" > /etc/apt/sources.list.d/docker.list\'').run()
        
        # 安装Docker
        CmdTask("sudo apt update").run()
        CmdTask("sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin").run()
        
        # 添加用户到docker组
        import getpass
        user = getpass.getuser()
        CmdTask(f"sudo usermod -aG docker {user}").run()
        
        PrintUtils.print_success("Docker 安装完成！")
        PrintUtils.print_warning("请注销并重新登录以使权限生效")
        PrintUtils.print_info("测试命令: docker run hello-world")
