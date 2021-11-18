# need append jmeter to path

import os
import time
import json
from .sh_and_os_ext import exec_cmd

def _get_jmx_file(dir):
    jmx_files = []
    for root, dirs, files in os.walk(dir):
        for x in files:
            if '.jmx' in x:
                jmx_files.append(x)
    return jmx_files

def _get_datetime():
    '''
    获取当前日期时间，格式'20150708085159'
    '''
    return time.strftime(r'%m%d%H%M%S', time.localtime(time.time()))

def combine_cli_exec(dir, threads,loops, jmx_files=None, per_testplan_sleep=5*60):
    csvlog_dir = os.path.join(dir,'csvlog')
    report_dir = os.path.join(dir, 'web-report')
    if not os.path.exists(csvlog_dir):
        os.makedirs(csvlog_dir)
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    if not jmx_files:
        jmx_files = _get_jmx_file(os.path.join(dir, 'jmx'))

    for jmx in jmx_files:
        now = _get_datetime()
        tmp = f"{jmx}t{threads}Xl{loops}at{now}"
        jmx_file = os.path.join(dir,'jmx', jmx)
        print(f'jmx_file={jmx_file}')
        csv_file = os.path.join(csvlog_dir,f'{tmp}.csv')
        web_report = os.path.join(report_dir, tmp)
        if not os.path.exists(web_report):
            os.makedirs(web_report)
        cmd = f"jmeter -Jthreads={threads} -Jloops={loops} -n -t {jmx_file} -l {csv_file} -e -o {web_report}"
        print(cmd)
        exec_cmd(cmd)
        time.sleep(per_testplan_sleep)

def gen_summary_report(dir):
    jmx_dir = os.path.join(dir,'jmx')
    csv_dir = os.path.join(dir,'csvlog')
    report_dir = os.path.join(dir, 'web-report')
    jmx_csv_report = []
    for root, dirs, files in os.walk(jmx_dir):
        for name in files:
            if '.jmx' in name:
                tmp_csv_list = []
                tmp_report_list = set()
                for csv_root, csv_dirs, csv_files in os.walk(csv_dir):
                    for csv in csv_files:
                        if name in csv:
                            tmp_csv_list.append(csv)
                            for report_root, report_dirs, report_files in os.walk(report_dir):
                                for report in report_dirs:
                                    if name in report:
                                        tmp_report_list.add(report)
                tmp = {'jmx_file': name, 'csv_files': tmp_csv_list,
                       'report_dirs': list(tmp_report_list)}
                jmx_csv_report.append(tmp)

    print(json.dumps(jmx_csv_report))

    title = ['执行时间', '场景名', 'jmx文件', 'csvLog', '报告详情']

    th_str = '<tr>'
    for x in title:
        th_str = th_str + '<th>' + x + '</th>'
    else:
        th_str = th_str + '</tr>'

    td_str = ''
    for rows in jmx_csv_report:
        td_str = td_str + '<tr>'
        run_time = '无'
        sci_name = '无'
        jmx_name = rows['jmx_file']
        td_jmx = f'<a href="file:///{jmx_dir}/{jmx_name}" target="_blank">{jmx_name}</a>'
        if not rows['csv_files']:
            td_str = td_str + f'<td>{run_time}</td>' + f'<td>{sci_name}</td>' + \
                f'<td>{td_jmx}</td><td>无</td><td>无</td></tr>'
        else:
            for i in rows['csv_files']:
                run_time = i.split('at')[-1].split('.csv')[0]
                sci_name = i.split('jmx')[-1].split('at')[0]
                jmx_name = rows['jmx_file']
                td_jmx = f'<a href="{jmx_dir}/{jmx_name}" target="_blank">{jmx_name}</a>'
                td_csv = f'<a href="{csv_dir}/{i}" target="_blank">{i}</a>'
                td_report = "无"
                may_be_report_name = i[:-4]
                if may_be_report_name in rows['report_dirs']:
                    td_report = f'<a href="{report_dir}/{may_be_report_name}/index.html" target="_blank">查看</a>'
                td_str = td_str + f'<td>{run_time}</td>' + f'<td>{sci_name}</td>' + \
                    f'<td>{td_jmx}</td>' + f'<td>{td_csv}</td>' + \
                    f'<td>{td_report}</td></tr><tr>'
            td_str = td_str[:-4]

    table_str = f'<table border="1">{th_str}{td_str}</table>'
    table_style = '''
    <style type="text/css">
                table {
                    font-family: verdana,arial,sans-serif;
                    font-size:15px;
                    color:#333333;
                    border-width: 1px;
                    border-color: #666666;
                    border-collapse: collapse;
                }
                table th {
                    border-width: 1px;
                    padding: 8px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: #dedede;
                }
                table td {
                    border-width: 1px;
                    padding: 8px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: #ffffff;
                }
            </style>
    '''
    html_str = f'<!DOCTYPE html><html lang="en"><head>{table_style}<head><body><center>{table_str}</center></body></html>'
    with open('SummaryReport.htm', 'w', encoding='utf-8') as file:
        file.writelines(html_str)



# combine_cli_cmd('./jmx',2,2,'../csvlog','../web-report')


if __name__ == '__main__':
    current_path = '.'

    [combine_cli_exec(current_path, x, 10, per_testplan_sleep=3) for x in range(1,10)]

