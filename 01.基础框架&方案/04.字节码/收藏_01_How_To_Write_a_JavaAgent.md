# 概述

[B站视频链接](https://www.bilibili.com/video/BV1eh41167Lx/?spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=401e9151ff5196d99069159680a48dbc)


![[Pasted image 20231025220500.png|500]]

性能方面：ASM > Byte Buddy > Javassit

# 可能遇到问题

## 1.依赖冲突

![[Pasted image 20231025221148.png|400]]

解决方案：

![[Pasted image 20231025221319.png|600]]

方案一

![[Pasted image 20231025221401.png|775]]

方案二

![[Pasted image 20231025221434.png|775]]


![[Pasted image 20231025221650.png|775]]


![[Pasted image 20231025221832.png|775]]

## 2.Class Not Found

![[Pasted image 20231025221942.png|775]]


![[Pasted image 20231025221958.png|775]]


![[Pasted image 20231025222115.png|775]]


![[Pasted image 20231025222207.png|775]]


![[Pasted image 20231025222307.png|775]]


![[Pasted image 20231025222519.png|775]]

## 3.想要的信息不能一次拦截获取


![[Pasted image 20231025222507.png|775]]


![[Pasted image 20231025222748.png|775]]

SkyWalking和Pinpoint均基于此方案实现。

![[Pasted image 20231025222735.png|775]]


![[Pasted image 20231025223004.png|775]]


![[Pasted image 20231025223131.png|775]]

## 4.异步方法


![[Pasted image 20231025223155.png|775]]


![[Pasted image 20231025223203.png|775]]


![[Pasted image 20231025223243.png|775]]


![[Pasted image 20231025223432.png|775]]


# 开发踩坑


![[Pasted image 20231025223625.png|775]]


![[Pasted image 20231025224006.png|775]]


# 应用


## APM

![[Pasted image 20231025224140.png|775]]


![[Pasted image 20231025224349.png|775]]


![[Pasted image 20231025224433.png|775]]

# 资料推荐

![[Pasted image 20231025224515.png|775]]
