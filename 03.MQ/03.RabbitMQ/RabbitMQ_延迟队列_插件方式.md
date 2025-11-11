
## 查看插件

```bash
# 查看已经安装的插件
[root@localhost sbin]# rabbitmq-plugins list
Listing plugins with pattern ".*" ...
 Configured: E = explicitly enabled; e = implicitly enabled
 | Status: * = running on rabbit@localhost
 |/
[  ] rabbitmq_amqp1_0                  3.8.5
[  ] rabbitmq_auth_backend_cache       3.8.5
[  ] rabbitmq_auth_backend_http        3.8.5
[  ] rabbitmq_auth_backend_ldap        3.8.5
[  ] rabbitmq_auth_backend_oauth2      3.8.5
[  ] rabbitmq_auth_mechanism_ssl       3.8.5
[  ] rabbitmq_consistent_hash_exchange 3.8.5
[  ] rabbitmq_event_exchange           3.8.5
[  ] rabbitmq_federation               3.8.5
[  ] rabbitmq_federation_management    3.8.5
[  ] rabbitmq_jms_topic_exchange       3.8.5
[E*] rabbitmq_management               3.8.5
[e*] rabbitmq_management_agent         3.8.5
[  ] rabbitmq_mqtt                     3.8.5
[  ] rabbitmq_peer_discovery_aws       3.8.5
[  ] rabbitmq_peer_discovery_common    3.8.5
[  ] rabbitmq_peer_discovery_consul    3.8.5
[  ] rabbitmq_peer_discovery_etcd      3.8.5
[  ] rabbitmq_peer_discovery_k8s       3.8.5
[E*] rabbitmq_prometheus               3.8.5
[  ] rabbitmq_random_exchange          3.8.5
[  ] rabbitmq_recent_history_exchange  3.8.5
[  ] rabbitmq_sharding                 3.8.5
[  ] rabbitmq_shovel                   3.8.5
[  ] rabbitmq_shovel_management        3.8.5
[e*] rabbitmq_stomp                    3.8.5
[  ] rabbitmq_top                      3.8.5
[  ] rabbitmq_tracing                  3.8.5
[  ] rabbitmq_trust_store              3.8.5
[e*] rabbitmq_web_dispatch             3.8.5
[  ] rabbitmq_web_mqtt                 3.8.5
[  ] rabbitmq_web_mqtt_examples        3.8.5
[E*] rabbitmq_web_stomp                3.8.5
[  ] rabbitmq_web_stomp_examples       3.8.5
```

## 查看插件目录

>1.下载插件~

* 官方插件：https://www.rabbitmq.com/community-plugins
* 延迟插件Github地址：https://github.com/rabbitmq/rabbitmq-delayed-message-exchange
* <font color="#c0504d">注意版本兼容性</font>

>2.放置到RabbitMQ的插件目录<font color="#c0504d">plugins</font>下，并使其生效~

```bash
[root@localhost plugins]# cd /usr/lib/rabbitmq/lib/rabbitmq_server-3.8.5/plugins

# 启用插件
[root@localhost plugins]# rabbitmq-plugins enable rabbitmq_delayed_message_exchange
Enabling plugins on node rabbit@localhost:
rabbitmq_delayed_message_exchange
The following plugins have been configured:
  rabbitmq_delayed_message_exchange
  rabbitmq_management
  rabbitmq_management_agent
  rabbitmq_prometheus
  rabbitmq_stomp
  rabbitmq_web_dispatch
  rabbitmq_web_stomp
Applying plugin configuration to rabbit@localhost...
The following plugins have been enabled:
  rabbitmq_delayed_message_exchange

started 1 plugins.

# 禁用插件
[root@localhost ~]# rabbitmq-plugins disable rabbitmq_delayed_message_exchange
Disabling plugins on node rabbit@localhost:
rabbitmq_delayed_message_exchange
The following plugins have been configured:
  rabbitmq_management
  rabbitmq_management_agent
  rabbitmq_prometheus
  rabbitmq_stomp
  rabbitmq_web_dispatch
  rabbitmq_web_stomp
Applying plugin configuration to rabbit@localhost...
The following plugins have been disabled:
  rabbitmq_delayed_message_exchange

stopped 1 plugins.
```

问题：使用插件实现延迟消息后，发送的消息一直没有被消费会丢失吗？

