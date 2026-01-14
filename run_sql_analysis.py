import sqlite3
import pandas as pd

# 连接到刚创建的数据库
conn = sqlite3.connect('D:/experiment/car_insurance_analysis/insurance.db')

print("开始进行车险理赔数据探索分析...\n")
print("="*50)

# 查询1：最常见的出险原因是什么？ (GROUP BY)
query1 = """
SELECT 
    出险原因,
    COUNT(*) AS 出险次数,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS 占比百分比
FROM claims
GROUP BY 出险原因
ORDER BY 出险次数 DESC;
"""
print("1. 【最常见的出险原因分析】")
df1 = pd.read_sql_query(query1, conn)
print(df1.to_string(index=False))  # 美化打印，不显示行索引
print("\n")

# 查询2：不同车型的平均理赔金额是多少？ (GROUP BY, AVG)
query2 = """
SELECT 
    车型类别,
    COUNT(*) AS 保单数量,
    ROUND(AVG(`理赔金额(元)`), 2) AS 平均理赔金额,
    ROUND(SUM(`理赔金额(元)`), 2) AS 总理赔金额
FROM claims
GROUP BY 车型类别
ORDER BY 平均理赔金额 DESC;
"""
print("2. 【不同车型类别的理赔金额分析】")
df2 = pd.read_sql_query(query2, conn)
print(df2.to_string(index=False))
print("\n")

# 查询3：夜间出险的理赔总数是否高于白天？ (CASE WHEN)
# 假设白天为 7:00 - 19:00，夜间为 19:00 - 次日7:00
query3 = """
SELECT 
    CASE 
        WHEN CAST(strftime('%H', 出险时间) AS INTEGER) >= 7 
             AND CAST(strftime('%H', 出险时间) AS INTEGER) < 19 THEN '白天 (7:00-19:00)'
        ELSE '夜间 (19:00-次日7:00)'
    END AS 出险时段,
    COUNT(*) AS 出险次数,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS 时段占比百分比,
    ROUND(AVG(`理赔金额(元)`), 2) AS 该时段平均理赔金额
FROM claims
GROUP BY 出险时段
ORDER BY 出险次数 DESC;
"""
print("3. 【日间与夜间出险情况对比】")
df3 = pd.read_sql_query(query3, conn)
print(df3.to_string(index=False))

print("\n" + "="*50)
print("核心分析完成！")

# 第三步（重要）：将SQL查询语句保存到 .sql 文件
# 这是你展示给面试官看的“过程资产”
sql_to_save = f"""
-- 车险理赔数据探索分析SQL脚本
-- 生成时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

-- 1. 最常见的出险原因
{query1}

-- 2. 不同车型的平均理赔金额
{query2}

-- 3. 日间与夜间出险情况对比
{query3}
"""

with open('D:/experiment/car_insurance_analysis/sql/insurance_data_analysis.sql', 'w', encoding='utf-8') as f:
    f.write(sql_to_save)
print("所有SQL查询语句已保存至 'insurance_data_analysis.sql' 文件。")

# 关闭数据库连接
conn.close()