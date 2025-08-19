import streamlit as st
import pandas as pd
from datetime import datetime
import os
from case_management import CaseManagement

def show_knowledge_base():
    """显示知识科普页面"""
    st.title("水稻花粉知识库")
    
    # 侧边栏导航
    category = st.sidebar.selectbox(
        "选择分类",
        ["基础知识", "研究方法", "最新进展", "案例分析"]
    )
    
    if category == "基础知识":
        st.header("水稻花粉基础知识")
        
        st.subheader("1. 水稻花粉的形态特征")
        st.write("""
        水稻花粉粒呈圆形或椭圆形，具有以下特征：
        - 大小：直径约为35-45微米
        - 外壁：具有特殊的纹饰结构
        - 萌发孔：单孔，位于赤道部位
        """)
        
        st.subheader("2. 花粉活力的定义")
        st.write("""
        花粉活力是指花粉粒具有正常生长发育和完成受精功能的能力，主要表现为：
        - 细胞质密度
        - 代谢活性
        - 萌发能力
        """)
        
    elif category == "研究方法":
        st.header("花粉研究方法")
        
        st.subheader("1. 采样方法")
        st.write("""
        正确的采样对于研究结果至关重要：
        - 选择适当的采样时间
        - 使用合适的采样工具
        - 正确的保存方法
        """)
        
        st.subheader("2. 活力检测方法")
        st.write("""
        常用的花粉活力检测方法包括：
        - TTC染色法
        - FDA染色法
        - 体外萌发法
        - AI图像分析法
        """)
        
    elif category == "最新进展":
        st.header("研究最新进展")
        
        st.subheader("1. 新技术应用")
        st.write("""
        近年来花粉研究领域的新技术包括：
        - 人工智能图像分析
        - 高通量筛选技术
        - 单细胞测序技术
        """)
        
        st.subheader("2. 研究热点")
        st.write("""
        当前研究热点包括：
        - 气候变化对花粉活力的影响
        - 花粉发育的分子机制
        - 杂种优势利用
        """)
        
    else:  # 案例分析
        st.header("典型案例分析")
        
        st.subheader("1. 实际应用案例")
        st.write("""
        以下是一些典型的应用案例：
        - 杂交水稻育种中的花粉活力筛选
        - 环境胁迫对花粉活力的影响评估
        - 农艺措施对花粉活力的调控
        """)
        
        st.subheader("2. 问题解决方案")
        st.write("""
        常见问题的解决方案：
        - 花粉活力低下的改善措施
        - 采样保存技术优化
        - 检测效率提升方法
        """)

def show_case_studies():
    """显示案例分享页面"""
    st.title("案例分享")
    
    # 案例列表
    cases = [
        {
            "title": "南方稻区花粉活力研究",
            "description": "研究南方水稻主产区不同品种花粉活力特征...",
            "results": "发现温度和湿度是影响花粉活力的主要因素..."
        },
        {
            "title": "杂交水稻育种应用",
            "description": "在杂交水稻育种过程中应用AI辅助筛选...",
            "results": "提高育种效率30%，选育成功2个优质品种..."
        }
    ]
    
    for case in cases:
        st.subheader(case["title"])
        st.write("研究描述：", case["description"])
        st.write("研究结果：", case["results"])
        st.markdown("---")

def show_professional_knowledge_base():
    """显示专业用户知识库"""
    st.title("水稻花粉专业知识库")
    
    # 侧边栏导航
    category = st.sidebar.selectbox(
        "选择分类",
        ["专业知识", "研究方法", "最新进展", "实验技术", "数据分析", "文献资料"]
    )
    
    if category == "专业知识":
        st.header("专业知识")
        
        st.subheader("1. 花粉发育的分子机制")
        st.write("""
        花粉发育过程中的关键基因和信号通路：
        - GAMYB转录因子家族
        - 植物激素调控网络
        - 细胞程序性死亡机制
        """)
        
        st.subheader("2. 花粉活力的生化指标")
        st.write("""
        活力评估的关键生化指标：
        - 酯酶活性
        - 线粒体活性
        - 膜完整性
        - 细胞质流动性
        """)
        
    elif category == "实验技术":
        st.header("实验技术详解")
        
        st.subheader("1. 高级染色技术")
        st.write("""
        专业染色方法及注意事项：
        - FDA染色的最佳条件
        - TTC染色的温度控制
        - 多重染色技术
        - 活体成像技术
        """)
        
        st.subheader("2. 显微观察技术")
        st.write("""
        显微镜观察的专业技巧：
        - 焦平面的选择
        - 光强的调节
        - 分辨率的优化
        - 图像采集参数
        """)
        
    elif category == "文献资料":
        st.header("相关文献资料")
        
        # 文献数据
        literature_data = pd.DataFrame({
            "标题": ["水稻花粉活力研究进展", "花粉发育的分子机制", "活力检测新方法"],
            "作者": ["张三等", "李四等", "王五等"],
            "期刊": ["中国水稻科学", "植物学报", "作物学报"],
            "年份": [2023, 2022, 2023],
            "DOI": ["10.xxxx/yyyy", "10.xxxx/zzzz", "10.xxxx/wwww"]
        })
        
        st.dataframe(literature_data)
        
        st.subheader("文献下载")
        st.write("请联系管理员获取文献全文访问权限")

