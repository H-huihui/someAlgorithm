# -*- coding: utf-8 -*-
"""
Created on Tue Aug 01 18:18:58 2017

@author: Mason
"""

import pandas as pd
import os
#==============================================================================
# 此文件用于JDFeed流账户月报制作，可以一键生成月报所需所有数据&格式  
# 月报源表的结构为 [日期 账户 推广计划 推广计划ID	推广单元	推广单元ID /
# 创意名称 创意ID 标题	描述	图片数量	url	展现	点击	消费	点击率 平均点击价格 千次展现消费	网页转化	推广计划 推广单元 创意名称/
# 创意类型 活动名称 投放资源 投放位置	 投放设备	 广告类型	 定向方式	 页面类型	 月份 自然周 星期]
# 该程序的目的为按照一定格式汇总[u'页面类型',u'投放设备',u'活动名称',u'创意类型',u'定向方式']几个维度的数据
# 程序可以生成一个xlsx文件，包含 5 个sheet，分别为上述几个维度名称
# 每一个sheet结构为
# [part1]
# 时间周期  账面消费  曝光    点击  点击率  CPC   CPM
# xxx       xxx       xxx    xxx    xxx   xxx  xxx
# 环比数据   xx       xxx    xxx    xxx   xxx   xxx
# [part2]
# 时间     创意样式   账面消费  曝光 点击  点击率  CPC CPM  [总]消费占比   [总]点击占比
# xxx
# 环比数据
# 在此将part1作为一部分，part2作为一部分
#==============================================================================
class JDFeeds(object):
    
    def __init__(self):
        #读取对应的文件并对文件进行预处理，文件地址默认为程序同文件夹下
        self.keyword = pd.read_excel(u'京东-百度【周报用】源数据.xlsx',sheetname=u'创意报告')
        #最终表“展现”-->“曝光”
        self.keyword = self.keyword.rename(columns = {u'展现':u'曝光'})
        #先求的自然周的展点消汇总，为后面求的各维度占比备用
        self.allCost = self.keyword.groupby([u'自然周'],as_index=False)[u'消费',u'点击',u'曝光'].sum()
        self.allCostSave = self.allCost.copy()#copy()用来完整复制整个变量
        self.allCost = self.allCost.rename(columns={u'消费':u'总消费',u'点击':u'总点击',u'曝光':u'总曝光'})
        #汇总数据格式
        self.allCostSave[u'点击率'] = self.allCostSave[u'点击']/self.allCostSave[u'曝光']
        self.allCostSave[u'CPC'] = self.allCostSave[u'消费']/self.allCostSave[u'点击']
        self.allCostSave[u'CPM'] = self.allCostSave[u'消费']/self.allCostSave[u'曝光']*1000
        # self.allCostSave变量用来作为每个sheet上的数据汇总表
        self.allCostSave = self.addOneRow(self.allCostSave)
        #用来生成结果表最上面部分结构
    
    def addWeidu(self,weidu):
        #增加几个指标数据，并且删除相关数据
        weidu = pd.merge(weidu,self.allCost,on=u'自然周',how='left')
        weidu[u'点击率']=weidu[u'点击']/weidu[u'曝光']
        weidu[u'CPC'] = weidu[u'消费']/weidu[u'点击']
        weidu[u'CPM'] = weidu[u'消费']/weidu[u'曝光']*1000
        weidu[u'消费占比']= weidu[u'消费']/weidu[u'总消费']
        weidu[u'点击占比']= weidu[u'点击']/weidu[u'总点击']
        weidu = weidu.drop([u'总消费',u'总点击',u'总曝光'],axis=1)
        return weidu
    
    #addOneRow 用来为每一个part添加环比数据，输入一个dataframe，返回一个增加环比后的dataframe
    def addOneRow(self,res):
        #每一块数据都添加一行“环比数据”,part2有10列数据，part2有8列
        if res.shape[1] == 10:
            new = pd.Series([u'环比消费',u'环比消费',0,0.0,0.0,0,0,0,0,0],index=res.columns)
            #由于源数据中展现和点击是int格式数据，因此在新增行中，设置为0.0
            startPoint = 2
            #startPoint 用来做开始的节点，part1中只有一个“时间周期”列，part2中有“时间”和“创意样式”两列
        else:
            startPoint = 1
            new = pd.Series([u'环比消费',0,0.0,0.0,0,0,0],index=res.columns)
            
        res = res.reset_index(drop = True)
        #重置索引，为ix和iloc做准备
        res.ix[res.shape[0]] = new
        #将环比列添加到part中
        for x in range(startPoint,res.shape[1]):
            res.iloc[res.shape[0]-1,x] = (res.iloc[res.shape[0]-2,x]-res.iloc[res.shape[0]-3,x])/res.iloc[res.shape[0]-3,x]
            #循环遍历新增行每一个数据，添加环比
        return res
    
    def splitResult(self,res,types):
        resList = []
        resList.append(self.allCostSave)
        typeList = res[types][~res[types].duplicated()].tolist() 
        for typex in typeList:
            resList.append(self.addOneRow(res[res[types] == typex]))
        return resList
        
    def getNum(self,types):
        temp = self.keyword.groupby([u'自然周',types],as_index=False)[u'消费',u'曝光',u'点击'].sum()
        luodiye = self.addWeidu(temp)
        resList = self.splitResult(luodiye,types)
        return resList

if __name__ == '__main__':
    typeList = [u'账户',u'页面类型',u'投放设备',u'品类名称',u'创意类型',u'定向方式']
    jdF = JDFeeds()
    writer = pd.ExcelWriter(u'测试数据结果-0808.xlsx')
    jdF.allCostSave.to_excel(writer,sheet_name=u'消费汇总',index=False)
    for types in typeList:
        print types
        result = jdF.getNum(types)
        startPoint = 0
        for count in range(len(result)):
            result[count].replace('inf',0).fillna(0).to_excel(writer,sheet_name=types,startrow = startPoint,index=False,header=count<2)
            startPoint += result[count].shape[0]+ int(count<2)
    writer.save()
