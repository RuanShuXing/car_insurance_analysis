
## 技术栈

- **数据处理与分析**: `Python` (pandas, NumPy, Faker), `SQL` (SQLite)
- **数据可视化**: `Matplotlib`, `Excel` (数据透视表、透视图、切片器)
- **版本控制**: `Git`, `GitHub`
- **环境**: Jupyter Notebook / 任何Python IDE

## 核心分析步骤与业务发现

### 1. 数据模拟与生成
- **脚本**: `scripts/generate_data.py`
- **描述**: 使用 `Faker` 库生成包含 **1000+** 条记录的模拟车险理赔数据集，并加入了一些倾向（如“年轻驾驶员碰撞概率更高”），使分析更贴近现实。

### 2. 数据探索与SQL分析
- **脚本**: `scripts/import_to_sqlite.py`, `scripts/run_sql_analysis.py`
- **产出**: `sql/insurance_data_analysis.sql`
- **核心业务查询**：
  - **出险原因排名**：发现“碰撞”是最主要的出险原因，占比约23%。
  - **车型风险分析**：“豪华型”车辆的平均理赔金额显著高于“经济型”和“SUV”。
  - **位置风险对比**：渝中区的平均理赔金额较其他地区低0.5%。

### 3. 深入分析与可视化
- **脚本**: `scripts/advanced_analysis.py`
- **产出**: `output/` 目录下的所有图表和摘要。
- **关键发现** ：
![img.png](https://github.com/RuanShuXing/car_insurance_analysis/blob/591e6c344877b2902e479fd100d940c6ef3515f5/img.png)中年驾驶员的平均理赔金额最高，是风险管理的重点人群。
![img_1.png](https://github.com/RuanShuXing/car_insurance_analysis/blob/591e6c344877b2902e479fd100d940c6ef3515f5/img_1.png)月度理赔趋势显示，年末理赔次数迅速降低，但平均理赔金额呈上升趋势，可能坐大型交通工具与回家过年相关。
![img_2.png](https://github.com/RuanShuXing/car_insurance_analysis/blob/591e6c344877b2902e479fd100d940c6ef3515f5/img_2.png)热力图清晰揭示，“豪华型”车辆的“碰撞”事故理赔成本最高。

### 4. 交互式业务仪表盘
- **脚本**: `scripts/prepare_dashboard_data.py`
- **最终成品**:![img_3.png](https://github.com/RuanShuXing/car_insurance_analysis/blob/591e6c344877b2902e479fd100d940c6ef3515f5/img_3.png)![img_4.png](https://github.com/RuanShuXing/car_insurance_analysis/blob/591e6c344877b2902e479fd100d940c6ef3515f5/img_4.png)
- **功能**：集成数据透视表、透视图及多个切片器（车型、地区、年份），业务人员可**动态交互**，快速定位特定风险场景。

## 如何运行

1.  **克隆项目**:
    ```bash
    git clone https://github.com/RuanShuXing/car_insurance_analysis.git
    cd car_insurance_analysis
    ```

2.  **安装依赖**:
    ```bash
    pip install pandas numpy faker matplotlib openpyxl
    ```

3.  **按顺序执行脚本** (在项目根目录下):
    ```bash
    python scripts/generate_data.py        # 生成数据
    python scripts/import_to_sqlite.py     # 导入数据库
    python scripts/run_sql_analysis.py     # SQL分析
    python scripts/advanced_analysis.py    # 高级分析与出图
    python scripts/prepare_dashboard_data.py # 准备仪表盘数据
    ```
    最后，打开生成的 `data/dashboard_data_source.xlsx` 文件，手动创建Excel交互式仪表盘。

## 成果展示

| 分析图表 | Excel交互仪表盘 |
| :--- | :--- |
| ![年龄段分析](https://github.com/RuanShuXing/car_insurance_analysis/blob/591e6c344877b2902e479fd100d940c6ef3515f5/1_年龄段_平均理赔金额与占比.png) | |
| *中年驾驶员的平均理赔金额最高* | *支持多维度动态筛选的看板* |

## 项目总结与收获

通过此项目，我系统性地实践了数据分析的全流程：
- **技术层面**：熟练运用 `Python` 进行数据生成、清洗、分析与可视化；掌握使用 `SQL` 进行业务查询；精通利用 `Excel` 高级功能制作商业报告。
- **业务层面**：培养了数据敏感度，学会了从保险业务（风险、赔付）的角度提出分析问题并解读结果。
- **工程层面**：形成了规范的项目结构、代码归档和版本控制习惯。

## 联系我

如果您对该项目有任何疑问或合作意向，欢迎通过以下方式联系：

- **姓名**:陈宣佐
- **邮箱**:2031762463@qq.com
- **GitHub**: https://github.com/RuanShuXing

- **求职意向**: 寻求数据分析/数据支持相关的实习机会。


