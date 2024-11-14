<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://github.com/WwwwwyDev/fantasy-world-bot4qq"><img src="https://s2.loli.net/2024/11/14/7LcfzE2tVZn1oXy.png" alt="fantasy-world-bot4qq" style="width:30%; height:30%" ></a>

<div align="center">

# fantasy-world-bot4qq

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
基于官方[PythonSDK](https://github.com/tencent-connect/botpy "PythonSDK")开发的群聊游戏机器人
<!-- prettier-ignore-end -->

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10.0+-blue" alt="python">
  <a href="https://github.com/WwwwwyDev/fantasy-world-bot4qq/stargazers"><img src="https://img.shields.io/github/stars/WwwwwyDev/fantasy-world-bot4qq" alt="GitHub stars"style="max-width: 100%;">
  </a>
  <br/>
</p>
</div>


## 介绍

幻想世界是纯文本qq群聊机器人，以活跃群为目的，过审即用，支持个人账号，无需ark或markdown权限。使用官方sdk开发，不会有封号风险。使用非关系型数据库mongodb，部署简单。使用mvc软件架构开发，便于二开。

## 部署
1. 在[qq开放平台](https://q.qq.com)中注册你的qq机器人
2. 使用conda导入python环境
`conda env create -f environment.yml`
3. 部署mongodb数据库
4. 在config.yaml中配置相关信息，并使用命令`python main.py`开启服务器，此时机器人可在沙箱环境中运行
5. 通过官方审核，便可以添加至自己的群聊
6. 使用`nohup python main.py &`挂起服务器或使用Supervisor等管理工具进行管理

## 体验
扫描二维码添加机器人到群聊在线体验\
![二维码](./images/bot.png)