def show_professional_case_studies():
    """显示专业用户案例分享平台"""
    st.title("专业案例分享平台")
    
    # 初始化案例管理器
    case_manager = CaseManagement()
    
    # 添加新案例
    st.subheader("分享新案例")
    with st.form("case_form"):
        title = st.text_input("案例标题")
        description = st.text_area("研究描述")
        methods = st.text_area("研究方法")
        results = st.text_area("研究结果")
        conclusions = st.text_area("结论与展望")
        
        # 上传相关图片
        images = st.file_uploader("上传案例相关图片", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        # 添加标签
        tags = st.multiselect(
            "添加标签",
            ["育种", "栽培", "生理", "基因", "环境胁迫", "其他"],
            default=["其他"]
        )
        
        submitted = st.form_submit_button("提交案例")
        if submitted and title and description:  # 确保必填字段已填写
            # 保存案例
            success, case_id = case_manager.add_case(
                title=title,
                description=description,
                methods=methods,
                results=results,
                conclusions=conclusions,
                author=st.session_state.get('username', '匿名用户'),
                tags=tags
            )
            
            if success:
                # 保存图片
                if images:
                    os.makedirs('case_images', exist_ok=True)
                    for img in images:
                        img_path = os.path.join('case_images', f"{case_id}_{img.name}")
                        with open(img_path, 'wb') as f:
                            f.write(img.getbuffer())
                        case_manager.add_case_image(case_id, img_path)
                
                st.success("案例提交成功！")
            else:
                st.error("案例提交失败，请稍后重试。")
    
    # 显示现有案例
    st.subheader("最新案例")
    
    # 筛选和排序选项
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("排序方式", ["最新发布", "最多评论", "最多点赞"])
    with col2:
        filter_tags = st.multiselect("按标签筛选", ["育种", "栽培", "生理", "基因", "环境胁迫", "其他"])
    
    # 获取案例列表
    cases = case_manager.get_cases(sort_by=sort_by, tags=filter_tags)
    
    # 显示案例
    for case in cases:
        with st.expander(f"{case['title']} - {case['author']} ({case['date']})"):
            st.write("**研究描述：**", case["description"])
            st.write("**研究方法：**", case["methods"])
            st.write("**研究结果：**", case["results"])
            st.write("**结论与展望：**", case["conclusions"])
            st.write("**标签：**", ", ".join(case["tags"]))
            
            # 显示图片
            if case['images']:
                cols = st.columns(min(len(case['images']), 3))
                for idx, img_path in enumerate(case['images']):
                    if os.path.exists(img_path):
                        cols[idx % 3].image(img_path)
            
            # 点赞功能
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"👍 {case['likes']}", key=f"like_{case['id']}"):
                    if case_manager.like_case(case['id']):
                        st.experimental_rerun()
            
            # 评论区
            st.subheader(f"评论区 ({case['comment_count']})")
            comments = case_manager.get_case_comments(case['id'])
            for comment in comments:
                st.text(f"{comment['username']} ({comment['date']})")
                st.write(comment['content'])
                st.markdown("---")
            
            # 添加评论
            if 'user_id' in st.session_state:
                comment = st.text_area("发表评论", key=f"comment_{case['id']}")
                if st.button("提交评论", key=f"submit_comment_{case['id']}"):
                    if case_manager.add_comment(case['id'], st.session_state['user_id'], comment):
                        st.success("评论提交成功！")
                        st.experimental_rerun()
                    else:
                        st.error("评论提交失败，请稍后重试。")
            else:
                st.warning("请登录后发表评论") 