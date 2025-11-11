# 1.忽略规则配置不生效问题

```shell
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```
# 2.在Window下同时配置GitLab和GitHub

[在Windows下同时配置GitLab和GitHub](https://blog.csdn.net/weixin_43207025/article/details/118862575)

按照上述文档中的操作，先生成密钥文件，并添加之服务端。

```sh
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2024/3/23     11:22            161 config
-a----         2024/3/23     10:51           2602 github_id_rsa
-a----         2024/3/23     10:51            571 github_id_rsa.pub
-a----         2024/3/23     10:35           2455 id_rsa
-a----         2024/3/23     10:35            575 id_rsa.pub
```

需要新增`config`配置文件，内容如下：

```
Host github
  user git
  hostname github.com
  identityfile ~/.ssh/github_id_rsa
Host gitlab
  user git
  hostname 10.2.3.111
  identityfile ~/.ssh/id_rsa
```

测试命令：

```
ssh -T git@github
ssh -T git@gitlab
```

# 3.远程分支回滚

[一文了解git分支回滚操作全流程](https://blog.csdn.net/Albert_J/article/details/135759175)


# 4.怎么查看当前的git分支是基于哪个分支创建的？


```bash
$ git reflog --date=local | grep bug_foundation_hcy_33759
09e7fae0 HEAD@{Fri Feb 28 13:41:30 2025}: checkout: moving from master to bug_foundation_hcy_33759
```