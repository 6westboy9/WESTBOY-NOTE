

启动类：OAPServerStartUp




![[Pasted image 20231221095418.png|575]]

* AnalysisListener接口：
* FirstAnalysisListener接口：只定义了parseFirst解析方法，这里为什么会有这个接口呢？难道Entry不是First吗？
* EntryAnalysisListener接口：只定义了parseEntry解析方法
* LocalAnalysisListener接口：只定义了parseLocal解析方法
* ExitAnalysisListener接口：只定义了parseExit解析方法
* SegmentListener接口：只定义了parseSegment解析方法
* SegmentAnalysisListener实现类（<font color="#f79646">当前核心关注点</font>）：
* MultiScopesAnalysisListener实现类：
* NetworkAddressAliasMappingListener实现类：


