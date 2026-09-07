import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="早鳥計算機", layout="wide")

st.title("早鳥計算機")

st.write("---")

# --- 1. 基本設定（早鳥原價與方案） ---
col1, col2 = st.columns(2)

with col1:
    early_bird_orig = st.number_input(
        "早鳥原價 (円)：", value=16100, step=100
    )

with col2:
    eb_scheme = st.selectbox(
        "選擇早鳥折扣：",
        ["早鳥 30 天 (95折 / -5%)", "早鳥 60 天 (9折 / -10%)", "早鳥 90 天 (85折 / -15%)"],
    )

discount_map = {
    "早鳥 30 天 (95折 / -5%)": 0.95,
    "早鳥 60 天 (9折 / -10%)": 0.90,
    "早鳥 90 天 (85折 / -15%)": 0.85,
}
current_discount = discount_map[eb_scheme]

st.write("---")

# --- 2. 輸入區域（二選一或混合輸入） ---
st.subheader("價格輸入")

col_normal, col_direct_eb = st.columns(2)

with col_normal:
    st.markdown("最新常態價格")
    st.caption("輸入最新常態 1 泊 2 食價格")

with col_direct_eb:
    st.markdown("更新後的早鳥價")
    st.caption("輸入最新早鳥價")

# --- 3. 運算與輸出 ---
results = []

# 處理方式 A（透過常態價格計算）
if normal_prices_input.strip():
    raw_numbers_a = re.findall(
        r"\d+(?:\.\d+)?", normal_prices_input.replace(",", "")
    )
    for p_str in raw_numbers_a:
        p = float(p_str)
        target_eb_price = p * current_discount
        adj_ratio = (
            ((target_eb_price - early_bird_orig) / early_bird_orig) * 100
            if early_bird_orig > 0
            else 0.0
        )

        results.append(
            {
                "計算來源": "常態價格推算",
                "早鳥原價": int(early_bird_orig),
                "常態價格": int(p),
                "目標/更新後早鳥價": int(target_eb_price),
                "比例調整": f"{adj_ratio:+.2f}%",
            }
        )

# 處理方式 B（直接使用更新後的早鳥價）
if direct_eb_input.strip():
    raw_numbers_b = re.findall(
        r"\d+(?:\.\d+)?", direct_eb_input.replace(",", "")
    )
    for eb_str in raw_numbers_b:
        eb_price = float(eb_str)
        adj_ratio = (
            ((eb_price - early_bird_orig) / early_bird_orig) * 100
            if early_bird_orig > 0
            else 0.0
        )

        results.append(
            {
                "計算來源": "直接輸入早鳥價",
                "早鳥原價": int(early_bird_orig),
                "常態價格": "-",
                "目標/更新後早鳥價": int(eb_price),
                "比例調整": f"{adj_ratio:+.2f}%",
            }
        )

# 顯示結果
if results:
    st.write("---")
    st.subheader("計算結果")
    res_df = pd.DataFrame(results)
    st.dataframe(
        res_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "計算來源": st.column_config.TextColumn("計算來源"),
            "早鳥原價": st.column_config.NumberColumn(
                "早鳥原價", format="%d円"
            ),
            "常態價格": st.column_config.TextColumn("常態價格"),
            "目標/更新後早鳥價": st.column_config.NumberColumn(
                "目標/更新後早鳥價", format="%d円"
            ),
            "比例調整": st.column_config.TextColumn("比例調整"),
        },
    )
