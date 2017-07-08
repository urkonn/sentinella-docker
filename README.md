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


-----


# License

Released under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

