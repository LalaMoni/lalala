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

g_input = st.sidebar.slider("收入增长率", 0.0, 0.4, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前收入增长率: {g_input*100:.2f}%")

h_input = st.sidebar.slider("人力成本变动", -0.2, 0.1, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前人力成本变动: {h_input*100:.2f}%")

p_input = st.sidebar.slider("平台费变动", -0.3, 0.0, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前平台费变动: {p_input*100:.2f}%")

m_input = st.sidebar.slider("毛利率变动", 0.0, 0.12, 0.0, 0.01, format="%.2f")
st.sidebar.write(f"当前毛利率变动: {m_input*100:.2f}%")

# 分析部分

scenario_var = st.selectbox("选择要对比的变量", ["毛利率变动", "人力成本变动", "平台费变动"])
x_vals = np.linspace(0, 0.4, 50)

# 不同变量的对比值设定
if scenario_var == "毛利率变动":
    scenario_values = [0.00, 0.04, 0.08, 0.12]
elif scenario_var == "人力成本变动":
    scenario_values = [-0.20, -0.10, 0.00, 0.10]
else:  # 平台费变动 p
    scenario_values = [-0.30, -0.20, -0.10, 0.00]

fig = go.Figure()

for val in scenario_values:
    net_profit_rates = []
    for g in x_vals:
        h = h_input
        p = p_input
        m = m_input
        if scenario_var == "毛利率变动":
            m = val
        elif scenario_var == "人力成本变动":
            h = val
        elif scenario_var == "平台费变动":
            p = val
        net_profit_rates.append(calc_net_profit_rate(g, h, p, m))
    
    fig.add_trace(go.Scatter(
        x=x_vals * 100,
        y=net_profit_rates,
        mode='lines+markers',
        name=f"{scenario_var} = {val*100:.0f}%"
    ))

fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="盈亏平衡线", annotation_position="bottom right")

fig.update_layout(
    title=f"多场景对比：不同 {scenario_var} 下的净营业利润率变化",
    xaxis_title="收入增长率 (%)",
    yaxis_title="净营业利润率 (%)",
    width=800,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# 当前净利润率计算
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
