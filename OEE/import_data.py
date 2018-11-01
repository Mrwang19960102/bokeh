# 使用Pandas读取OEE_data.xlsx文件，做简单数据清洗，获取各个制造产地制造过程中每周的OOE数据。
import pandas as pd
import numpy as np
def im_data():
    excel_path = 'OEE_data.xlsx'
    df = pd.read_excel(excel_path)
    import_data = df[1:18].drop(['2018年各地光缆厂各工序周OEE达成', 'Unnamed: 1'], axis=1)
    import_data.set_index(['Unnamed: 2'], inplace=False)
    return import_data
	