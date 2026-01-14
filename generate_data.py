import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# 初始化Faker，用于生成中文虚拟数据
fake = Faker('zh_CN')

# 设置随机种子，确保每次运行生成的数据集相同（便于复现）
random.seed(42)
np.random.seed(42)

# 根据实际定义一些基础选项
car_brands_models = {
    '经济型': ['丰田卡罗拉', '大众朗逸', '本田思域', '日产轩逸'],
    'SUV': ['哈弗H6', '吉利博越', '大众途观', '本田CR-V'],
    '豪华型': ['奔驰C级', '宝马3系', '奥迪A4L', '特斯拉Model 3']
}
claim_reasons = ['碰撞', '刮擦', '自然灾害（水淹）', '盗抢', '玻璃破损', '第三者责任']
regions = ['渝中区', '江北区', '南岸区', '九龙坡区', '沙坪坝区']

# 准备一个空列表来存储所有生成的数据行
records = []

# 生成1000条模拟数据
for i in range(1, 1001):
    # 1. 生成保单号 (格式：LB20231124001)
    policy_id = f"LB{datetime.now().strftime('%Y%m%d')}{i:03d}"

    # 2. 生成客户基本信息
    gender = random.choice(['男', '女'])
    # 年龄分布：更偏向18-60岁的驾驶员，并让“年轻”驾驶员（<25）占一定比例
    if random.random() < 0.15:  # 15%的概率为年轻驾驶员
        age = random.randint(18, 25)
    else:
        age = random.randint(26, 60)

    # 3. 生成车辆信息，并且注意豪华车型更贵
    car_type = random.choice(list(car_brands_models.keys()))  # 随机选择车型类别
    car_model = random.choice(car_brands_models[car_type])  # 从类别中选具体车型
    car_age = random.randint(0, 10)  # 车龄0-10年

    # 4. 生成投保地区
    region = random.choice(regions)

    # 5. 生成出险信息
    claim_reason = random.choice(claim_reasons)

    # 模式1：年轻驾驶员更容易出碰撞事故
    if age < 25 and random.random() < 0.6:  # 年轻驾驶员有60%概率分配为“碰撞”
        claim_reason = '碰撞'

    # 模式2：特定地区（如“渝中区”）出险频率会更高
    # 我们通过让该地区有更高概率生成记录来模拟（循环外整体控制）

    # 6. 生成理赔金额
    base_amount = 0
    # 基础金额根据出险原因浮动
    if claim_reason == '碰撞':
        base_amount = np.random.normal(5000, 1500)  # 正态分布，均值5000，标准差1500
    elif claim_reason == '盗抢':
        base_amount = np.random.normal(80000, 20000)
    else:
        base_amount = np.random.normal(2000, 800)

    # 模式3：年轻驾驶员的“碰撞”事故理赔金额更高
    if claim_reason == '碰撞' and age < 25:
        base_amount *= random.uniform(1.2, 1.5)  # 金额上浮20%-50%

    # 模式4：豪华车型的理赔金额更高
    if car_type == '豪华型':
        base_amount *= random.uniform(1.3, 2.0)

    # 金额不为负，保留两位小数
    claim_amount = round(abs(base_amount), 2)

    # 7. 生成出险时间（模拟过去一年内的随机时间）
    days_ago = random.randint(1, 365)
    claim_date = datetime.now() - timedelta(days=days_ago)
    # 将时间格式化为字符串，便于存储
    claim_time = claim_date.strftime('%Y-%m-%d %H:%M:%S')

    # 将生成好的数据组合成一条记录，添加到列表
    records.append([
        policy_id, gender, age, car_type, car_model, car_age,
        region, claim_reason, claim_amount, claim_time
    ])

# 8. 将列表转换为Pandas DataFrame，并指定列名
df = pd.DataFrame(records, columns=[
    '保单号', '客户性别', '客户年龄', '车型类别', '具体车型', '车龄(年)',
    '投保地区', '出险原因', '理赔金额(元)', '出险时间'
])

# 9. 模式2：让“渝中区”的记录多一些，模拟出险频率高的情况
extra_records = []
for _ in range(200):  # 额外生成200条
    # ... [代码逻辑与上面类似，但固定地区为'渝中区'] ...
    pass

# 10. 保存数据到CSV文件
df.to_csv('D:/experiment/car_insurance_analysis/data/car_insurance_claims.csv', index=False, encoding='utf-8-sig')
print(f"模拟数据生成完成！共生成 {len(df)} 条记录。")
print(f"数据已保存至 'D:/experiment/car_insurance_analysis/data/car_insurance_claims.csv'")
print("\n数据预览：")
print(df.head())