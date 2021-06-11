# PU_eventkill
口袋校园活动抢报工具

更新日期：2021年6月11日
使用方法：
1.用ios登录PU
2.进行一次关键词搜索并抓包
3.进行一次活动报名并抓包
3.根据URL找的相应的包名，替换掉cookie和content-type以及body部分
4.需要微信推送的话，修改pushplus_submit里的token部分

已经配置好dockerfile，需要放到服务器上的话自己打包即可
docker build -t pu .
