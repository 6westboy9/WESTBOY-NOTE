## 1.环境与版本

>环境

| IP            |               |
| ------------- | ------------- |
| 192.168.91.11 | master        |
| 192.168.91.12 | node1         |
| 192.168.91.13 | node2         |
| 172.16.0.0/16 | podSubnet     |
| 10.96.0.0/16  | serviceSubnet |
>版本

* kubelet-1.20.9
* kubeadm-1.20.9
* kubectl-1.20.9
* docker-ce-cli-19.03.15
* docker-ce-19.03.15
* containerd.io-1.3.7

## 2.安装Docker

[卸载Docker](https://blog.csdn.net/m0_65992672/article/details/132415703)

```bash
# 1.配置yum源
yum install -y yum-utils
yum-config-manager \
--add-repo \
http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

```bash
# 2.安装K8s时使用的Docker环境
yum install -y docker-ce-19.03.15 docker-ce-cli-19.03.15  containerd.io-1.3.7
```

```bash
# 3.启动
# --now表示既要现在启动，又要开机启动
systemctl enable docker --now
```

```bash
# 4.配置加速
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
    "registry-mirrors": [
        "https://jkbqrc40.mirror.aliyuncs.com",
        "https://dockerproxy.com",
        "https://docker.mirrors.ustc.edu.cn",
        "https://docker.nju.edu.cn"
    ],
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "100m"
    },
    "storage-driver": "overlay2"
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

这个cgroupdriver=systemd和cgroupdriver=cgroupfs区别是？

* 

>这里额外添加了Docker的生产环境核心配置cgroup，其作用是？

* 在Docker的生产环境中，核心配置之一是cgroup（Control Group）。<font color="#f79646">cgroup是Linux内核提供的一种机制</font>，用于限制和管理进程组的资源使用。Docker通过cgroup实现了对容器的资源隔离和控制。
* 主要作用：
	- 资源限制和分配：使用cgroup可以对容器的CPU、内存、磁盘、网络等资源进行限制和分配。这样可以避免容器之间相互干扰，确保每个容器能够按需使用资源。
	- 资源统计和监控：cgroup可以统计和监控容器使用的资源量。这对于性能分析、资源优化以及故障排查非常重要。管理员可以通过监控cgroup的统计信息来了解容器的资源利用情况，并进行相应的优化措施。
	- 资源限制策略：使用cgroup可以定义和配置资源限制策略，例如CPU配额、内存限制等。这样可以确保不同容器之间的资源分配满足业务需求，并避免出现资源竞争和过度使用的情况。
- 总之，cgroup在Docker的生产环境中起着关键作用，通过资源限制、分配和统计，它实现了对容器的资源隔离、控制和监控，从而提供了更高效、安全和可靠的容器化环境。

---
# 3.安装Kubeadm

## 1.准备

* 主机名不能重复
* 内网互信


```bash
# 192.168.91.11
hostnamectl set-hostname k8s-master
# 192.168.91.12
hostnamectl set-hostname k8s-node1
# 192.168.91.13
hostnamectl set-hostname k8s-node2
```

> 所有机器均执行以下操作

```bash
echo "192.168.91.11 k8s-master" >> /etc/hosts
echo "192.168.91.12 k8s-node1" >> /etc/hosts
echo "192.168.91.13 k8s-node2" >> /etc/hosts

# 将SELinux设置为permissive模式（相当于将其禁用）
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

# 关闭swap
swapoff -a  
sed -ri 's/.*swap.*/#&/' /etc/fstab

# 允许iptables检查桥接流量
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

# 以上配置生效
sudo sysctl --system
```

## 2.安装Kubelet_Kubeadm_Kubectl

```bash
# 配置K8s下载地址信息
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
   http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

# 安装需要的组件
sudo yum install -y kubelet-1.20.9 kubeadm-1.20.9 kubectl-1.20.9 --disableexcludes=kubernetes

# 所有机器开机并立即启动Kubelet
sudo systemctl enable --now kubelet

# 查看状态
sudo systemctl status kubelet
```

