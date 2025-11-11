# 主文件配置

>nginx.conf

整个配置文件是以<font color="#f79646">区块</font>的形式组织的。一般，<font color="#f79646">每个区块以一对大括号{}来表示开始与结束</font>~

```json
// 主配置，即全局配置段，对http，mail都有效
...

// 配置nginx服务器的事件模块相关参数
events {
 ...
}

// http/https协议相关配置段
http {
 ...
} 

// 默认配置文件不包括下面两个模块

// mail协议相关配置段
mail {
 ...
}    
// stream服务器相关配置段
stream {
 ...
}
```

## 全局配置



## events


## http



## 日志变量

```bash
$remote_addr             // 表示客户端地址
$remote_user             // Http客户端请求Nginx认证用户名
$time_local              // Nginx的时间
$request                 // Request请求行, GET等方法、Http协议版本
$status                  // Respoence返回状态码
$body_bytes_sent         // 从服务端响应给客户端Body信息大小
$http_referer            // Http上一级页面, 防盗链、用户行为分析
$http_user_agent         // Http头部信息, 客户端访问设备
$http_x_forwarded_for    // Http请求携带的Http信息
```


```conf
http {
    log_format main [$time_local]
                    '###'
                    clientIp=$remote_addr
                    '###'
                    request=$request
                    '###'
                    httpPost=$http_host
                    '###'
                    status=$status
                    '###'
                    upstreamStatus=$upstream_status
                    '###'
                    byteSent=$body_bytes_sent
                    '###'
                    httpReferer=$http_referer
                    '###'
                    userAgent=$http_user_agent
                    '###'
                    upstreamAddr=$upstream_addr
                    '###'
                    requestTime=$request_time
                    '###'
                    upstreamResponseTime=$upstream_response_time;
}
```


```
[24/May/2024:14:53:28 +0800]###clientIp=10.2.15.5###request=GET /api/sys/sysConfigFileExt/value?key=departScheduleApproval HTTP/1.1###httpPost=10.2.6.179:86###status=200###upstreamStatus=200###byteSent=73###httpReferer=http://10.2.6.179:86/meepo_v2/###userAgent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36###upstreamAddr=10.2.6.179:10480###requestTime=0.003###upstreamResponseTime=0.003

// 方便查看转换了下

[24/May/2024:14:53:28 +0800]
###clientIp=10.2.15.5
###request=GET /api/sys/sysConfigFileExt/value?key=departScheduleApproval HTTP/1.1
###httpPost=10.2.6.179:86
###status=200
###upstreamStatus=200
###byteSent=73
###httpReferer=http://10.2.6.179:86/meepo_v2/
###userAgent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36
###upstreamAddr=10.2.6.179:10480
###requestTime=0.003
###upstreamResponseTime=0.003
```

# 子文件配置

>子文件配置一般在主文件的http配置部分

```
http {
	include conf.d/*.conf;
}
```


# 辅助工具


## 在线格式化

https://tooltt.com/nginx-format
