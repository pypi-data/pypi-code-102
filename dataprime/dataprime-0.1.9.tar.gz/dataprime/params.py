
EXAMPLES = {
    "drill": """
    # 钻取粒度
    drill_granularity_list = [
        {
            "value": "YEAR",
            "label": "年"
        },
        {
            "value": "MONTH",
            "label": "月"
        },
        {
            "value": "DAY",
            "label": "日"
        }
    ]
    
    # 钻取节点
    drill_node_list = [
        {
            "granularity": "",
            "point": "YEAR",
        },
        {
            "granularity": "YEAR",
            "point": "2021",
        },
        {
            "granularity": "MONTH",
            "point": "01",
        }
    ]
    
    # 需要钻取的维度,必须是日期格式
    dimensions = [
        {
            "column": "time",
            "dtype": "datetime",
        }
    ]
    """,

    "filter": """
    filter_list = [
        {
            "column": "score",             # 过滤字段
            "dtype": "int",                # 字段类型
            "filter": {
                "condition": "less_than",  # 过滤条件
                "value": "100",            # 过滤值
                "max": 50,                 # 最大值, 区间判断时用到
                "min": 0                   # 最小值, 区间判断时用到
            }
        }
    ]
    """,

    "generate": """
    generated_metric_list = [
        {
            "dtype": "float",
            "operate": {
                "label": "均值",
                "value": "Avg"          # 生成类型
            },
            "source_col_list": [        # 源数据列
                {
                    "column": "age",
                    "dtype": "int"
                },
                {
                    "column": "score",
                    "dtype": "int"
                }
            ],
            "column": "age-score-均值"  # 生成列名称
        }
    ]
    """,

    "sample": """
    sample = {
        "number": 5,      # 采样数量
        "type": "random"  # 采样方式, 随机:random  等距:equidistant
    }
    """,

    "aggregate": """
    aggregation_list = [
        {
            "column": "age",          # 源数据列
            "dtype": "int",
            "aggregation_option": {
                "label": "均值",
                "value": "mean"       # 聚合方法
            }
        }
    ]
    """,

    "order_by": """
    sort = {
        "condition": "desc",  # 升序:desc  降序:asc
        "column": "time"      # 排序字段
    }
    """,

    "top_n": """
    top_n_param = {
        "column": "score",     # 排序字段
        "condition": "desc",   # 排序方式， 升序:desc  降序:asc
        "limit": 3             # 取出数量
    }
    """
}
