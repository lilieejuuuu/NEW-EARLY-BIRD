import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="早鳥計算機", layout="wide")

st.title("早鳥計算機")
st.write("輸入原本早鳥價與最新價格，自動算出建議調整比例。")

st.write("---")

# 1. 基本設定
col1, col2 = st.columns(2)

with col1:
    early_bird_orig = st.number_input(
        "原本早鳥價 (円)：", value=13300, step=100
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

# 2. 輸入更改後的常態價格
st.subheader("更改後的常態價格")
normal_prices_input = st.text_area(
    "請貼上最新常態價格（可一次貼上多筆，支援空格、換行或逗號）：",
    value="15900\n13680",
)

# 3. 解析與計算
if normal_prices_input.strip():
    # 使用正則表達式提取所有數字（自動忽略逗號與文字）
    raw_numbers = re.findall(r"\d+(?:\.\d+)?", normal_prices_input.replace(",", ""))
    prices = [float(n) for n in raw_numbers]

    results = []
    for p in prices:
        # 計算目標早鳥價 (新常態價 * 折扣)
        target_eb_price = p * current_discount

        # 計算相較於原本早鳥價的調整 % 數
        if early_bird_orig > 0:
            adj_ratio = (
                (target_eb_price - early_bird_orig) / early_bird_orig
            ) * 100
        else:
            adj_ratio = 0.0

        results.append(
            {
                "原本早鳥價": int(early_bird_orig),
                "新常態價格": int(p),
                "目標早鳥價": int(target_eb_price),
                "比例調整": f"{adj_ratio:+.2f}%",
            }
        )

    if results:
        st.write("---")
        st.subheader("計算結果")
        res_df = pd.DataFrame(results)
        st.dataframe(
            res_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "原本早鳥價": st.column_config.NumberColumn(
                    "原本早鳥價", format="%d円"
                ),
                "新常態價格": st.column_config.NumberColumn(
                    "新常態價格", format="%d円"
                ),
                "目標早鳥價": st.column_config.NumberColumn(
                    "目標早鳥價", format="%d円"
                ),
                "比例調整": st.column_config.TextColumn("比例調整"),
            },
        )
