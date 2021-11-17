"""
计算薪水
"""
company = 'mi'
print('salary_real模块导入中。。。')


def salaryYear(salaryMonth):
    """
    根据传入的月薪，计算年薪，一年有12个月
    :param salaryMonth:月薪
    :return: salaryYear
    """
    return salaryMonth*12


def salaryDay(salaryMonth):
    """
    根据传入的月薪，计算日薪，一个月的工作日为22.5天
    :param salaryMonth:月薪
    :return: salaryDay
    """
    return salaryMonth/22.5

if __name__ == '__main__':
    print(salaryYear(3000))
    print(salaryDay(3000))