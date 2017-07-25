#### A plugin for collecting Docker containers metrics and store them into Sentinel.la. http://sentinel.la

-----

# What is sentinella-docker?

sentinella-docker plugin gets Docker containers metrics into [Sentinel.la](https://www.sentinel.la)

![Sentinella Docker}](/images/sentinellaDocker.png)

In order to this plugin to work, Docker should run as a service not by a sudo user.

``` bash
$ usermod -a -G docker sentinella
$ sentinella install sentinella-docker 0.1
```

# Configurartio plugin

``` bash
$ vi /etc/sentinella/sentinella.conf
```
Add the next cofiguration in section plugins

``` bash
....

"plugins": {

        "sentinella.openstack_logs": [

            "get_openstack_events"

        ], 

        "sentinella.metrics": [

            "get_server_usage_stats"

        ],

        "sentinella.sentinelladocker": [

            "docker_stats"

        ]

    },

....

```

-----


# License

Released under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

