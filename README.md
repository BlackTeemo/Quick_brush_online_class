# 河南大学雨课堂网课脚本

```python
河南大学 2020 电子信息科学与技术秋-马克思主义基本原理概论(周三晚10-18 21-22-1)网课代刷.py
```

由GTY查阅资料针对马克思主义基本原理概论开发 开发时间2021年12月19日晚至2021年12月20日上午 

### 截止2021年12月20日上午，修复了Bug如下

​	某一个正常代刷代Course，为第一次观看，之前没有观看记录造成无法获取该视频的观看状态，从而导致脚本崩溃

​	post get请求提交过于频繁导致雨课堂暂时性拉黑ip地址 （如果你可以科学上网可以更换代理继续快速刷网课）

​	

## 使用方法
  0 脚本中用到的模块 如果没有的话 请自行使用 pip命令安装

​	1 首先使用电脑 通过 谷歌浏览器 打开雨课堂官方网址 微信扫码进入你的雨课堂主页

​	2 按F12进入开发者模式 或在页面空白处右键点击检查 将csrftoken 和 sessionid 的值替换为代码中对应的值

​	3 user_id 的值需要自己检查获取 skuid 的值 一个班的值应该一样 也是自己检查获取 将这user_id值替换为代码中对应的值

​	4  运行脚本
