# 🌾 水稻花粉活力智能检测系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-8.3.104-green.svg)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个基于**YOLOv8**和**Streamlit**开发的水稻花粉活力智能检测系统，能够自动识别水稻花粉类型并判断其活力状态。

## ✨ 主要特性

- 🔍 **智能识别**：使用YOLOv8深度学习模型自动识别水稻花粉类型
- 🌱 **活力分析**：智能判断花粉的可育性状态
- 👥 **多用户系统**：支持普通用户、专业用户和管理员三种角色
- 📊 **数据分析**：提供详细的统计分析和可视化图表
- 📚 **知识库**：集成专业的水稻花粉知识科普和案例分享
- 💾 **数据管理**：完整的数据存储、导出和管理功能
- 🖼️ **批量处理**：支持多图片批量分析
- 📈 **趋势分析**：历史数据趋势分析和对比研究

## 🎯 应用场景

- **农业科研**：水稻育种研究中的花粉活力筛选
- **教学实验**：农业院校的植物生理学实验教学
- **生产指导**：水稻种植生产中的花粉质量评估
- **品种选育**：杂交水稻育种过程中的亲本筛选

## 🏗️ 技术架构

### 核心技术
- **AI模型**：YOLOv8目标检测算法
- **Web框架**：Streamlit响应式Web界面
- **图像处理**：OpenCV + PIL图像处理库
- **数据可视化**：Plotly + Pandas数据分析
- **数据库**：SQLite轻量级数据库

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   YOLOv8        │    │   SQLite        │
│   Web界面       │◄──►│   AI模型        │◄──►│   数据库        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户管理      │    │   图像处理      │    │   数据管理      │
│   系统          │    │   模块          │    │   模块          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- CUDA支持（可选，用于GPU加速）
- 内存：至少4GB
- 磁盘空间：至少2GB

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/lnlll162/rice-pollen-detection-system.git
cd rice-pollen-detection-system
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **运行应用**
```bash
streamlit run app_streamlit.py
```

5. **访问系统**
在浏览器中打开 `http://localhost:8501`

### 默认账号
- **管理员账号**：`admin` / `admin123`
- **普通用户**：需要注册

## 📖 使用指南

### 1. 花粉检测
- 上传显微镜图像或高分辨率花粉照片
- 系统自动识别花粉类型和活力状态
- 查看详细的分析结果和统计信息

### 2. 专业分析（专业用户）
- 批量图片分析
- 数据趋势分析
- 实验对照分析
- 专业报告导出

### 3. 知识库
- 水稻花粉基础知识
- 研究方法和最新进展
- 典型案例分析

### 4. 案例分享
- 分享研究案例
- 查看他人案例
- 评论和讨论

## 🔧 系统配置

### 模型配置
- 检测置信度阈值：0.0-1.0（可调）
- 高级分析模式：专业用户可用
- 模型路径：需要训练或下载（见MODEL_DOWNLOAD.md）

### 数据配置
- 支持格式：JPG、JPEG、PNG
- 文件大小限制：5MB
- 建议分辨率：不超过4000x3000

## 📊 功能模块

### 核心模块
- **`app_streamlit.py`**：主应用程序入口
- **`user_management.py`**：用户管理系统
- **`knowledge_base.py`**：知识库管理
- **`case_management.py`**：案例管理系统

### 数据模块
- **用户数据**：用户信息、角色权限
- **分析数据**：检测结果、统计数据
- **案例数据**：研究案例、评论信息

## 🎨 界面预览

系统提供直观的Web界面，包括：
- 登录注册页面
- 花粉检测主界面
- 数据分析仪表板
- 知识库浏览界面
- 案例分享平台

## 📈 性能指标

- **检测精度**：基于YOLOv8模型的高精度识别
- **处理速度**：支持实时图像处理
- **并发用户**：支持多用户同时使用
- **数据存储**：高效的数据管理和查询

## 🔒 安全特性

- 用户身份验证和授权
- 密码加密存储
- 角色权限管理
- 数据访问控制

## 🌟 特色功能

### 智能活力判断
系统基于图像特征自动判断花粉活力：
- 细胞质密度分析
- 形态完整性评估
- 发育阶段识别

### 多维度分析
- 品种分布分析
- 活力状态统计
- 历史趋势对比
- 实验对照研究

### 专业报告生成
- 自动生成分析报告
- 支持多种导出格式
- 包含详细统计图表
- 专业指标评估

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2024-12-19)
- ✨ 初始版本发布
- 🔍 基于YOLOv8的花粉识别
- 👥 多用户管理系统
- 📊 数据分析和可视化
- 📚 知识库和案例分享

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Ultralytics](https://github.com/ultralytics/ultralytics) - YOLOv8模型
- [Streamlit](https://streamlit.io/) - Web应用框架
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [Plotly](https://plotly.com/) - 数据可视化库

## 📞 联系我们

- **项目地址**：https://github.com/lnlll162/rice-pollen-detection-system
- **问题反馈**：请在GitHub Issues中提交
- **功能建议**：欢迎提交Feature Request

---

<div align="center">
  <p>如果这个项目对您有帮助，请给我们一个 ⭐️</p>
  <p>🌾 让AI技术为农业发展贡献力量 🌾</p>
</div>
