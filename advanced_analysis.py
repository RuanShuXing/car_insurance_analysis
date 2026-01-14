import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime

#找到字体并创建字体属性
import matplotlib.font_manager as fm

# 尝试寻找系统中文字体文件(虽然字体部分有点绕有点累赘但是不建议改动)
font_path = None
# 常见中文字体路径列表依次尝试
possible_font_paths = [
    r'C:\Windows\Fonts\msyh.ttc',          # 微软雅黑常规
    r'C:\Windows\Fonts\msyhbd.ttc',        # 微软雅黑粗体
    r'C:\Windows\Fonts\simhei.ttf',        # 黑体
    r'C:\Windows\Fonts\simsun.ttc',        # 宋体
]
for fp in possible_font_paths:
    if os.path.exists(fp):
        font_path = fp
        print(f"* 找到字体文件：{fp}")
        break

if font_path is None:
    # 如果都没找到，尝试用font_manager列出所有字体，手动选择一个
    print("* 未在标准路径找到字体，正在扫描系统字体...")
    for font in fm.fontManager.ttflist:
        if 'YaHei' in font.name or 'SimHei' in font.name:
            font_path = font.fname
            print(f"* 找到备用字体：{font.name} - {font_path}")
            break

if font_path and os.path.exists(font_path):
    # 创建字体属性对象，后续直接使用
    chinese_font_prop = fm.FontProperties(fname=font_path)
    print(f"* 成功加载字体属性：{chinese_font_prop.get_name()}")
else:
    print("* 警告：未找到合适的中文字体文件，图表将无法显示中文。")
    chinese_font_prop = None

# 全局样式
plt.style.use('seaborn-v0_8-darkgrid')
# 2. 读取数据
print("正在读取数据...")
df = pd.read_csv('D:/experiment/car_insurance_analysis/data/car_insurance_claims.csv', encoding='utf-8-sig')

# 3. 计算关键指标：赔付率 (理赔金额/保费)
# 模拟一个保费：假设保费是理赔金额的某个随机比例
np.random.seed(42)  # 固定随机种子，确保结果可复现
df['模拟保费(元)'] = df['理赔金额(元)'] * np.random.uniform(1.5, 3.0, size=len(df))
# 单条记录的赔付率
df['单笔赔付率'] = df['理赔金额(元)'] / df['模拟保费(元)']

# 整体关键指标
total_premium = df['模拟保费(元)'].sum()
total_claim = df['理赔金额(元)'].sum()
overall_loss_ratio = total_claim / total_premium

print("="*50)
print(f"核心业务指标计算结果：")
print(f"  总理赔金额：{total_claim:,.2f} 元")
print(f"  总模拟保费：{total_premium:,.2f} 元")
print(f"  整体赔付率：{overall_loss_ratio:.2%}")  # 格式化为百分比
print("="*50)

# 4. 确保输出目录存在
output_dir = r'D:\experiment\car_insurance_analysis\output'
os.makedirs(output_dir, exist_ok=True)

# ---------------------- 可视化1：不同年龄段平均理赔金额（柱状图）
print("\n正在生成图表1：不同年龄段平均理赔金额对比...")

# 定义年龄分段
bins = [0, 25, 40, 60, 100]
labels = ['青年 (≤25)', '中青年 (26-40)', '中年 (41-60)', '老年 (>60)']
df['年龄段'] = pd.cut(df['客户年龄'], bins=bins, labels=labels, right=False)

# 分组计算
age_group_stats = df.groupby('年龄段').agg(
    记录数=('理赔金额(元)', 'count'),
    平均理赔金额=('理赔金额(元)', 'mean'),
    总理赔金额=('理赔金额(元)', 'sum')
).round(2)

# 创建图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 子图1：平均理赔金额柱状图
bars = ax1.bar(age_group_stats.index.astype(str), age_group_stats['平均理赔金额'], color='skyblue', edgecolor='black')
ax1.set_title('各年龄段平均理赔金额对比', fontsize=14, fontweight='bold', fontproperties=chinese_font_prop)
ax1.set_ylabel('平均理赔金额 (元)', fontsize=12, fontproperties=chinese_font_prop)
ax1.set_xlabel('年龄段', fontsize=12, fontproperties=chinese_font_prop)
# 柱子上添加数值标签
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
             f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

# 子图2：各年龄段理赔总金额占比（饼图）
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
wedges, texts, autotexts = ax2.pie(age_group_stats['总理赔金额'], labels=age_group_stats.index, autopct='%1.1f%%',
                                   colors=colors, startangle=90)
ax2.set_title('各年龄段理赔总金额占比', fontsize=14, fontweight='bold', fontproperties=chinese_font_prop)
# 饼图的标签（texts）和百分比（autotexts）设置字体
for text in texts:
    text.set_fontproperties(chinese_font_prop)
