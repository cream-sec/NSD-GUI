# NSD-GUI

NSD-GUI, The auxiliary tool for network security devices has now completed support for the Huawei USG6300 FIREWALL-02, with continuous updates planned for the future.

![image-20240923152109931](./img/image-20240923152109931.png)

目前的版本主要应用于封禁IP和恶意域名等，配合华为防火墙USG6300 FIREWALL-02使用，大致功能点如下：

- 登陆和日志显示；
- 防火墙策略查询；
- 地址组和域名组内数量查询；
- 内外网IP映射查询；
- IP拉黑；
- URL拉黑。

上面的拉黑处理需要操作人员清楚防火墙的哪些地址组或者域名组用于封禁作用！

有两项注意事项：
- 在防火墙中添加API用户，该用户的服务类型选择API；
- 开启北向接口，程序中使用的接口是RESTCONF，选择HTTP，启用端口为9000（程序中已经写死了，后续再更新程序吧）。
