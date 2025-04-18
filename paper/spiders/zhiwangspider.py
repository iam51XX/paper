import json     #处理 JSON 字符串
from typing import Iterable     #解码 POST 表单字符串
import urllib.parse     #用 BeautifulSoup 解析 HTML 页面
import bs4      	#读取 Excel / CSV 文件
import scrapy    	#Scrapy 框架核心
import pandas     #发送模拟表单 POST 请求
from scrapy import FormRequest, Request
from paper.items import ZhiwangItem     #自定义数据结构

class ZhiwangspiderSpider(scrapy.Spider):
    name = "zhiwangspider"
    allowed_domains = ["cnki.net"]          #限定爬虫的网站
    start_urls = ["https://cnki.net"]
    cookies = {
        'show_vpn': '1',
        'heartbeat': '1',
        'show_faq': '0',
        'Hm_lvt_2e552fbaf5e9c8ff5d407c2048cc91bb': '1744723856,1744867867,1744942935,1744944787',
        'Hm_lpvt_2e552fbaf5e9c8ff5d407c2048cc91bb': '1744944787',
        'HMACCOUNT': 'FC9D3909A3EBF658',
        'wengine_vpn_ticketwebvpn_shmtu_edu_cn': 'b7b55427970f14ab',
        'refresh': '0'
    }

    school = pandas.read_csv(r'D:/python_project/paper/paper/school.csv')
    beida = pandas.read_excel(r'D:/python_project/paper/paper/北核期刊.xlsx')
    headers = {

        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '1868',  # 可以删掉这个，Scrapy 会自动处理
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://webvpn.shmtu.edu.cn',
        'Referer': 'https://webvpn.shmtu.edu.cn/https/77726476706e69737468656265737421fbf952d2243e635930068cb8/kns8s/AdvSearch?crossids=YSTT4HG0%2CLSTPFY1C%2CJUP3MUPD%2CMPMFIG1A%2CWQ0UVIAA%2CBLZOG7CK%2CPWFIRAGL%2CEMRPGLPA%2CNLBO1Z6R%2CNN3FJMUV',
        'Sec-Ch-Ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'X-Requested-With': 'XMLHttpRequest'
    }


    def start_requests(self):
        for school in self.school.values:
            school = school[0]
            for magazine in self.beida.values:
                magazine = magazine[3]
                zongfenlei=magazine[0][2:]       #去掉前两个编号 只取分类名称
                school = school
                magazine = magazine
                data = 'boolSearch=true&QueryJson={"Platform":"","Resource":"CROSSDB","Classid":"WD0FTY92","Products":"","QNode":{"QGroup":[{"Key":"Subject","Title":"","Logic":0,"Items":[],"ChildItems":[{"Key":"input[data-tipid=gradetxt-3]","Title":"作者单位","Logic":0,"Items":[{"Key":"input[data-tipid=gradetxt-3]","Title":"作者单位","Logic":0,"Field":"AF","Operator":"FUZZY","Value":"学校名称","Value2":""}],"ChildItems":[]},{"Key":"input[data-tipid=gradetxt-4]","Title":"文献来源","Logic":0,"Items":[{"Key":"input[data-tipid=gradetxt-4]","Title":"文献来源","Logic":0,"Field":"LY","Operator":"DEFAULT","Value":"杂志名称","Value2":""}],"ChildItems":[]}]},{"Key":"ControlGroup","Title":"","Logic":0,"Items":[],"ChildItems":[]}]},"ExScope":"0","SearchType":1,"Rlang":"CHINESE","KuaKuCode":"YSTT4HG0,LSTPFY1C,JUP3MUPD,MPMFIG1A,WQ0UVIAA,BLZOG7CK,EMRPGLPA,PWFIRAGL,NLBO1Z6R,NN3FJMUV"}&pageNum=1&pageSize=20&dstyle=listmode&boolSortSearch=false&sentenceSearch=false&productStr=YSTT4HG0,LSTPFY1C,RMJLXHZ3,JQIRZIYA,JUP3MUPD,1UR4K4HZ,BPBAFJ5S,R79MZMCB,MPMFIG1A,WQ0UVIAA,NB3BWEHK,XVLO76FD,HR1YT1Z9,BLZOG7CK,EMRPGLPA,J708GVCE,ML4DRIDX,PWFIRAGL,NLBO1Z6R,NN3FJMUV,&aside=（作者单位：学校名称(模糊)）AND（文献来源：杂志名称(精确)）&searchFrom=资源范围：总库;++时间范围：更新时间：不限;++&CurPage=1'
                #构造一个知网接口接收POST表单
                data = data.replace('学校名称', school).replace('杂志名称', magazine)
                #自动替换关键词
                decoded_form_data = urllib.parse.parse_qs(data)         #把URL格式的表单字符串data转换成Scrapy能用的字典形式
                data = {key: value[0] if value else "" for key, value in decoded_form_data.items()}
                yield FormRequest(url='https://webvpn.shmtu.edu.cn/https/77726476706e69737468656265737421fbf952d2243e635930068cb8/kns8s/brief/grid',cookies=self.cookies,headers=self.headers,callback=self.parse,formdata=data,cb_kwargs={'学校':school,'期刊':magazine,'总分类':zongfenlei})
                #发送post请求，并交给self.parse() 来处理返回的搜索结果

    #对每一个【学校 + 期刊】组合，构造一个 POST 表单，模拟从知网“高级检索”搜索论文数量，并发出请求，交给 parse() 去处理返回结果。

    def parse(self, response,**kwargs):
        response=response.text
        try:
            soup = int(bs4.BeautifulSoup(response, 'html.parser').find('span', class_='pagerTitleCell').find(
                'em').text.strip())
        except:
            soup=-99
        ite=ZhiwangItem()
        school=kwargs['学校']
        magazine=kwargs['期刊']
        zongfenlei=kwargs['总分类']
        print(school,magazine,soup)
        ite['学校']=school
        ite['期刊']=magazine
        ite['数量']=soup
        ite['总分类']=zongfenlei
        ite['属于']='北核'
        yield ite