# streamlit run RAG项目案例\app_file_uploader.py

import time
import streamlit as st
import config_data as config
from knowledge_base import KnowledgeBaseService

st.set_page_config(page_title="FitBot 知识库管理", page_icon="📚", layout="wide")

# 标题区域
st.title("📚 FitBot 知识库管理")
st.caption("上传健身营养知识文档，丰富FitBot的专业知识库")
st.divider()

# 初始化知识库服务
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()
    st.session_state["upload_history"] = []

# 文件上传区域
st.subheader("📤 文件上传")
st.info("支持上传健身训练计划、营养饮食指南、运动补剂知识、减脂增肌策略等TXT文档。")
uploader_file_list = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=True,
)

# 文件处理逻辑：遍历文件列表
if uploader_file_list is not None and len(uploader_file_list) > 0:
    for uploader_file in uploader_file_list:
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size / 1024

        with st.expander(f"📄 文件信息 - {file_name}", expanded=True):
            st.write(f"文件名：{file_name}")
            st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

        text = uploader_file.getvalue().decode("utf-8")

        with st.spinner(f"[{file_name}] 载入FitBot知识库中..."):
            time.sleep(1)
            result = st.session_state["service"].upload_by_str(text, file_name)
            st.success(f"{file_name}：{result}")

            upload_record = {
                "filename": file_name,
                "size": f"{file_size:.2f} KB",
                "status": result,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state["upload_history"].append(upload_record)

# 上传历史展示
if st.session_state["upload_history"]:
    st.divider()
    st.subheader("📋 上传历史")
    for idx, record in enumerate(st.session_state["upload_history"], 1):
        with st.container(border=True):
            col1, col2, col3 = st.columns([0.4, 0.3, 0.3])
            with col1:
                st.write(f"文件：{record['filename']}")
            with col2:
                st.write(f"大小：{record['size']}")
            with col3:
                st.write(f"时间：{record['time']}")
            st.write(f"状态：{record['status']}")

# 侧边栏信息
with st.sidebar:
    st.header("ℹ️ 使用说明")
    st.info("""
    **FitBot知识库管理** 用于维护和更新FitBot的健身营养知识库。
    
    **使用步骤：**
    1. 准备好TXT格式的健身营养知识文档
    2. 点击上传按钮选择文件
    3. 系统自动将内容向量化存入知识库
    4. 上传后FitBot即可基于新知识回答相关问题
    
    **注意事项：**
    - 仅支持TXT格式文件
    - 重复内容会自动跳过，避免重复入库
    - 建议文件内容与健身、营养、训练相关
    """)
    st.divider()
    st.subheader("📊 上传统计")
    st.write(f"总上传次数：{len(st.session_state['upload_history'])}")
    success_uploads = len([r for r in st.session_state["upload_history"] if "成功" in r["status"]])
    st.write(f"成功上传：{success_uploads} 次")
    skip_uploads = len([r for r in st.session_state["upload_history"] if "跳过" in r["status"]])
    st.write(f"跳过重复：{skip_uploads} 次")
    st.divider()
    st.subheader("📂 已内置知识库")
    st.write("""
    - 🥗 营养饮食指南
    - 🏋️ 健身训练计划
    - 💊 运动营养补剂
    - 📉 减脂增肌策略
    """)