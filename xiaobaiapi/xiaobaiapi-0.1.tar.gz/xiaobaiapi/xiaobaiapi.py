#! /usr/bin/env python
__script__ = 'xiaobaiapi.py'
__create__ = '2021/11/14 9:43 下午'
__author__ = 'Tser'
__email__ = '807447312@qq.com'

from requests import request
from jmespath import search
from re import search as re_search
from lxml import etree

def RequestClient(
        method='GET',
        url='',
        assertAt='body',
        assertType='json',
        assertExpression=None,
        assertValue=None,
        extractorAt='body',
        extractorType='json',
        extractorExpression=None,
        extractorVariable=None,
        **kwargs):
    '''

    :param method:
    :param url:
    :param assertAt             位置选择：body(默认)、headers
    :param assertType           断言类型：json(默认)、xml、str
    :param assertExpression     表达式：json、xpath、str
    :param assertValue          预期值：INT/STR
    :param extractorAt          位置选择：body(默认)、headers
    :param extractorType        断言类型：json(默认)、xml、str
    :param extractorExpression  表达式：json、xpath、str
    :param extractorVariable    预期值：None(提取时必填项)
    :param kwargs:
    :return:
    '''
    response = request(method=method, url=url, **kwargs)
    response.variable = {}
    # Assertion
    if assertValue and assertExpression:
        if 'json' == assertType:
            if assertAt == 'headers':
                assert assertValue == search(assertExpression, response.headers)
            else:
                assert assertValue == search(assertExpression, response.json())
        elif 'str' == assertType:
            if assertAt and 'headers':
                assert assertValue == re_search(assertExpression, response.headers.__str__()).groups()[0]
            else:
                assert assertValue == re_search(assertExpression, response.text).groups()[0]
        elif 'xml' == assertType:
            if assertAt and 'headers':
                assert assertValue == etree.HTML(response.headers.__str__()).xpath(assertExpression)
            else:
                assert assertValue == etree.HTML(response.text).xpath(assertExpression)
        else:
            raise Exception('assertType的值不被支持，只支持：json、xml、str')
    # Extractor
    if extractorVariable and extractorExpression:
        if 'json' == assertType:
            if 'extractorAt' in kwargs.keys() and 'headers' == extractorAt:
                value = search(extractorExpression, response.headers)
            else:
                value = search(extractorExpression, response.json())
        elif 'str' == extractorType:
            if 'extractorAt' in kwargs.keys() and 'headers' == extractorAt:
                value = re_search(extractorExpression, response.headers.__str__()).groups()[0]
            else:
                value = re_search(extractorExpression, response.text).groups()[0]
        elif 'xml' == extractorType:
            if 'extractorAt' in kwargs.keys() and 'headers' == extractorAt:
                value = etree.HTML(response.headers.__str__()).xpath(
                    extractorExpression)
            else:
                value = etree.HTML(response.text).xpath(extractorExpression)
        else:
            raise ('assertType的值不被支持，只支持：json、xml、str')
        response.variable[extractorVariable] = value
    return response