# streamlit run RAG项目案例\app_file_uploader.py

import time
import streamlit as st
import config_data as config
from knowledge_base import KnowledgeBaseService

# 标题区域
st.title("📚知识库更新服务")
st.divider()  # 分隔符

# 初始化知识库服务
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()
    st.session_state["upload_history"] = []  # 记录上传历史

# 文件上传区域
st.subheader("文件上传")
uploader_file_list = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=True,  # True表示接受多个文件的上传
)

# 文件处理逻辑：遍历文件列表
if uploader_file_list is not None and len(uploader_file_list) > 0:
    # 循环遍历每一个上传文件
    for uploader_file in uploader_file_list:
        # 提取单个文件的信息
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size / 1024  # KB

        # 显示文件信息
        with st.expander(f"📄 文件信息 - {file_name}", expanded=True):
            st.write(f"文件名：{file_name}")
            st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

        # 读取文件内容并处理
        text = uploader_file.getvalue().decode("utf-8")

        with st.spinner(f"[{file_name}] 载入知识库中..."):  # 转圈加载动画
            time.sleep(1)
            result = st.session_state["service"].upload_by_str(text, file_name)
            st.success(f"{file_name}：{result}")

            # 记录上传历史
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
    st.header("ℹ️ 帮助信息")
    st.info("""
    - 仅支持TXT格式文件上传
    - 重复内容会自动跳过，避免重复入库
    - 上传后的内容会立即加入向量知识库
    - 点击重置按钮可重启知识库服务
    """)
    st.divider()
    st.subheader("📊 上传统计")
    st.write(f"总上传次数：{len(st.session_state['upload_history'])}")
    success_uploads = len([r for r in st.session_state["upload_history"] if "成功" in r["status"]])
    st.write(f"成功上传：{success_uploads} 次")
    skip_uploads = len([r for r in st.session_state["upload_history"] if "跳过" in r["status"]])
    st.write(f"跳过重复：{skip_uploads} 次")