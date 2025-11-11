# 1.编译阶段

官方文档：[mc](https://arthas.aliyun.com/doc/mc.html)

mc为Memory Compiler即内存编译器的缩写，作用就是编译源码文件到Class文件。

<font color="#f79646">1.替换前</font>

```
[arthas@22316]$ jad com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService processPatInhosRecordExt

ClassLoader:
+-sun.misc.Launcher$AppClassLoader@18b4aac2
  +-sun.misc.Launcher$ExtClassLoader@2d8f65a4

Location:
/D:/Projects/Idea/P2/mnis/windranger-mnis/target/classes/

        private void processPatInhosRecordExt(String wardCode, List<String> allowedLevels, Date currentTime, String patrolNurseCode, List<MnisNursePatrolExt> patrolRecords, Map<String, MnisNursePatrolExt> lastPatrolRecordMap, PatInhosRecordExt patInhosRecordExt) {
/*374*/     String inhosCode = patInhosRecordExt.getInhosCode();
            MnisNursePatrolExt nursePatrolNew = new MnisNursePatrolExt();
/*376*/     nursePatrolNew.setWardCode(wardCode);
/*377*/     nursePatrolNew.setInhosCode(inhosCode);
/*378*/     nursePatrolNew.setBedCode(patInhosRecordExt.getBedCode());
/*379*/     nursePatrolNew.setGender(patInhosRecordExt.getGender());
/*380*/     nursePatrolNew.setPatName(patInhosRecordExt.getPatName());
/*381*/     String nurseLevel = patInhosRecordExt.getNurseLevel();
/*383*/     if (StringUtils.isNotEmpty((String)nurseLevel)) {
/*384*/         nursePatrolNew.setNurseLevel(Integer.valueOf(Integer.parseInt(nurseLevel)));
            }
/*386*/     if (allowedLevels.contains(nurseLevel)) {
/*388*/         nursePatrolNew.setExecuteType(Integer.valueOf(1));
/*389*/         nursePatrolNew.setPatrolTime(currentTime);
/*390*/         nursePatrolNew.setPatrolNurse(patrolNurseCode);
/*392*/         nursePatrolNew.setPatrolEvent("1");
/*394*/         nursePatrolNew.setPatrolEventName(this.sysUtils.getSysDicValue("patPatrolEvent", nursePatrolNew.getPatrolEvent()));
/*396*/         if (StringUtils.isEmpty((String)nursePatrolNew.getPatrolContent())) {
/*397*/             nursePatrolNew.setPatrolContent(nursePatrolNew.getPatrolEventName());
                }
/*399*/         MnisNursePatrol addedRecord = (MnisNursePatrol)this.addResource((ValuedBean)nursePatrolNew);
/*400*/         nursePatrolNew.setSeqId(addedRecord.getSeqId());
/*403*/     } else if (lastPatrolRecordMap.containsKey(inhosCode)) {
/*404*/         MnisNursePatrolExt patrolExt = lastPatrolRecordMap.get(inhosCode);
/*405*/         nursePatrolNew.setPatrolTime(patrolExt.getPatrolTime());
/*406*/         nursePatrolNew.setPatrolEventName(this.sysUtils.getSysDicValue("patPatrolEvent", patrolExt.getPatrolEvent()));
/*408*/         if (StringUtils.isEmpty((String)nursePatrolNew.getPatrolContent())) {
/*409*/             nursePatrolNew.setPatrolContent(nursePatrolNew.getPatrolEventName());
                }
            }
/*413*/     patrolRecords.add(nursePatrolNew);
        }

Affect(row-cnt:2) cost in 938 ms.
```

<font color="#f79646">2.反编译得到源码</font>

```sh
# windows
jad  --source-only com.==lachesis.windranger.mnis.service.impl.MnisNursePatrolService  > D:/com/lachesis/windranger/mnis/service/impl/MnisNursePatrolService.java
# linux
jad  --source-only com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService  > /usr/local/springboot/springboot5_mnis/WRMSMnis/com/lachesis/windranger/mnis/service/impl/MnisNursePatrolService.java
```

<font color="#f79646">3.修改源码中的问题</font>

```
sc -d com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService | grep classLoaderHash
18b4aac2
```

<font color="#f79646">4.编译源码</font>

```
mc -c 238e0d81 /usr/local/springboot/springboot5_mnis/WRMSMnis/com/lachesis/windranger/mnis/service/impl/MnisNursePatrolService.java -d /usr/local/springboot/springboot5_mnis/WRMSMnis
```

报错了~

```ad-important
mc命令可能失败，如果编译失败可以在本地编译好Class文件，再上传至服务器。后续执行流程参考retransform~
```

# 2.加载阶段

官方文档：[retransform](https://arthas.aliyun.com/doc/retransform.html)

将编译后的class文件放置到指定目录，然后使用retransform命令进行加载即可。

```sh
# 1.查看加载前源码
jad com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService processPatInhosRecordExt

# 2.加载指定class文件
retransform /usr/local/springboot/springboot5_mnis/WRMSMnis/MnisNursePatrolService.class

# 3.验证是否生效
jad com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService processPatInhosRecordExt
```

```ad-important
1. 在stop命令后，再次重进后，使用jad命令查看，发现是替换前的代码~
	- 关于这一点在Arthas官网stop命令中已经声明：<font color="#f79646">关闭Arthas服务器之前，会重置掉所有做过的增强类。但是用redefine重加载的类内容不会被重置~</font>
	- 但是redefine官方已经不推荐使用了~
1. 每加载一个Class文件，则会记录一个retransform entry，多次执行则会有多个条retransform entry~
```

```sh
[arthas@29067]$ retransform -l
Id              ClassName       TransformCount  LoaderHash      LoaderClassName 
[arthas@29067]$ retransform /usr/local/springboot/springboot5_mnis/WRMSMnis/MnisNursePatrolService.class # 第1次则会记录一个retransform
retransform success, size: 1, classes:
com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService
[arthas@29067]$ retransform -l
Id              ClassName       TransformCount  LoaderHash      LoaderClassName 
1               com.lachesis.wi 1               null            null            
                ndranger.mnis.s                                                 
                ervice.impl.Mni                                                 
                sNursePatrolSer                                                 
                vice                                                            
[arthas@29067]$ retransform /usr/local/springboot/springboot5_mnis/WRMSMnis/MnisNursePatrolService.class # 第2次则会记录一个retransform
retransform success, size: 1, classes:
com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService
[arthas@29067]$ retransform -l
Id              ClassName       TransformCount  LoaderHash      LoaderClassName 
1               com.lachesis.wi 1               null            null            
                ndranger.mnis.s                                                 
                ervice.impl.Mni                                                 
                sNursePatrolSer                                                 
                vice                                                            
2               com.lachesis.wi 1               null            null            
                ndranger.mnis.s                                                 
                ervice.impl.Mni                                                 
                sNursePatrolSer                                                 
                vice 
```

TransformCount统计在ClassFileTransformer#transform函数里阐述返回entry对应的Class文件的次数，<font color="#f79646">但并不表明一定成功</font>。

```sh
# 删除指定id的retransform entry
retransform -d 1
# 删除所有retransform entry
retransform --deleteAll

# 显示触发retransform，注意对于同一个类，当存在多个retransform entry时，显示触发，则最后添加的entry生效（即最大id的entry生效）
retransform --classPattern com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService
retransform success, size: 2, classes:
com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService
com.lachesis.windranger.mnis.service.impl.MnisNursePatrolService$$EnhancerBySpringCGLIB$$4fb920ca
```

* @ 显示触发的作用是？用途？TODO
