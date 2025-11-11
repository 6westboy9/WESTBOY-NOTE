# 命名空间

> [!important] 
> Namespace只隔离资源，不隔离网络！


```bash
# 查询命名空间
[root@k8s-master ~]# kubectl get ns
NAME                   STATUS   AGE
default                Active   146m
kube-flannel           Active   144m
kube-node-lease        Active   146m
kube-public            Active   146m
kube-system            Active   146m
kubernetes-dashboard   Active   110m
```

```bash
# 仅获取默认命名空间下的Pod
[root@k8s-master ~]# kubectl get pods
No resources found in default namespace.

# 获取全部命名空间下的Pod
[root@k8s-master ~]# kubectl get pods -A
NAMESPACE              NAME                                         READY   STATUS    RESTARTS   AGE
kube-flannel           kube-flannel-ds-9zlpm                        1/1     Running   0          144m
kube-flannel           kube-flannel-ds-hh8hm                        1/1     Running   0          144m
kube-flannel           kube-flannel-ds-zmzsl                        1/1     Running   0          146m
kube-system            coredns-5897cd56c4-9fb2p                     1/1     Running   0          148m
kube-system            coredns-5897cd56c4-fxg2t                     1/1     Running   0          148m
kube-system            etcd-k8s-master                              1/1     Running   0          148m
kube-system            kube-apiserver-k8s-master                    1/1     Running   0          148m
kube-system            kube-controller-manager-k8s-master           1/1     Running   0          148m
kube-system            kube-proxy-5bgt6                             1/1     Running   0          144m
kube-system            kube-proxy-nn9ct                             1/1     Running   0          148m
kube-system            kube-proxy-zxp4g                             1/1     Running   0          144m
kube-system            kube-scheduler-k8s-master                    1/1     Running   0          148m
kubernetes-dashboard   dashboard-metrics-scraper-79c5968bdc-jfqs5   1/1     Running   0          112m
kubernetes-dashboard   kubernetes-dashboard-658485d5c7-6kc9n        1/1     Running   0          112m
```

>操作方式1.命令行方式

```
kubectl create ns hello
kubectl delete ns hello
```

>操作方式2.YAML配置文件方式

```yml
apiVersion: v1
kind: Namespace
metadata:
  name: hello
```

# Pod

![[Pasted image 20240613190827.png|800]]

```bash
[root@k8s-master ~]# kubectl run mynginx --image=nginx
pod/mynginx created
[root@k8s-master ~]# kubectl get pod 
NAME      READY   STATUS              RESTARTS   AGE
mynginx   0/1     ContainerCreating   0          7s
```


```bash
[root@k8s-master ~]# kubectl describe pod mynginx
Name:         mynginx
Namespace:    default
Priority:     0
Node:         k8s-node1/192.168.91.12
Start Time:   Fri, 14 Jun 2024 09:39:27 +0800
Labels:       run=mynginx
Annotations:  <none>
Status:       Running
IP:           172.16.1.3
IPs:
  IP:  172.16.1.3
Containers:
  mynginx:
    Container ID:   docker://b7008bd10f58470c6cdda2d017f492b0b0281e59382e4814e4acbea738ac7fa5
    Image:          nginx
    Image ID:       docker-pullable://nginx@sha256:0d17b565c37bcbd895e9d92315a05c1c3c9a29f762b011a10c54a66cd53c9b31
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Fri, 14 Jun 2024 09:40:00 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-hzxts (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-hzxts:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-hzxts
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  35s   default-scheduler  Successfully assigned default/mynginx to k8s-node1
  Normal  Pulling    32s   kubelet            Pulling image "nginx"
  Normal  Pulled     3s    kubelet            Successfully pulled image "nginx" in 29.15196482s
  Normal  Created    2s    kubelet            Created container mynginx
  Normal  Started    2s    kubelet            Started container mynginx
[root@k8s-master ~]# kubectl describe pod mynginx
Name:         mynginx
Namespace:    default
Priority:     0
Node:         k8s-node1/192.168.91.12
Start Time:   Fri, 14 Jun 2024 09:39:27 +0800
Labels:       run=mynginx
Annotations:  <none>
Status:       Running
IP:           172.16.1.3
IPs:
  IP:  172.16.1.3
Containers:
  mynginx:
    Container ID:   docker://b7008bd10f58470c6cdda2d017f492b0b0281e59382e4814e4acbea738ac7fa5
    Image:          nginx
    Image ID:       docker-pullable://nginx@sha256:0d17b565c37bcbd895e9d92315a05c1c3c9a29f762b011a10c54a66cd53c9b31
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Fri, 14 Jun 2024 09:40:00 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-hzxts (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-hzxts:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-hzxts
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  36s   default-scheduler  Successfully assigned default/mynginx to k8s-node1
  Normal  Pulling    33s   kubelet            Pulling image "nginx"
  Normal  Pulled     4s    kubelet            Successfully pulled image "nginx" in 29.15196482s
  Normal  Created    3s    kubelet            Created container mynginx
  Normal  Started    3s    kubelet            Started container mynginx
```

```bash
[root@k8s-master ~]# kubectl get pod 
NAME      READY   STATUS    RESTARTS   AGE
mynginx   1/1     Running   0          40s
```

```bash
[root@k8s-master ~]# kubectl logs mynginx
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/06/14 01:40:00 [notice] 1#1: using the "epoll" event method
2024/06/14 01:40:00 [notice] 1#1: nginx/1.21.5
2024/06/14 01:40:00 [notice] 1#1: built by gcc 10.2.1 20210110 (Debian 10.2.1-6) 
2024/06/14 01:40:00 [notice] 1#1: OS: Linux 3.10.0-1160.el7.x86_64
2024/06/14 01:40:00 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/06/14 01:40:00 [notice] 1#1: start worker processes
2024/06/14 01:40:00 [notice] 1#1: start worker process 31
2024/06/14 01:40:00 [notice] 1#1: start worker process 32
```