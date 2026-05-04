# 算法可视化演示系统

基于 Web 的《数据结构与算法》可视化演示系统

## 项目介绍

本项目采用前后端分离架构，通过 WebSocket 实现实时双向通信，展示数据结构和算法的执行过程。

### 支持的算法

| 算法 | 说明 |
|------|------|
| 堆的创建 | 最大堆构建过程可视化 |
| 快速排序 | 分区排序过程可视化 |
| 链表操作 | 链表创建与遍历可视化 |
| 二叉树遍历 | 前序/中序/后序遍历可视化 |

## 项目结构

```
├── backend/              # 后端（Flask + WebSocket）
│   ├── app.py           # 主服务入口
│   ├── algorithms/      # 算法执行器
│   └── utils/           # 工具模块
│
├── frontend/            # 前端（队友负责）
│   ├── index.html
│   ├── css/
│   └── js/
│
└── README.md
```

## 后端启动

```bash
cd backend
pip install -r requirements.txt
python app.py
```

服务地址: http://127.0.0.1:5000

## 接口文档

详见: [backend/README.md](backend/README.md)

## 分工

- **后端**: @YuYang - Flask服务、算法执行器、WebSocket通信
- **前端**: @队友 - 页面设计、可视化渲染、用户交互

## 协作说明

1. 前后端通过WebSocket实时通信
2. 步骤数据格式统一（详见backend/README.md）
3. 建议使用Git分支开发，完成后合并

---
*Last updated: 2026-05-04*
