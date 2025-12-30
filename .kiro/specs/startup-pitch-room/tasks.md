# Implementation Plan: Startup Pitch Room Demo

## Overview

基于已有的 hello_world demo 结构，实现 Startup Pitch Room 多代理演示。该实现将创建网络配置、三个角色代理（创始人、工程师、投资人）以及完整的文档。

## Tasks

- [x] 1. 创建 demo 目录结构
  - 创建 `demos/01_startup_pitch_room/` 目录
  - 创建 `demos/01_startup_pitch_room/agents/` 子目录
  - 创建必要的 mods 和 logs 目录结构
  - _Requirements: 6.6_

- [x] 2. 创建网络配置文件
  - [x] 2.1 创建 network.yaml
    - 配置网络名称为 "StartupPitchRoom"
    - 配置 HTTP 传输端口 8700，启用 Studio
    - 配置 gRPC 传输端口 8600
    - 配置 messaging mod 及默认频道 (pitch-room, ideas)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9_

- [x] 3. 创建代理配置文件
  - [x] 3.1 创建 founder.yaml (创始人代理)
    - 配置 CollaboratorAgent 类型
    - 配置 agent_id 为 "founder"
    - 配置热情、乐观、有创造力的个性指令
    - 配置只响应人类消息的规则
    - 配置随机延迟 0-3 秒
    - 配置响应长度限制 50 词
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 5.1, 5.4_

  - [x] 3.2 创建 engineer.yaml (工程师代理)
    - 配置 CollaboratorAgent 类型
    - 配置 agent_id 为 "engineer"
    - 配置分析性、注重细节的个性指令
    - 配置只响应人类消息的规则
    - 配置随机延迟 0-3 秒
    - 配置响应长度限制 50 词
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 5.2, 5.4_

  - [x] 3.3 创建 investor.yaml (投资人代理)
    - 配置 CollaboratorAgent 类型
    - 配置 agent_id 为 "investor"
    - 配置分析性、关注回报的个性指令
    - 配置只响应人类消息的规则
    - 配置随机延迟 0-3 秒
    - 配置响应长度限制 50 词
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 5.3, 5.4_

- [x] 4. 创建 README 文档
  - [x] 4.1 创建 README.md
    - 包含架构图
    - 包含前置条件说明
    - 包含环境变量配置指南
    - 包含快速开始指南（多终端命令）
    - 包含排障指南
    - 包含文件结构说明
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [x] 5. Checkpoint - 验证配置完整性
  - 确保所有配置文件语法正确
  - 确保目录结构完整
  - 如有问题请询问用户

## Notes

- 该 demo 基于已有的 hello_world demo 结构
- 使用 glm-4.7 模型（智谱 AI）
- 代理通过 instruction 中的规则防止相互响应
- 所有代理共享相同的网络连接配置
