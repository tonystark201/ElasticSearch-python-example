# Using Python to Search data in ElasticSearch  Cluster

## ElasticSearch

## Docker Compose

> Docker Compose is a tool that was developed to help define and share multi-container applications. With Compose, we can create a YAML file to define the services and with a single command, can spin everything up or tear it all down.

When deploying service clusters locally for some common testing, engineers will prefer Docker for containerized deployment. As an artifact of container orchestration, docker compose is favored by countless engineers, and the docker compose has got unanimous praise.

### Build Service

1. Edit your own `docker-compose.yml` file according to the syntax of the compose tools. __*For this demo you can check and review my compose file in the folder of "compose" in this Repo*__

2. Run the command as below.

   ```shell
   docker-compose up -d --build
   ```

3. Waiting! Then check the status

   ```shell
   docker-compose ps
   ```

   You can see the result as below.

   ```shell
   ElasticSearch-python-example\compose>docker-compose ps
    Name                Command               State                                         Ports
   -------------------------------------------------------------------------------------------------------------------------------------
   cerebro   /opt/cerebro/bin/cerebro - ...   Up      0.0.0.0:9000->9000/tcp,:::9000->9000/tcp
   es01      /tini -- /usr/local/bin/do ...   Up      0.0.0.0:9200->9200/tcp,:::9200->9200/tcp, 0.0.0.0:9301->9300/tcp,:::9301->9300/tcp
   es02      /tini -- /usr/local/bin/do ...   Up      0.0.0.0:9201->9200/tcp,:::9201->9200/tcp, 0.0.0.0:9302->9300/tcp,:::9302->9300/tcp
   es03      /tini -- /usr/local/bin/do ...   Up      0.0.0.0:9202->9200/tcp,:::9202->9200/tcp, 0.0.0.0:9303->9300/tcp,:::9303->9300/tcp
   kibana    /usr/local/bin/dumb-init - ...   Up      0.0.0.0:5601->5601/tcp,:::5601->5601/tcp
   ```

4. If some service exit, you can check the logs

   ```shell
   docker-compose logs es03
   ```

   Your can see the result as below.(The timezone is UTC)

   ```shell
   Attaching to es03
   es03       | {"type": "server", "timestamp": "xxxxxxxx", "level": "INFO", "component": "o.e.n.Node", "cluster.name": "es_cluster", "node.name": "es03", "message": "version[7.8.0], pid[8], build[default/docker/757314695644ea9a1dc2fecd26d1a43856725e65/2020-06-14T19:35:50.234439Z], OS[Linux/5.10.25-linuxkit/amd64], JVM[AdoptOpenJDK/OpenJDK 64-Bit Server VM/14.0.1/14.0.1+7]" }
   es03       | {"type": "server", "timestamp": "xxxxxxxx", "level": "INFO", "component": "o.e.n.Node", "cluster.name": "es_cluster", "node.name": "es03", "message": "JVM home [/usr/share/elasticsearch/jdk]" }
   es03       | {"type": "server", "timestamp": "xxxxxxxx", "level": "INFO", "component": "o.e.n.Node", "cluster.name": "es_cluster", "node.name": "es03", "message": "JVM arguments [-Xshare:auto, -Des.networkaddress.cache.ttl=60, -Des.networkaddress.cache.negative.ttl=10, -XX:+AlwaysPreTouch, -Xss1m, -Djava.awt.headless=true, -Dfile.encoding=UTF-8, -Djna.nosys=true, -XX:-OmitStackTraceInFastThrow, -XX:+ShowCodeDetailsInExceptionMessages, -Dio.netty.noUnsafe=true, -Dio.netty.noKeySetOptimization=true, -Dio.netty.recycler.maxCapacityPerThread=0, -Dio.netty.allocator.numDirectArenas=0, -Dlog4j.shutdownHookEnabled=false, -Dlog4j2.disable.jmx=true, -Djava.locale.providers=SPI,COMPAT, -Xms1g, -Xmx1g, -XX:+UseG1GC, -XX:G1ReservePercent=25, -XX:InitiatingHeapOccupancyPercent=30, -Djava.io.tmpdir=/tmp/elasticsearch-11918629754561330994, -XX:+HeapDumpOnOutOfMemoryError, -XX:HeapDumpPath=data, -XX:ErrorFile=logs/hs_err_pid%p.log, -Xlog:gc*,gc+age=trace,safepoint:file=logs/gc.log:utctime,pid,tags:filecount=32,filesize=64m, -Des.cgroups.hierarchy.override=/, -Xms256m, -Xmx256m, -XX:MaxDirectMemorySize=134217728, -Des.path.home=/usr/share/elasticsearch, -Des.path.conf=/usr/share/elasticsearch/config, -Des.distribution.flavor=default, -Des.distribution.type=docker, -Des.bundled_jdk=true]" }
   es03       | {"type": "server", "timestamp": "xxxxxxxx", "level": "INFO", "component": "o.e.p.PluginsService", "cluster.name": "es_cluster", "node.name": "es03", "message": "loaded module [aggs-matrix-stats]" }
   es03       | {"type": "server", "timestamp": "xxxxxxxx", "level": "INFO", "component": "o.e.p.PluginsService", "cluster.name": "es_cluster", "node.name": "es03", "message": "loaded module [analysis-common]" }
   ```

### Tools Display

+ The `Kibana`

  __*When the docker container run successfully, you can put the `http://127.0.0.1:5601` in the browser URL location, then you can the page as below.*__

![image-20220704231751925](E:\GitTonyStark\RepoPublic\ElasticSearch-python-example\img\image-20220704231751925.png)

+ The` Cerebro`

  __*When the docker container run successfully, you can put the `http://127.0.0.1:9000` in the browser URL location, then you can the page as below.*__ All the three instances are running and status is green.

  ![image-20220704232035871](E:\GitTonyStark\RepoPublic\ElasticSearch-python-example\img\image-20220704232035871.png)

## Summary







## Reference

+ [Using volumes in Docker Compose](https://devopsheaven.com/docker/docker-compose/volumes/2018/01/16/volumes-in-docker-compose.html)