# -*- coding: utf-8 -*-
"""
系统源一键配置工具
"""

from base import BaseTool, PrintUtils, CmdTask, ChooseTask

class Tool(BaseTool):
    def __init__(self):
        self.type = BaseTool.TYPE_CONFIG
        self.name = "系统源配置"
        self.author = "no-one-wu"
        self.description = "更换Ubuntu系统软件源为国内镜像"
    
    def run(self):
        PrintUtils.print_info("准备更换系统软件源...")
        
        # 获取系统代号
        task = CmdTask("lsb_release -cs")
        task.run()
        codename = task.stdout.strip() if task.stdout else "focal"
        PrintUtils.print_info(f"检测到系统代号: {codename}")
        
        # 选择镜像源
        mirrors = [
            ("清华大学", f"https://mirrors.tuna.tsinghua.edu.cn/ubuntu/"),
            ("阿里云", f"https://mirrors.aliyun.com/ubuntu/"),
            ("中科大", f"https://mirrors.ustc.edu.cn/ubuntu/"),
            ("腾讯云", f"https://mirrors.cloud.tencent.com/ubuntu/"),
        ]
        
        options = [{"name": "返回"}] + [{"name": m[0]} for m in mirrors]
        choice = ChooseTask("请选择镜像源", options).run()
        
        if choice == 0:
            return
        
        name, url = mirrors[choice - 1]
        PrintUtils.print_info(f"已选择: {name}")
        
        # 备份原配置
        CmdTask("sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak.$(date +%Y%m%d)").run()
        
        # 生成新配置
        content = f"""# 由一键安装工具自动生成
deb {url} {codename} main restricted universe multiverse
deb {url} {codename}-updates main restricted universe multiverse
deb {url} {codename}-backports main restricted universe multiverse
deb {url} {codename}-security main restricted universe multiverse
"""
        
        # 写入临时文件并替换
        with open("/tmp/sources.list.new", "w") as f:
            f.write(content)
        CmdTask("sudo mv /tmp/sources.list.new /etc/apt/sources.list").run()
        CmdTask("sudo apt update").run()
        
        PrintUtils.print_success("系统源更换完成！")
