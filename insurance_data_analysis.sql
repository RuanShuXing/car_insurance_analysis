
-- 车险理赔数据探索分析SQL脚本
-- 生成时间：2026-01-13 17:04:51

-- 1. 最常见的出险原因

SELECT 
    出险原因,
    COUNT(*) AS 出险次数,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS 占比百分比
FROM claims
GROUP BY 出险原因
ORDER BY 出险次数 DESC;


-- 2. 不同车型的平均理赔金额

SELECT 
    车型类别,
    COUNT(*) AS 保单数量,
    ROUND(AVG(`理赔金额(元)`), 2) AS 平均理赔金额,
    ROUND(SUM(`理赔金额(元)`), 2) AS 总理赔金额
FROM claims
GROUP BY 车型类别
ORDER BY 平均理赔金额 DESC;


-- 3. 日间与夜间出险情况对比

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