```
[root@k8s-master ~]# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: activating (auto-restart) (Result: exit-code) since Thu 2024-06-13 11:19:31 CST; 6s ago
     Docs: https://kubernetes.io/docs/
  Process: 10798 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS (code=exited, status=255)
 Main PID: 10798 (code=exited, status=255)

Jun 13 11:19:31 k8s-master kubelet[10798]: /workspace/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:133 +0x98
Jun 13 11:19:31 k8s-master systemd[1]: kubelet.service: main process exited, code=exited, status=255/n/a
Jun 13 11:19:31 k8s-master kubelet[10798]: k8s.io/kubernetes/vendor/k8s.io/apimachinery/pkg/util/wait.Until(...)
Jun 13 11:19:31 k8s-master kubelet[10798]: /workspace/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:90
Jun 13 11:19:31 k8s-master kubelet[10798]: k8s.io/kubernetes/vendor/k8s.io/apimachinery/pkg/util/wait.Forever(0x4a8f738, 0x12a05f200)
Jun 13 11:19:31 k8s-master kubelet[10798]: /workspace/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/k8s.io/apimachinery/pkg/util/wait/wait.go:81 +0x4f
Jun 13 11:19:31 k8s-master kubelet[10798]: created by k8s.io/kubernetes/vendor/k8s.io/component-base/logs.InitLogs
Jun 13 11:19:31 k8s-master kubelet[10798]: /workspace/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/k8s.io/component-base/logs/logs.go:58 +0x8a
Jun 13 11:19:31 k8s-master systemd[1]: Unit kubelet.service entered failed state.
Jun 13 11:19:31 k8s-master systemd[1]: kubelet.service failed.
```

> [!error] 注意
> Kubelet现在每隔几秒就会重启，因为它陷入了一个等待Kubeadm指令的死循环~

# 4.使用Kubeadmin引导集群


## 1.下载各个机器需要的镜像

```shell
sudo tee ./images.sh <<-'EOF'
#!/bin/bash
images=(
kube-apiserver:v1.20.9
kube-proxy:v1.20.9
kube-controller-manager:v1.20.9
kube-scheduler:v1.20.9
coredns:1.7.0
etcd:3.4.13-0
pause:3.2
)
for imageName in ${images[@]} ; do
docker pull registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/$imageName
done
EOF
   
chmod +x ./images.sh && ./images.sh
```

```bash
# 所有节点的镜像均已经准备完成
[root@k8s-master ~]# docker images
REPOSITORY                                                                 TAG        IMAGE ID       CREATED       SIZE
registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/kube-proxy                v1.20.9    8dbf9a6aa186   2 years ago   99.7MB
registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/kube-controller-manager   v1.20.9    eb07fd4ad3b4   2 years ago   116MB
registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/kube-scheduler            v1.20.9    295014c114b3   2 years ago   47.3MB
registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/kube-apiserver            v1.20.9    0d0d57e4f64c   2 years ago   122MB
registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/etcd                      3.4.13-0   0369cf4303ff   3 years ago   253MB
registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/coredns                   1.7.0      bfe3a36ebd25   3 years ago   45.2MB
registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/pause                     3.2        80d28bedfe5d   4 years ago   683kB
```

## 2.初始化Master节点

```shell
# 所有机器添加Master域名映射，以下需要修改为自己的
# cluster-endpoint即集群的入口节点，也就是Master节点
# 所有机器节点都要执行
echo "192.168.91.11 cluster-endpoint" >> /etc/hosts

# Master节点初始化
kubeadm init \
--apiserver-advertise-address=192.168.91.11 \                            # master节点IP
--control-plane-endpoint=cluster-endpoint \                              # 上述配置的域名值
--image-repository registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images \    # 镜像仓库
--kubernetes-version v1.20.9 \                                           # K8s版本
--service-cidr=10.96.0.0/16 \                                            # 注意Service、Pod、Docker自己的IP、机器四者IP地址范围不能重叠
--pod-network-cidr=172.16.0.0/16                                         # 注意Service、Pod、Docker自己的IP、机器四者IP地址范围不能重叠

kubeadm init \
--apiserver-advertise-address=192.168.91.11 \
--control-plane-endpoint=cluster-endpoint \
--image-repository registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images \
--kubernetes-version v1.20.9 \
--service-cidr=10.96.0.0/16 \
--pod-network-cidr=172.16.0.0/16
```

