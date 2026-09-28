import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="過灘時間與潮窗計算系統",
    page_icon="🚢",
    layout="centered"
)

st.title("🚢 過灘時間與潮窗計算系統")
st.caption("高雄港二航道 (設計水深 17.0m) 靜態 UKC 評估系統")

channel_depth = 17.0
draft = st.number_input("船舶吃水 (m)", min_value=5.0, max_value=25.0, value=16.0, step=0.1)

mock_data = [
    {"時間": "00:00", "預報潮高": 0.50},
    {"時間": "02:00", "預報潮高": 0.20},
    {"時間": "04:00", "預報潮高": 0.00},
    {"時間": "06:00", "預報潮高": 0.40},
    {"時間": "08:00", "預報潮高": 0.90},
    {"時間": "10:00", "預報潮高": 1.30},
    {"時間": "12:00", "預報潮高": 1.50},
    {"時間": "14:00", "預報潮高": 1.20},
    {"時間": "16:00", "預報潮高": 0.80},
    {"時間": "18:00", "預報潮高": 0.30},
    {"時間": "20:00", "預報潮高": 0.10},
    {"時間": "22:00", "預報潮高": 0.60},
]

results = []
for row in mock_data:
    tide = row["預報潮高"]
    avail_depth = channel_depth + tide
    ukc = avail_depth - draft
    ukc_pct = (ukc / draft) * 100
    
    if ukc_pct >= 15.0:
        status = "🟢 安全通行"
    elif ukc_pct >= 10.0:
        status = "🟡 限制通行"
    else:
        status = "🔴 禁止過灘"
        
    results.append({
        "時間": row["時間"],
        "潮高(m)": f"{tide:.2f}",
        "可用水深(m)": f"{avail_depth:.2f}",
        "UKC %": f"{ukc_pct:.1f}%",
        "狀態": status
    })

df = pd.DataFrame(results)

st.subheader("過灘時間視窗 (Tidal Window)")
green_count = sum(1 for r in results if "🟢" in r["狀態"])
yellow_count = sum(1 for r in results if "🟡" in r["狀態"])
red_count = sum(1 for r in results if "🔴" in r["狀態"])

col1, col2, col3 = st.columns(3)
col1.metric("🟢 可通行", f"{green_count * 2}hr")
col2.metric("🟡 限制", f"{yellow_count * 2}hr")
col3.metric("🔴 禁止", f"{red_count * 2}hr")

st.write("---")
st.dataframe(df, use_container_width=True)