for autotext in autotexts:
    autotext.set_fontproperties(chinese_font_prop)
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.suptitle('车险理赔 - 年龄段分析', fontsize=16, fontweight='bold', fontproperties=chinese_font_prop)
plt.tight_layout()

if chinese_font_prop:
    plt.rcParams['font.sans-serif'] = [chinese_font_prop.get_name()]
plt.savefig(os.path.join(output_dir, '1_年龄段_平均理赔金额与占比.png'), dpi=300, bbox_inches='tight')
print(f"  图表已保存至：{output_dir}/1_年龄段_平均理赔金额与占比.png")

# ---------------------- 可视化2：月度理赔次数趋势（折线图）
print("\n正在生成图表2：月度理赔次数趋势...")

# 将出险时间转换为日期时间格式，并提取年月
df['出险时间_dt'] = pd.to_datetime(df['出险时间'])
df['出险年月'] = df['出险时间_dt'].dt.to_period('M').astype(str)  # e.g. "2023-01"

# 按年月分组统计
monthly_claims = df.groupby('出险年月').agg(
    理赔次数=('理赔金额(元)', 'count'),
    平均金额=('理赔金额(元)', 'mean')
).reset_index()

# 创建图表
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('出险年月', fontsize=12)
ax1.set_ylabel('理赔次数', color=color, fontsize=12)
line1 = ax1.plot(monthly_claims['出险年月'], monthly_claims['理赔次数'],
                 marker='o', color=color, linewidth=2, label='理赔次数')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_title('月度理赔次数与平均金额趋势', fontsize=14, fontweight='bold')
# 旋转X轴标签，避免重叠
plt.xticks(rotation=45)

# 创建第二个Y轴，展示平均金额
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('平均理赔金额 (元)', color=color, fontsize=12)
line2 = ax2.plot(monthly_claims['出险年月'], monthly_claims['平均金额'],
                 marker='s', color=color, linewidth=2, linestyle='--', label='平均金额')
ax2.tick_params(axis='y', labelcolor=color)

# 合并图例
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '2_月度理赔次数与平均金额趋势.png'), dpi=300, bbox_inches='tight')
print(f"  图表已保存至：{output_dir}/2_月度理赔次数与平均金额趋势.png")

# ---------------------- 可视化3：出险原因与车型的交叉分析（热力图）
print("\n正在生成图表3：出险原因与车型交叉分析...")

# 创建交叉表，计算不同组合下的平均理赔金额
pivot_table = pd.pivot_table(df, values='理赔金额(元)', index='出险原因',
                             columns='车型类别', aggfunc='mean', fill_value=0).round(2)

# 创建热力图
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(pivot_table.values, cmap='YlOrRd')  # 黄-橙-红色系

# 设置坐标轴
ax.set_xticks(np.arange(len(pivot_table.columns)))
ax.set_yticks(np.arange(len(pivot_table.index)))
ax.set_xticklabels(pivot_table.columns)
ax.set_yticklabels(pivot_table.index)

# 每个单元格中显示数值
for i in range(len(pivot_table.index)):
    for j in range(len(pivot_table.columns)):
        text = ax.text(j, i, f'{pivot_table.iloc[i, j]:,.0f}',
                       ha="center", va="center", color="black" if pivot_table.iloc[i, j] < pivot_table.values.max()/2 else "white")

ax.set_title('不同出险原因与车型的平均理赔金额热力图 (元)', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax, label='平均理赔金额 (元)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '3_出险原因与车型_平均理赔金额热力图.png'), dpi=300, bbox_inches='tight')
print(f"  图表已保存至：{output_dir}/3_出险原因与车型_平均理赔金额热力图.png")

# ---------------------- 保存关键指标到文本文件
print("\n正在保存关键指标摘要...")
summary_text = f"""车险理赔数据分析项目 - 关键指标摘要
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据分析范围：共 {len(df)} 条理赔记录

【核心业务指标】
1. 总理赔金额：{total_claim:,.2f} 元
2. 总模拟保费：{total_premium:,.2f} 元
3. 整体赔付率：{overall_loss_ratio:.2%}

【年龄段分析】
{age_group_stats.to_string()}

【月度趋势分析】
观测期：{monthly_claims['出险年月'].iloc[0]} 至 {monthly_claims['出险年月'].iloc[-1]}
月均理赔次数：{monthly_claims['理赔次数'].mean():.1f} 次
理赔次数最高月份：{monthly_claims.loc[monthly_claims['理赔次数'].idxmax(), '出险年月']} ({monthly_claims['理赔次数'].max()} 次)
"""
with open(os.path.join(output_dir, 'analysis_summary.txt'), 'w', encoding='utf-8') as f:
    f.write(summary_text)
print(f"  摘要已保存至：{output_dir}/analysis_summary.txt")

print("\n" + "="*50)
print("高级分析与可视化步骤全部完成！")
print(f"请查看 '{output_dir}' 文件夹下的所有生成文件。")
print("="*50)

# 可选：在控制台显示关键图表
plt.show()