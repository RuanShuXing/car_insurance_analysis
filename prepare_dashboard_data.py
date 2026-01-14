import pandas as pd
import numpy as np
from datetime import datetime
import os

print("正在为Excel仪表盘准备汇总数据...")

# 1. 读取原始数据
df = pd.read_csv('D:/experiment/car_insurance_analysis/data/car_insurance_claims.csv', encoding='utf-8-sig')
df['出险时间_dt'] = pd.to_datetime(df['出险时间'])
df['出险年份'] = df['出险时间_dt'].dt.year
df['出险月份'] = df['出险时间_dt'].dt.month

# 2. 创建第一个工作表：原始数据（供透视表使用）
raw_data_for_pivot = df[['出险时间_dt', '出险年份', '出险月份', '车型类别', '客户年龄', '投保地区', '出险原因', '理赔金额(元)']].copy()

# 3. 创建第二个工作表：预聚合的月度趋势数据（用于固定图表）
monthly_trend = df.groupby(['出险年份', '出险月份']).agg(
    理赔次数=('理赔金额(元)', 'count'),
    总理赔金额=('理赔金额(元)', 'sum'),
    平均理赔金额=('理赔金额(元)', 'mean')
).round(2).reset_index()
monthly_trend['年月'] = monthly_trend['出险年份'].astype(str) + '年' + monthly_trend['出险月份'].astype(str).str.zfill(2) + '月'

# 4. 创建第三个工作表：各维度汇总（用于下拉菜单或展示）
dimension_summary = []
# 按车型汇总
car_type_summary = df.groupby('车型类别').agg(理赔次数=('理赔金额(元)', 'count'), 总理赔金额=('理赔金额(元)', 'sum')).round(2)
car_type_summary['维度'] = '车型类别'
car_type_summary = car_type_summary.reset_index().rename(columns={'车型类别': '维度值'})
dimension_summary.append(car_type_summary)

# 按出险原因汇总
reason_summary = df.groupby('出险原因').agg(理赔次数=('理赔金额(元)', 'count'), 总理赔金额=('理赔金额(元)', 'sum')).round(2)
reason_summary['维度'] = '出险原因'
reason_summary = reason_summary.reset_index().rename(columns={'出险原因': '维度值'})
dimension_summary.append(reason_summary)

# 合并
final_summary = pd.concat(dimension_summary, ignore_index=True)

# 5. 写入Excel文件
output_path = 'D:/experiment/car_insurance_analysis/data/dashboard_data_source.xlsx'
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    raw_data_for_pivot.to_excel(writer, sheet_name='原始数据', index=False)
    monthly_trend.to_excel(writer, sheet_name='月度趋势', index=False)
    final_summary.to_excel(writer, sheet_name='维度汇总', index=False)

print(f"数据准备完成！已生成数据源文件：{output_path}")
print("接下来，请打开此文件，按照指南创建仪表盘。")