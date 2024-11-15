import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel处理工具", layout="centered")

# 设置页面样式
st.markdown("""
    <style>
        .stApp {
            max-width: 800px;
            margin: 0 auto;
        }
        .upload-text {
            font-size: 16px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# 标题
st.title("Excel处理工具")

# 文件上传
uploaded_file = st.file_uploader("请选择Excel文件", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # 读取Excel文件
        df = pd.read_excel(uploaded_file)
        
        # 获取第一列数据
        first_column = df.iloc[:, 0].tolist()
        
        # 存储拆分后的所有号码
        split_numbers = []
        
        # 处理每一行数据
        for cell in first_column:
            if pd.notna(cell):
                numbers = str(cell).split('|')
                split_numbers.extend(numbers)
        
        # 创建新的DataFrame
        new_df = pd.DataFrame(split_numbers, columns=['Numbers'])
        
        # 创建输出的Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            new_df.to_excel(writer, index=False)
        
        # 提供下载按钮
        st.download_button(
            label="下载处理后的文件",
            data=output.getvalue(),
            file_name="processed_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # 显示预览
        st.subheader("数据预览")
        st.dataframe(new_df)
        
    except Exception as e:
        st.error(f"处理文件时出错：{str(e)}")