> [!danger] 注意
> Docker自身会占用一个IP地址范围：172.17.0.1/16，通过`ip add`命令查看~

<font color="#f79646">如何重置呢？</font>https://blog.csdn.net/xinshuzhan/article/details/115331683

执行完成，日志如下：

```
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of control-plane nodes by copying certificate authorities
and service account keys on each node and then running the following as root:

  kubeadm join cluster-endpoint:6443 --token fxkwfg.s8fc0ojddl4qgskt \
    --discovery-token-ca-cert-hash sha256:d96f75c294438a07a045e33791d46f89440819d1d013689228b8b0fd95c3a31d \
    --control-plane 

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join cluster-endpoint:6443 --token fxkwfg.s8fc0ojddl4qgskt \
    --discovery-token-ca-cert-hash sha256:d96f75c294438a07a045e33791d46f89440819d1d013689228b8b0fd95c3a31d 
```

## 3.按照提示执行_准备

在<font color="#c0504d">Master节点</font>执行如下命令（上述日志中列举的命令）：

```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```

此时借助`kubectl`工具查看集群中的节点信息：

```bash
[root@k8s-master ~]# kubectl get nodes
NAME         STATUS     ROLES                  AGE     VERSION
k8s-master   NotReady   control-plane,master   4m46s   v1.20.9
```

## 4.按照提示执行_安装网络插件

>K8s支持的网络插件：https://kubernetes.io/docs/concepts/cluster-administration/addons

在<font color="#c0504d">Master节点</font>执行：

### 4.1.calico_一直没成功

```
curl https://docs.projectcalico.org/v3.20/manifests/calico.yaml -O
kubectl apply -f calico.yaml
```

```bash
[root@k8s-master ~]# kubectl get pods -A
NAMESPACE     NAME                                       READY   STATUS                  RESTARTS   AGE
kube-system   calico-kube-controllers-577f77cb5c-j6blv   0/1     Pending                 0          13h
kube-system   calico-node-xflsb                          0/1     Init:ImagePullBackOff   0          95s   <= 问题
kube-system   coredns-5897cd56c4-96lrg                   0/1     Pending                 0          14h
kube-system   coredns-5897cd56c4-ttmqq                   0/1     Pending                 0          14h
kube-system   etcd-k8s-master                            1/1     Running                 2          14h
kube-system   kube-apiserver-k8s-master                  1/1     Running                 1          14h
kube-system   kube-controller-manager-k8s-master         1/1     Running                 1          14h
kube-system   kube-proxy-scvnw                           1/1     Running                 1          14h
kube-system   kube-scheduler-k8s-master                  1/1     Running                 1          14h
```

```bash
# 使用-o参数指定输出格式为wide，这将显示更广泛的信息，包括Pod的IP地址、所在的节点、启动时间等~
[root@k8s-master ~]# kubectl get pods -n kube-system -o wide
NAME                                       READY   STATUS                  RESTARTS   AGE    IP              NODE         NOMINATED NODE   READINESS GATES
calico-kube-controllers-577f77cb5c-j6blv   0/1     Pending                 0          13h    <none>          <none>       <none>           <none>
calico-node-xflsb                          0/1     Init:ImagePullBackOff   0          3m5s   192.168.91.11   k8s-master   <none>           <none>
coredns-5897cd56c4-96lrg                   0/1     Pending                 0          14h    <none>          <none>       <none>           <none>
coredns-5897cd56c4-ttmqq                   0/1     Pending                 0          14h    <none>          <none>       <none>           <none>
etcd-k8s-master                            1/1     Running                 2          14h    192.168.91.11   k8s-master   <none>           <none>
kube-apiserver-k8s-master                  1/1     Running                 1          14h    192.168.91.11   k8s-master   <none>           <none>
kube-controller-manager-k8s-master         1/1     Running                 1          14h    192.168.91.11   k8s-master   <none>           <none>
kube-proxy-scvnw                           1/1     Running                 1          14h    192.168.91.11   k8s-master   <none>           <none>
kube-scheduler-k8s-master                  1/1     Running                 1          14h    192.168.91.11   k8s-master   <none>           <none>
```

