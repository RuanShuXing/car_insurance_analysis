import pandas as pd
import sqlite3

# 1. 读取之前生成的CSV数据
df = pd.read_csv('D:/experiment/car_insurance_analysis/data/car_insurance_claims.csv', encoding='utf-8-sig')
print("数据读取成功，共有{}条记录。".format(len(df)))

# 2. 创建并连接到SQLite数据库
# 创建数据库文件insurance.db
conn = sqlite3.connect('D:/experiment/car_insurance_analysis/insurance.db')

# 3. 将DataFrame数据写入数据库，并命名为 `claims` 表
# `if_exists='replace'` 表示如果表已存在，则替换它
df.to_sql('claims', conn, if_exists='replace', index=False)
print("数据已成功导入到 `insurance.db` 数据库的 `claims` 表中。")

# 4. 验证导入：查询前5行数据
query = "SELECT * FROM claims LIMIT 5;"
preview = pd.read_sql_query(query, conn)
print("\n表内容预览：")
print(preview)

# 5. 不要忘记关闭连接
conn.close()