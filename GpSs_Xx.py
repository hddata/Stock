import requests
import pandas as pd
from utils import ZQSS


class GpSsQq(ZQSS):
    '''
    股票实时请求
    请求腾讯接口。https://zhuanlan.zhihu.com/p/484082454
    '''
    def __init__(self,zqdm):
        self.zqdm=zqdm


    def qq_txjk(self):
        '''
        请求腾讯接口。
        参数：
            zqdm: string, 证券代码,支持代码组（【证券1，证券2】参数模式）
        返回值：
            zqssxx_df: dataframe, 证券实时信息
        '''
        
        #证券代码_简短
        zqdm_jd=self.zqdm.replace(".", "")
        # print(zqdm_jd)sh000001,sz000415
        url = 'https://qt.gtimg.cn/q='+zqdm_jd
        # print(url)
        response = requests.get(url)
        if response.status_code == 200:
            zqssxx=response.text
            # 将字符串拆解成列表
            zqssxx_lb = zqssxx.strip().split("\n")
            # 创建一个空的DataFrame
            zqssxx_df = pd.DataFrame()
            # 逐行解析列表的元素并添加到DataFrame
            for zqssxx_ys in zqssxx_lb:
                #拆分成键值对
                jian, zhi = zqssxx_ys.split("=")
                #键值调整
                jian_tz = jian[2:][:2] + "." + jian[2:][2:]
                zhi_tz = zhi.rstrip(";").strip('"').split("~")
                zqssxx_df[jian_tz] = zhi_tz

            # print(f"Response content:\n{response.text}")
        else:
            raise(f"Error: Status code {response.status_code}")
        # print(zqssxx_df)

        return zqssxx_df


class GpSsXx(ZQSS):
    '''
    股票实时信息。
    参数：
        zqdm: string, 证券代码
    返回值：
        
    '''
    def __init__(self,zqdm):
        self.zqdm=zqdm
        self.zqssxx_df=GpSsQq(zqdm).qq_txjk()
    
    def hq_gpzss_dfzd(self):
        '''
        获取股票組实时跌幅最大
        参数：

        返回值：
            gpss_dfzd: string, 股票信息_跌幅最大
        '''
        #股票组实时信息_涨跌幅_df
        gpzssxx_zdh_df = self.zqssxx_df.iloc[32].astype(float)
        gpss_dfzd = gpzssxx_zdh_df.idxmin()

        return gpss_dfzd

    
    def hq_gpzss_jg(self):
        '''
        获取股票組实时价格
        参数：

        返回值：
            gpss_dfzd: string, 股票信息_跌幅最大
        '''
        #股票组实时信息_价格_df
        gpzssxx_jg_df = self.zqssxx_df.iloc[3,30].astype(float)
        gpzssxx_jg_df

        return gpzssxx_jg_df



if __name__ == '__main__':
    '''
    '''
    GpSsXx('sz.003008,sh.000001').hq_gpzss_dfzd()
    GpSsXx('sz.003008,sh.000001').hq_gpzss_jg()