```bash
[root@k8s-master ~]# cat calico.yaml | grep image
          image: docker.io/calico/cni:v3.20.6
          image: docker.io/calico/cni:v3.20.6
          image: docker.io/calico/pod2daemon-flexvol:v3.20.6
          image: docker.io/calico/node:v3.20.6
          image: docker.io/calico/kube-controllers:v3.20.6
```

### 4.2.flannel_成功了

下载配置文件：https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

```yaml
# 1.手动导出导入镜像 <<< 注意每个节点都要执行
# image: docker.io/flannel/flannel:v0.25.4
image: flannel/flannel:v0.25.4
# image: docker.io/flannel/flannel-cni-plugin:v1.4.1-flannel1
image: flannel/flannel-cni-plugin:v1.4.1-flannel1

# 2.设置网络 <<< 只需要Master节点
net-conf.json: |
{
  "Network": "172.16.0.0/16", # 替换为自己的Pod网络
  "Backend": {
	"Type": "vxlan"
  }
}
```

```bash
[root@k8s-master ~]# kubectl apply -f kube-flannel.yml
[root@k8s-master ~]# kubectl get pods -A
NAMESPACE      NAME                                 READY   STATUS    RESTARTS   AGE
kube-flannel   kube-flannel-ds-wr4bh                1/1     Running   0          7m38s
kube-system    coredns-5897cd56c4-trstt             1/1     Running   0          8m57s
kube-system    coredns-5897cd56c4-xp29d             1/1     Running   0          8m57s
kube-system    etcd-k8s-master                      1/1     Running   0          9m9s
kube-system    kube-apiserver-k8s-master            1/1     Running   0          9m9s
kube-system    kube-controller-manager-k8s-master   1/1     Running   0          9m9s
kube-system    kube-proxy-n4wgq                     1/1     Running   0          8m57s
kube-system    kube-scheduler-k8s-master            1/1     Running   0          9m9s

# 此时Master节点就准备好了
[root@k8s-master ~]# kubectl get nodes
NAME         STATUS   ROLES                  AGE   VERSION
k8s-master   Ready    control-plane,master   25m   v1.20.9
```

## 5.按照提示执行_加入Node节点

```bash
# 在k8s-node1和k8s-node2节点上执行
kubeadm join cluster-endpoint:6443 --token l6xadf.j3opsz26ytaroy4q \
    --discovery-token-ca-cert-hash sha256:553c3aa1fb135a55a337eadd1089d1b8a5a6252ae8fa7baba08ade886203707d  
```

><font color="#f79646">问题1.超时场景一</font>

```bash
[root@k8s-node1 ~]# kubeadm join cluster-endpoint:6443 --token pomq3a.uk8f5vzd7zan8wg4     --discovery-token-ca-cert-hash sha256:f893c561a345a1682490326165916a6d1be8817e8d27a4a7d1c462521ea3caa1 
[preflight] Running pre-flight checks
	[WARNING SystemVerification]: this Docker version is not on the list of validated versions: 20.10.7. Latest validated version: 19.03
systemctl status firewalld.service
error execution phase preflight: couldn't validate the identity of the API Server: could not find a JWS signature in the cluster-info ConfigMap for token ID "pomq3a"
```

解决方案：重新在Master节点创建新的令牌，再重试即可。

```
[root@k8s-master ~]# kubeadm token create --print-join-command
kubeadm join cluster-endpoint:6443 --token oqakwf.9563iqwgx2ig7rdg     --discovery-token-ca-cert-hash sha256:e22712ddf7cfdb032c0a37a0940b4a4c8106bac7a831f41b695fe00e7381dfd1
```

## 6.验证

