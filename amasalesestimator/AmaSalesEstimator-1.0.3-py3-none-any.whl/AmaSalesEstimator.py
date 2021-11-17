import pandas as pd
import numpy as np
import os

#Raise
class ParaError(Exception):
    pass
class CateError(Exception):
    pass

#Init
class AmaSalesEstimator(object):
    """ 亚马逊预计销量计算器
    version == 1.0.3
    
    根据亚马逊大部分的一级类目BSR来计算产品当前的预计日销量或月销量。

    Arrtibutes:
        df_temp_para: 最近一次导出参数的临时保存表，默认为None，用于缓存参数加速销量的计算。
        sales: 计算的预计日销量。
    
    Usage:
        AmaSalesEstimator(<paradata_path>, 'us', 'Home & Kitchen',95623).sales
            地区为us，一级类目为Home & Kitchen，BSR为95623的预计日销量。
        AmaSalesEstimator(<paradata_path>, 'us', 'Home & Kitchen', 221563, True).sales
            地区为us，一级类目为Home & Kitchen，BSR为221563的预计月销量。
        AmaSalesEstimator(<paradata_path>, 'us', 'Home & Kitchen', 5120, daily_float=True).sales
            输出为包含两位小数的预计日销量，如果月销量开关打开的时候这个功能无效。
    """
    df_temp_para = None
    sales = None

    def __init__(self, paradata_path, cy, cate, bsr, monthly=False, daily_float=False):
        """ 寻找并提取对应的参数表，计算与BSR相应的预计日销量

        Args:
            paradata_path: 参数文件的地址，字符串。
            cy: 国家地区，字符串，用两位英文字母来表示。
            cate: 一级类目名称，字符串，必须严格按照亚马逊上显示的一级类目来填写。
            bsr: 一级类目的BSR值，整数。
            monthly: 按月统计，布尔值，因为日销量原始数据的计算是浮点数，建议通过打开该开关来得到相对更准确的月销量。
            daily_float: 输出带两位小数的预计日销量，布尔值。

        Raise:
            ParaError: 当文件夹内没有参数表sales_est_para.xlsx时报错。
            CateError: 当所查询的类目没有在参数表内有记录时报错。
        """
        #验证输入的bsr值是否在200以内
        cy = cy.lower()
        cate = cate.strip()
        bsr = int(bsr)
        #导入计算用参数表
        if os.path.isfile(paradata_path):
            df_para = pd.read_excel(paradata_path)
        else:
            raise ParaError('没有找到计算参数表sales_est_para.xlsx')
        #查看是否存在临时参数表
        if self.df_temp_para == None:
            df_temp_para = df_para[(df_para['cy'] == cy) & (df_para['cate'] == cate)]
            if df_temp_para['cy'].count() == 0:
                raise CateError('没有在参数表内找到对应类目的参数，请检查类目名称或更新参数表')
            else:
                pass
            self.df_temp_para = df_temp_para
        else:
            #如果存在临时参数表，则查看是否和本次导入的一级类目一致
            if df_temp_para['cy'].iloc[0] == cy:
                pass
            else:
                df_temp_para = df_para[(df_para['cy'] == cy) & (df_para['cate'] == cate)]
                if df_temp_para['cy'].count() == 0:
                    raise CateError('没有在参数表内找到对应类目的参数，请检查类目名称或更新参数表')
                else:
                    pass
                self.df_temp_para = df_temp_para
        list_para = df_temp_para[['a','b','c','d']].iloc[0].tolist()
        #计算公式
        def func(x,a,b,c,d):
            fx = a * x ** 3 + b * x ** 2 + c * x + d
            return fx
        #将输入的bsr转换为x
        x = np.log2(bsr)
        #计算
        fx = func(x, list_para[0], list_para[1], list_para[2], list_para[3])
        y = 2 ** fx   #转换后的预计日销量初步结果

        #如果原数据存在销量0值点，则在0值点后的数据均为0，避免过拟合导致销量上升
        if bsr >= df_temp_para['even'].iloc[0]:
            y = 0
        else:
            pass

        #如果计算的预计月销量0.8，则修改为0
        #因为计算结果落在(0.5,1]的BSR区间太广
        if y < 0.8:
            y = 0
        else:
            pass

        #月销量开关
        if monthly == True:
            y = int(round(y * 30, 0))
        else:
            if daily_float == True:
                y = round(y, 2)
            else:
                y = int(round(y, 0))
        
        self.sales = y    #导出数据