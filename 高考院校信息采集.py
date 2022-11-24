#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author ：Sam
# @Time : 2022/11/24 17:03
# @File : 高考院校信息采集.py
# @Software : PyCharm


import csv
import time

from selenium import webdriver

url = 'https://www.gaokao.cn/choose/school/code'
# 登录信息cookie保存目录
profile_directory = r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
option = webdriver.ChromeOptions()
option.add_argument(profile_directory)
# 无头模式，避免被检测
option.add_argument('--headless')
# 配置options
driver = webdriver.Chrome(options=option)
# csv表头
header_list = ['院校名', '类别', '分数']
# 存储数据list
data_list = []


def main():
    driver.get(url)
    time.sleep(1)
    # 移除页面底端iframe，防止遮挡'下一页'按钮
    driver.execute_script("var data=document.querySelector('.ani_wrap').remove()")
    # 采集第一页数据
    get_info()
    # save to csv
    save_csv()


def get_info():
    # 院校名
    name_list = []
    names = driver.find_elements_by_xpath('//span[@class="am_l set_hoverl"]')
    for it in names:
        name = it.text
        name_list.append(name)
    print(name_list)

    # 类别及分数
    tag_list = []
    score_list = []
    tags = driver.find_elements_by_xpath('//*[@class="bottom-item"]')
    for tag in tags:
        tag_0 = tag.find_elements_by_class_name('tag-item')[0].text
        tag_1 = tag.find_elements_by_class_name('tag-item')[1].text
        tag_2 = tag.find_elements_by_class_name('tag-item')[2].text
        score = tag.find_element_by_class_name('tag-item-active').text
        tag_txt = '{0}|{1}|{2}'.format(tag_0, tag_1, tag_2)
        tag_list.append(tag_txt)
        score_list.append(score)

    print('{0}\n{1}\n-------'.format(tag_list, score_list))
    for x, y, z in zip(name_list, tag_list, score_list):
        data_list.append(
            {'院校名': x, '类别': y, '分数': z}
        )
    # print(data_list)

    # 获取页面数据数量
    data_len = len(tags)
    # print(data_len)
    # 当页面数据<20条时表明没有'下一页'，则结束采集
    if data_len < 20:
        driver.close()
    else:
        page = driver.find_element_by_xpath('//*[contains(text(),"下一页")]')
        # 页面滚动到底部方便driver找到'下一页'按钮
        driver.execute_script("arguments[0].scrollIntoView(false);", page)
        # 执行点击'下一页'操作
        driver.find_element_by_xpath('//ul/li[contains(text(),"下一页")]').click()
        # 休眠1s等待页面加载数据
        time.sleep(1)
        # 采集下一页数据
        get_info()


def save_csv():
    # 以写方式打开文件。注意添加 newline=""，否则会在两行数据之间都插入一行空白。
    with open("data.csv", mode="w", encoding="utf-8-sig", newline="") as f:
        # 基于打开的文件，创建 csv.DictWriter 实例，将 header 列表作为参数传入。
        writer = csv.DictWriter(f, header_list)
        # 写入 header
        writer.writeheader()
        # 写入数据
        writer.writerows(data_list)


if __name__ == '__main__':
    main()