```
[root@k8s-master ~]# kubectl get pods -A
NAMESPACE      NAME                                 READY   STATUS    RESTARTS   AGE
kube-flannel   kube-flannel-ds-9zlpm                1/1     Running   0          9m9s
kube-flannel   kube-flannel-ds-hh8hm                1/1     Running   0          8m43s
kube-flannel   kube-flannel-ds-zmzsl                1/1     Running   0          11m
kube-system    coredns-5897cd56c4-9fb2p             1/1     Running   0          12m
kube-system    coredns-5897cd56c4-fxg2t             1/1     Running   0          12m
kube-system    etcd-k8s-master                      1/1     Running   0          13m
kube-system    kube-apiserver-k8s-master            1/1     Running   0          13m
kube-system    kube-controller-manager-k8s-master   1/1     Running   0          13m
kube-system    kube-proxy-5bgt6                     1/1     Running   0          9m9s
kube-system    kube-proxy-nn9ct                     1/1     Running   0          12m
kube-system    kube-proxy-zxp4g                     1/1     Running   0          8m43s
kube-system    kube-scheduler-k8s-master            1/1     Running   0          13m
[root@k8s-master ~]# kubectl get nodes
NAME         STATUS   ROLES                  AGE     VERSION
k8s-master   Ready    control-plane,master   14m     v1.20.9
k8s-node1    Ready    <none>                 10m     v1.20.9
k8s-node2    Ready    <none>                 9m44s   v1.20.9
```

## 7.安装Dashboard

### 7.1.部署

Kubernetes官方提供的可视化界面：[https://github.com/kubernetes/dashboard](https://github.com/kubernetes/dashboard)

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
```

>如果访问不了，可以自行下载下来~

### 7.2.设置访问端口

```
kubectl edit svc kubernetes-dashboard -n kubernetes-dashboard
# 第1步.输入'/'， 搜索ClusterIP
# 第2步.输入'i'， 修改type: ClusterIP -> type: NodePort
# 第3步.输入'wq'，保存即可~
```

查看访问端口（如果不是虚拟机的话，需要在安全组放行端口）

```
[root@k8s-master ~]# kubectl get svc -A |grep kubernetes-dashboard
kubernetes-dashboard   dashboard-metrics-scraper   ClusterIP   10.96.98.192    <none>        8000/TCP                 2m13s
kubernetes-dashboard   kubernetes-dashboard        NodePort    10.96.224.249   <none>        443:30557/TCP            2m13s
```

使用集群任意IP均可以访问：https://192.168.91.12:30557

Chrome您的连接不是私密连接解决办法，当前页面用键盘输入thisisunsafe ，不是在地址栏输入，就直接敲键盘就行了~

![[Pasted image 20240613123711.png|1000]]

### 7.3.创建访问账号

```yaml
# 创建访问账号，准备一个yaml文件: vi dash.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

```bash
kubectl apply -f dash.yaml
```

```bash
# 获取访问令牌
kubectl -n kubernetes-dashboard get secret $(kubectl -n kubernetes-dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"
```

```
eyJhbGciOiJSUzI1NiIsImtpZCI6InYwUzdpUF9LVFBvbS00d1dNTWFUcVBwV21UbllVS2RoUzlIbzQtMWhNMFEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLXhyMjk3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI2NzVjNTk4Ni0yZTM4LTQzYzAtODY1My00ZDE5MDlmNDU5YTUiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.Jom1gHgGSTIVGais2Fqb6gmozu73RsikL6ojpvBc9ugI0XDUuEmqYKsYq4g9HQX4nGxHZQqowlPkDVpIlvU2ImQcpZH4iX-ilU2gdmBCdmh8DTpLlBHnXx7mrjO7HkrvBI-YTuxU6a1UNffUYhzA-EewYs_OX4yW9CiLzlq4uCi_yMioxzwS8X0xH6QcxgftPzrJmWeXzKxFBVQsTWu2qBO6r6TJlpeNLHBiTYxNLJYMoLQm2gG9XoLaYq1YqlJGQ_cVcOJsIKqwMPyIzjXc39BS88Fy6xsfTDW_FYTrvAJmKdVLdfM5PRVB7OK8RlGwE8dB1nkWShxi0ZfQC3Hp9Q
```

![[Pasted image 20240613134701.png|1000]]


