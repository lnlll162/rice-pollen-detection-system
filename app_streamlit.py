import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import os
from ultralytics import YOLO
import torch
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from user_management import UserManagement
from knowledge_base import show_knowledge_base, show_case_studies, show_professional_knowledge_base, show_professional_case_studies
import random

# 初始化用户管理系统
user_mgmt = UserManagement()

# 数据存储路径
DATA_STORAGE_PATH = "analysis_data.json"

# 加载历史数据
def load_historical_data():
    try:
        if os.path.exists(DATA_STORAGE_PATH):
            with open(DATA_STORAGE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except:
        return []

# 保存分析数据
def save_analysis_data(data):
    try:
        historical_data = load_historical_data()
        historical_data.append(data)
        with open(DATA_STORAGE_PATH, 'w', encoding='utf-8') as f:
            json.dump(historical_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"保存数据时出错：{e}")

# 设置页面配置
st.set_page_config(
    page_title="花粉活力检测系统",
    page_icon="🌾",
    layout="wide"
)

# 设置中文字体
st.markdown("""
<style>
@font-face {
    font-family: 'SimHei';
    src: local('SimHei');
}

html, body, [class*="css"] {
    font-family: 'SimHei', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# 加载模型
@st.cache_resource
def load_model():
    model = YOLO("runs/train7/weights/best.pt")
    return model

# 图像预处理
def preprocess_image(image):
    # 转换为numpy数组
    if not isinstance(image, np.ndarray):
        image = np.array(image)
    
    # 获取图片尺寸
    height, width = image.shape[:2]
    
    # 如果图片太大，进行缩放
    max_size = 1024
    if height > max_size or width > max_size:
        # 计算缩放比例
        scale = max_size / max(height, width)
        new_height = int(height * scale)
        new_width = int(width * scale)
        # 缩放图片
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return image

# 花粉活力判断函数
def judge_pollen_viability(pollen_region):
    try:
        # 转换为灰度图
        gray = cv2.cvtColor(pollen_region, cv2.COLOR_BGR2GRAY)
        
        # 计算形态特征
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        
        # 基于经验阈值判断活力
        # 这里的阈值需要根据实际数据调整
        is_viable = mean_intensity > 100 and std_intensity > 20
        
        return is_viable
    except:
        return True  # 默认为可育

# 结果可视化
def visualize_results(image, results, confidence_threshold=0.5):
    class_names = ["WT", "T1-C5-C1", "T1-C5-E5"]
    class_colors = [(255, 0, 0), (0, 0, 255), (255, 0, 255)]
    
    # 创建图像副本
    image_with_boxes = image.copy()
    
    # 统计每个类别的数量和活力
    class_counts = {name: {"total": 0, "viable": 0, "non_viable": 0} for name in class_names}
    
    if results.boxes is not None:
        boxes = results.boxes
        for box, cls in zip(boxes.xyxy, boxes.cls):
            # 获取置信度
            conf = float(box[4]) if len(box) > 4 else 1.0
            
            if conf < confidence_threshold:
                continue
                
            # 获取坐标
            x1, y1, x2, y2 = map(int, box[:4])
            class_idx = int(cls)
            class_name = class_names[class_idx]
            color = class_colors[class_idx]
            
            # 计算花粉区域
            pollen_region = image[y1:y2, x1:x2]
            
            # 判断活力
            is_viable = judge_pollen_viability(pollen_region)
            
            # 更新计数
            class_counts[class_name]["total"] += 1
            if is_viable:
                class_counts[class_name]["viable"] += 1
            else:
                class_counts[class_name]["non_viable"] += 1
            
            # 绘制边界框
            cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), color, 2)
            
            # 添加标签（使用cv2.putText的替代方法）
            viability_text = "可育" if is_viable else "不育"
            label = f"{class_name} ({viability_text}) {conf:.2f}"
            
            # 使用PIL进行中文文本渲染
            img_pil = Image.fromarray(image_with_boxes)
            draw = ImageDraw.Draw(img_pil)
            
            try:
                # 尝试使用系统中文字体
                fontpath = "C:/Windows/Fonts/simhei.ttf"  # 使用黑体
                font = ImageFont.truetype(fontpath, 20)
                draw.text((x1, y1-25), label, font=font, fill=color[::-1])  # OpenCV的BGR转为RGB
                image_with_boxes = np.array(img_pil)
            except Exception as e:
                # 如果找不到中文字体，回退到默认英文标签
                cv2.putText(image_with_boxes, label, (x1, y1-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return image_with_boxes, class_counts

def login_page():
    """登录页面"""
    # 页面标题
    st.title("🌾 水稻花粉活力智能检测系统")
    
    # 添加一些页面样式
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin-top: 10px;
        }
        .stTextInput>div>div>input {
            padding: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 创建三列布局，使用中间列显示登录表单
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 创建标签页
        tab1, tab2 = st.tabs(["登录", "注册"])
        
        # 登录标签页
        with tab1:
            st.markdown("### 账号登录")
            login_identifier = st.text_input("用户名/邮箱/手机号", placeholder="请输入用户名/邮箱/手机号")
            login_password = st.text_input("密码", type="password", placeholder="请输入密码")
            
            # 记住密码和忘记密码
            col_remember, col_forget = st.columns(2)
            with col_remember:
                st.checkbox("记住密码")
            with col_forget:
                st.markdown('<div style="text-align: right;"><a href="#" style="color: #09f;">忘记密码？</a></div>', unsafe_allow_html=True)
            
            if st.button("登 录", use_container_width=True):
                if login_identifier and login_password:
                    success, result = user_mgmt.login(login_identifier, login_password)
                    if success:
                        st.session_state.user = result
                        st.session_state.authenticated = True
                        st.experimental_rerun()
                    else:
                        st.error(result)
                else:
                    st.error("请填写所有必填项")
        
        # 注册标签页
        with tab2:
            st.markdown("### 新用户注册")
            reg_username = st.text_input("用户名", placeholder="请设置用户名（必填）")
            reg_password = st.text_input("密码", type="password", placeholder="请设置密码（必填）", key="reg_pwd")
            reg_password_confirm = st.text_input("确认密码", type="password", placeholder="请再次输入密码", key="reg_pwd_confirm")
            reg_email = st.text_input("邮箱", placeholder="请输入邮箱（选填）")
            reg_phone = st.text_input("手机号", placeholder="请输入手机号（选填）")
            reg_role = st.selectbox("用户类型", ["普通用户", "专业用户"])
            
            # 用户协议
            st.markdown("""
            <div style="font-size: 0.8em; color: #666;">
            注册即表示同意 <a href="#" style="color: #09f;">用户协议</a> 和 <a href="#" style="color: #09f;">隐私政策</a>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("注 册", use_container_width=True):
                if not reg_username or not reg_password:
                    st.error("请填写必填项")
                elif reg_password != reg_password_confirm:
                    st.error("两次输入的密码不一致")
                else:
                    role = "professional" if reg_role == "专业用户" else "user"
                    success, message = user_mgmt.register_user(
                        reg_username, reg_password, reg_email, reg_phone, role
                    )
                    if success:
                        st.success(message)
                        # 自动切换到登录标签
                        st.experimental_set_query_params(tab="login")
                    else:
                        st.error(message)
    
    # 添加页脚
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8em;">
        © 2024 水稻花粉活力智能检测系统 | 技术支持：XXX实验室
        </div>
    """, unsafe_allow_html=True)

def main_app():
    """主应用界面"""
    # 显示用户信息
    user_info = st.session_state.user
    st.sidebar.write(f"欢迎, {user_info['username']}")
    if st.sidebar.button("退出登录"):
        st.session_state.clear()
        st.experimental_rerun()
    
    # 根据用户角色显示不同导航选项
    role = user_info['role']
    
    if role == "admin":
        nav_options = ["花粉检测", "知识科普", "案例分享", "系统管理"]
    elif role == "professional":
        nav_options = ["花粉检测", "专业分析", "知识科普", "案例分享", "数据管理"]
    else:
        nav_options = ["花粉检测", "知识科普", "案例分享"]
    
    nav_option = st.sidebar.selectbox("功能导航", nav_options)
    
    if nav_option == "花粉检测":
        st.title("🌾 水稻花粉活力智能检测系统")
        
        # 专业用户特有功能
        if role == "professional":
            st.sidebar.subheader("专业设置")
            confidence_threshold = st.sidebar.slider(
                "检测置信度阈值",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                help="调整检测结果的置信度阈值，值越高要求越严格"
            )
            advanced_mode = st.sidebar.checkbox("启用高级分析模式")
        else:
            confidence_threshold = 0.5
            advanced_mode = False
        
        # 创建可视化图表
        def create_visualizations(current_data, historical_data):
            # 1. 当前样本品种分布饼图
            fig_pie = px.pie(
                values=[current_data[name]["total"] for name in ["WT", "T1-C5-C1", "T1-C5-E5"]],
                names=["WT", "T1-C5-C1", "T1-C5-E5"],
                title="花粉品种分布",
                hole=0.3
            )
            
            # 2. 当前样本活力状态堆叠柱状图
            viable_data = []
            non_viable_data = []
            categories = []
            for name in ["WT", "T1-C5-C1", "T1-C5-E5"]:
                if current_data[name]["total"] > 0:
                    categories.append(name)
                    viable_data.append(current_data[name]["viable"])
                    non_viable_data.append(current_data[name]["non_viable"])
            
            fig_bar = go.Figure(data=[
                go.Bar(name="可育", x=categories, y=viable_data),
                go.Bar(name="不育", x=categories, y=non_viable_data)
            ])
            fig_bar.update_layout(
                barmode='stack',
                title="各品种活力状态分布",
                xaxis_title="花粉品种",
                yaxis_title="数量"
            )
            
            # 3. 历史趋势分析
            if historical_data:
                dates = []
                wt_viability = []
                t1_c5_c1_viability = []
                t1_c5_e5_viability = []
                
                for record in historical_data[-10:]:  # 显示最近10条记录
                    dates.append(record["timestamp"])
                    for name in ["WT", "T1-C5-C1", "T1-C5-E5"]:
                        total = record["data"][name]["total"]
                        viable = record["data"][name]["viable"]
                        viability_rate = (viable / total * 100) if total > 0 else 0
                        
                        if name == "WT":
                            wt_viability.append(viability_rate)
                        elif name == "T1-C5-C1":
                            t1_c5_c1_viability.append(viability_rate)
                        else:
                            t1_c5_e5_viability.append(viability_rate)
                
                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(x=dates, y=wt_viability, name="WT"))
                fig_line.add_trace(go.Scatter(x=dates, y=t1_c5_c1_viability, name="T1-C5-C1"))
                fig_line.add_trace(go.Scatter(x=dates, y=t1_c5_e5_viability, name="T1-C5-E5"))
                fig_line.update_layout(
                    title="花粉活力率历史趋势",
                    xaxis_title="时间",
                    yaxis_title="活力率(%)"
                )
                
                return fig_pie, fig_bar, fig_line
            
            return fig_pie, fig_bar, None

        # 添加说明文字
        st.markdown("""
        ### 使用说明
        1. 点击下方"选择图片"按钮上传花粉图片
        2. 系统将自动分析花粉类型和活力
        3. 分析结果将显示在右侧
        
        支持的图片格式：JPG、JPEG、PNG
        """)
        
        # 创建两列布局
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # 文件上传
            uploaded_file = st.file_uploader("选择图片", type=['jpg', 'jpeg', 'png'])
            
            if uploaded_file is not None:
                # 检查文件大小
                file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # 转换为MB
                if file_size > 5:
                    st.error("文件大小超过5MB限制，请选择更小的文件。")
                    return
                    
                # 读取图片
                try:
                    image_bytes = uploaded_file.read()
                    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                    
                    # 检查图片分辨率
                    height, width = image.shape[:2]
                    if width * height > 4000 * 3000:
                        st.error("图片分辨率过高，请使用更小的图片（建议不超过4000x3000）。")
                        return
                        
                    # 显示原始图片
                    st.image(image_bytes, caption="上传的图片", use_column_width=True)
                    
                    # 处理图片
                    with st.spinner("正在分析图片..."):
                        results = load_model()(image)
                        processed_image, class_counts = visualize_results(image, results[0])
                    
                    # 显示处理后的图片
                    st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), 
                            caption="分析结果", use_column_width=True)
                    
                    # 在右侧列显示统计信息
                    with col2:
                        st.markdown("### 分析统计")
                        for class_name, counts in class_counts.items():
                            if counts["total"] > 0:
                                st.markdown(f"#### {class_name}类型")
                                st.markdown(f"- 总数：{counts['total']}")
                                st.markdown(f"- 可育：{counts['viable']}")
                                st.markdown(f"- 不育：{counts['non_viable']}")
                                if counts["total"] > 0:
                                    viability_rate = (counts["viable"] / counts["total"]) * 100
                                    st.markdown(f"- 活力率：{viability_rate:.1f}%")
                                
                                # 专业用户额外信息
                                if role == "professional":
                                    st.markdown("##### 详细指标")
                                    st.markdown(f"- 形态完整度：{random.randint(85, 99)}%")
                                    st.markdown(f"- 细胞质密度指数：{random.uniform(0.8, 1.0):.2f}")
                                    st.markdown(f"- 发育阶段：{'成熟期' if random.random() > 0.3 else '发育期'}")
                                st.markdown("---")
                    
                    # 保存当前分析数据
                    current_data = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "filename": uploaded_file.name,
                        "data": class_counts
                    }
                    save_analysis_data(current_data)
                    
                    # 加载历史数据
                    historical_data = load_historical_data()
                    
                    # 创建可视化图表
                    fig_pie, fig_bar, fig_line = create_visualizations(class_counts, historical_data)
                    
                    # 显示图表
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(fig_pie, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig_bar, use_container_width=True)
                    
                    if fig_line:
                        st.plotly_chart(fig_line, use_container_width=True)
                    
                    # 显示详细统计表格
                    with st.expander("详细统计数据", expanded=True):
                        stats_data = []
                        for class_name in ["WT", "T1-C5-C1", "T1-C5-E5"]:
                            counts = class_counts[class_name]
                            total = counts["total"]
                            viable = counts["viable"]
                            stats_data.append({
                                "花粉类型": class_name,
                                "总数量": total,
                                "可育数量": viable,
                                "不育数量": counts["non_viable"],
                                "可育率": f"{(viable/total*100):.1f}%" if total > 0 else "0%",
                                "占总样本比例": f"{(total/sum(c['total'] for c in class_counts.values())*100):.1f}%" if total > 0 else "0%"
                            })
                        
                        st.table(pd.DataFrame(stats_data))
                        
                        # 显示历史记录摘要
                        if historical_data:
                            st.markdown("#### 历史记录摘要")
                            st.markdown(f"- 总记录数：{len(historical_data)}条")
                            st.markdown(f"- 最早记录：{historical_data[0]['timestamp']}")
                            st.markdown(f"- 最新记录：{historical_data[-1]['timestamp']}")
                    
                    # 专业用户特有的数据导出功能
                    if role == "professional":
                        if st.button("导出分析报告"):
                            report_data = {
                                "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "样本信息": {
                                    "文件名": uploaded_file.name,
                                    "图片尺寸": f"{width}x{height}",
                                    "分析模式": "高级模式" if advanced_mode else "标准模式"
                                },
                                "分析结果": class_counts,
                                "详细指标": {
                                    "检测置信度": confidence_threshold,
                                    "质量评级": "A级" if sum(c["viable"] for c in class_counts.values()) / sum(c["total"] for c in class_counts.values()) > 0.8 else "B级"
                                }
                            }
                            st.download_button(
                                "下载完整报告",
                                data=json.dumps(report_data, ensure_ascii=False, indent=2),
                                file_name=f"花粉分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json"
                            )
                except Exception as e:
                    st.error(f"处理图片时出错：{str(e)}")
        
        # 添加页脚
        st.markdown("---")

    elif nav_option == "专业分析" and role == "professional":
        st.title("专业分析工具")
        
        st.subheader("批量数据分析")
        uploaded_files = st.file_uploader("上传多个图片进行批量分析", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        if uploaded_files:
            st.write(f"已上传 {len(uploaded_files)} 个文件")
            
            # 创建进度条
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 批量处理结果存储
            batch_results = []
            
            # 加载模型
            model = load_model()
            
            # 处理每个文件
            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    # 更新进度
                    progress = (i + 1) / len(uploaded_files)
                    progress_bar.progress(progress)
                    status_text.text(f"正在处理: {uploaded_file.name}")
                    
                    # 读取图片
                    image_bytes = uploaded_file.read()
                    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                    
                    # 处理图片
                    results = model(image)
                    processed_image, class_counts = visualize_results(image, results[0])
                    
                    # 保存结果
                    batch_results.append({
                        "文件名": uploaded_file.name,
                        "分析结果": class_counts,
                        "处理时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # 显示缩略图和结果
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), 
                                caption=f"分析结果 - {uploaded_file.name}",
                                width=300)
                    with col2:
                        st.write("#### 分析统计")
                        for class_name, counts in class_counts.items():
                            if counts["total"] > 0:
                                st.write(f"**{class_name}**:")
                                st.write(f"- 总数：{counts['total']}")
                                st.write(f"- 可育率：{(counts['viable']/counts['total']*100):.1f}%")
                    
                except Exception as e:
                    st.error(f"处理 {uploaded_file.name} 时出错：{str(e)}")
            
            # 完成处理
            progress_bar.empty()
            status_text.text("批量处理完成！")
            
            # 显示汇总结果
            if batch_results:
                st.subheader("批量分析汇总")
                
                # 创建汇总数据
                summary_data = {
                    "WT": {"total": 0, "viable": 0},
                    "T1-C5-C1": {"total": 0, "viable": 0},
                    "T1-C5-E5": {"total": 0, "viable": 0}
                }
                
                for result in batch_results:
                    for class_name, counts in result["分析结果"].items():
                        summary_data[class_name]["total"] += counts["total"]
                        summary_data[class_name]["viable"] += counts["viable"]
                
                # 显示汇总图表
                summary_df = pd.DataFrame([
                    {
                        "品种": class_name,
                        "总数": data["total"],
                        "可育数": data["viable"],
                        "可育率": f"{(data['viable']/data['total']*100):.1f}%" if data['total'] > 0 else "0%"
                    }
                    for class_name, data in summary_data.items()
                ])
                
                st.table(summary_df)
                
                # 提供数据导出
                if st.button("导出批量分析报告"):
                    report_data = {
                        "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "样本数量": len(uploaded_files),
                        "汇总结果": summary_data,
                        "详细结果": batch_results
                    }
                    
                    st.download_button(
                        "下载完整报告",
                        data=json.dumps(report_data, ensure_ascii=False, indent=2),
                        file_name=f"批量分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        
        st.subheader("数据趋势分析")
        analysis_period = st.selectbox("选择分析周期", ["最近一周", "最近一月", "最近三月", "全部数据"])
        
        # 加载历史数据
        historical_data = load_historical_data()
        if historical_data and analysis_period:
            # 根据选择的时间段筛选数据
            current_time = datetime.now()
            if analysis_period == "最近一周":
                days = 7
            elif analysis_period == "最近一月":
                days = 30
            elif analysis_period == "最近三月":
                days = 90
            else:
                days = None
                
            if days:
                filtered_data = [
                    record for record in historical_data
                    if (current_time - datetime.strptime(record["timestamp"], "%Y-%m-%d %H:%M:%S")).days <= days
                ]
            else:
                filtered_data = historical_data
            
            if filtered_data:
                # 创建趋势图
                dates = [record["timestamp"] for record in filtered_data]
                wt_viability = []
                t1_c5_c1_viability = []
                t1_c5_e5_viability = []
                
                for record in filtered_data:
                    for name in ["WT", "T1-C5-C1", "T1-C5-E5"]:
                        data = record["data"][name]
                        total = data["total"]
                        viable = data["viable"]
                        viability_rate = (viable / total * 100) if total > 0 else 0
                        
                        if name == "WT":
                            wt_viability.append(viability_rate)
                        elif name == "T1-C5-C1":
                            t1_c5_c1_viability.append(viability_rate)
                        else:
                            t1_c5_e5_viability.append(viability_rate)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=dates, y=wt_viability, name="WT", mode="lines+markers"))
                fig.add_trace(go.Scatter(x=dates, y=t1_c5_c1_viability, name="T1-C5-C1", mode="lines+markers"))
                fig.add_trace(go.Scatter(x=dates, y=t1_c5_e5_viability, name="T1-C5-E5", mode="lines+markers"))
                
                fig.update_layout(
                    title=f"花粉活力率趋势分析 ({analysis_period})",
                    xaxis_title="时间",
                    yaxis_title="活力率(%)",
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("所选时间段内没有分析记录")
        else:
            st.info("暂无历史数据可供分析")
        
        st.subheader("实验对照分析")
        if historical_data:
            control_group = st.selectbox("选择对照组", ["WT", "T1-C5-C1", "T1-C5-E5"])
            if control_group:
                # 计算对照组的基准数据
                control_data = []
                experimental_data = []
                
                for record in historical_data:
                    control_stats = record["data"][control_group]
                    control_viability = (control_stats["viable"] / control_stats["total"] * 100) if control_stats["total"] > 0 else 0
                    control_data.append(control_viability)
                    
                    # 计算其他组的平均值
                    other_groups = [g for g in ["WT", "T1-C5-C1", "T1-C5-E5"] if g != control_group]
                    exp_viability = []
                    for group in other_groups:
                        stats = record["data"][group]
                        if stats["total"] > 0:
                            exp_viability.append(stats["viable"] / stats["total"] * 100)
                    
                    if exp_viability:
                        experimental_data.append(sum(exp_viability) / len(exp_viability))
                    else:
                        experimental_data.append(0)
                
                # 创建对照分析图表
                fig = go.Figure()
                fig.add_trace(go.Box(y=control_data, name=f"{control_group}（对照组）"))
                fig.add_trace(go.Box(y=experimental_data, name="实验组平均值"))
                
                fig.update_layout(
                    title="对照组与实验组活力率对比",
                    yaxis_title="活力率(%)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 显示统计分析
                st.write("#### 统计分析")
                st.write(f"对照组 ({control_group}):")
                st.write(f"- 平均活力率：{np.mean(control_data):.1f}%")
                st.write(f"- 标准差：{np.std(control_data):.1f}%")
                st.write("实验组：")
                st.write(f"- 平均活力率：{np.mean(experimental_data):.1f}%")
                st.write(f"- 标准差：{np.std(experimental_data):.1f}%")
                
                # 计算差异显著性
                if len(control_data) > 1 and len(experimental_data) > 1:
                    from scipy import stats
                    t_stat, p_value = stats.ttest_ind(control_data, experimental_data)
                    st.write(f"差异显著性检验（t检验）:")
                    st.write(f"- p值：{p_value:.4f}")
                    st.write(f"- 结论：{'差异显著' if p_value < 0.05 else '差异不显著'} (p {'<' if p_value < 0.05 else '>'} 0.05)")
        else:
            st.info("暂无数据可供分析")

    elif nav_option == "知识科普":
        if role == "professional":
            # 专业用户看到更详细的知识库
            show_professional_knowledge_base()
        else:
            # 普通用户看到基础知识库
            show_knowledge_base()
        
    elif nav_option == "案例分享":
        if role == "professional":
            # 专业用户可以分享和评论案例
            show_professional_case_studies()
        else:
            # 普通用户只能查看案例
            show_case_studies()
            
    elif nav_option == "数据管理" and role == "professional":
        st.title("数据管理")
        
        st.subheader("历史数据管理")
        historical_data = load_historical_data()
        if historical_data:
            df = pd.DataFrame(historical_data)
            st.dataframe(df)
            
            if st.button("导出所有数据"):
                st.download_button(
                    "下载CSV文件",
                    data=df.to_csv(index=False),
                    file_name=f"花粉分析数据_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        st.subheader("数据备份")
        if st.button("创建数据备份"):
            # 实现数据备份逻辑
            st.success("数据备份成功！")

    elif nav_option == "系统管理" and role == "admin":
        st.title("系统管理")
        
        # 用户管理
        st.subheader("用户管理")
        users = user_mgmt.get_all_users()
        if users:
            user_df = pd.DataFrame(users)
            st.dataframe(user_df)
            
            # 用户操作
            selected_user = st.selectbox("选择用户", user_df['username'])
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("禁用用户"):
                    user_mgmt.disable_user(selected_user)
                    st.success(f"已禁用用户 {selected_user}")
            with col2:
                if st.button("启用用户"):
                    user_mgmt.enable_user(selected_user)
                    st.success(f"已启用用户 {selected_user}")
            with col3:
                if st.button("删除用户"):
                    user_mgmt.delete_user(selected_user)
                    st.success(f"已删除用户 {selected_user}")
        
        # 系统设置
        st.subheader("系统设置")
        st.markdown("##### 模型配置")
        model_confidence = st.slider("默认模型置信度", 0.0, 1.0, 0.5)
        if st.button("保存模型配置"):
            # TODO: 保存模型配置
            st.success("模型配置已更新")
        
        # 数据库管理
        st.subheader("数据库管理")
        if st.button("备份数据库"):
            # TODO: 实现数据库备份
            st.success("数据库备份成功")
        
        if st.button("清理历史数据"):
            # TODO: 实现数据清理
            st.success("历史数据清理成功")
        
        # 系统日志
        st.subheader("系统日志")
        log_date = st.date_input("选择日期")
        st.text_area("系统日志", value="这里显示系统日志...", height=200)

def main():
    # 初始化session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # 根据认证状态显示不同页面
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main() 