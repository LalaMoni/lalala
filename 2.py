import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 基准参数
base_revenue = 100.0
base_gross_margin_rate = 0.3734
base_labor_cost_rate = 0.1792
base_platform_fee_rate = 0.4738

def calc_net_profit_rate(g, h, p, m):
    new_revenue = base_revenue * (1 + g)
    new_labor_cost = base_labor_cost_rate * base_revenue * (1 + h)
    new_platform_fee = base_platform_fee_rate * base_revenue * (1 + p)
    new_gross_margin_rate = base_gross_margin_rate + m
    new_gross_margin = new_revenue * new_gross_margin_rate
    new_net_profit = new_gross_margin - new_labor_cost - new_platform_fee
    new_net_profit_rate = new_net_profit / new_revenue
    return new_net_profit_rate * 100  # 百分比

st.title("净营业利润率敏感性分析")

st.sidebar.header("参数调整（其他参数保持当前值）")

# 滑块去掉 % 格式，使用普通浮点数格式
g_input = st.sidebar.slider("收入增长率", 0.0, 0.4, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前收入增长率: {g_input*100:.2f}%")

h_input = st.sidebar.slider("人力成本变动", -0.2, 0.05, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前人力成本变动: {h_input*100:.2f}%")

p_input = st.sidebar.slider("平台费变动", -0.3, 0.0, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前平台费变动: {p_input*100:.2f}%")

m_input = st.sidebar.slider("毛利率变动", 0.0, 0.06, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前毛利率变动: {m_input*100:.2f}%")

var_to_plot = st.selectbox("选择模拟参数", ["收入增长率", "人力成本变动", "平台费变动", "毛利率变动"])

# 生成绘图用的x轴数据（参数变化范围）
if var_to_plot == "收入增长率":
    x_vals = np.linspace(0, 0.4, 50)
elif var_to_plot == "人力成本变动":
    x_vals = np.linspace(-0.2, 0.05, 50)
elif var_to_plot == "平台费变动":
    x_vals = np.linspace(-0.3, 0.0, 50)
else:  # 毛利率变动 m
    x_vals = np.linspace(0.0, 0.06, 50)

net_profit_rates = []
for val in x_vals:
    g = val if var_to_plot == "收入增长率" else g_input
    h = val if var_to_plot == "人力成本变动" else h_input
    p = val if var_to_plot == "平台费变动" else p_input
    m = val if var_to_plot == "毛利率变动" else m_input
    net_profit_rates.append(calc_net_profit_rate(g, h, p, m))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_vals*100, y=net_profit_rates, mode='lines+markers', name="净营业利润率 (%)"))
fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="盈亏平衡线", annotation_position="bottom right")

fig.update_layout(
    title=f"敏感性分析: {var_to_plot} 对净营业利润率的影响",
    xaxis_title=f"{var_to_plot} (%)",
    yaxis_title="净营业利润率 (%)",
    yaxis_range=[min(net_profit_rates)-5, max(net_profit_rates)+5],
    width=800,
    height=500,
)

st.plotly_chart(fig, use_container_width=True)

current_net_profit_rate = calc_net_profit_rate(g_input, h_input, p_input, m_input)
color = "green" if current_net_profit_rate > 0 else "red"
st.markdown(f"### 当前净营业利润率: <span style='color:{color}; font-size:32px'>{current_net_profit_rate:.2f}%</span>", unsafe_allow_html=True)

st.markdown(f"""
**当前参数值：**  
- 收入增长率 g: {g_input*100:.2f}%  
- 人力成本变动 h: {h_input*100:.2f}%  
- 平台费变动 p: {p_input*100:.2f}%  
- 毛利率变动 m: {m_input*100:.2f}%  
""")
