import os
import json
import logging

import trollius as asyncio
from trollius import From
import docker

logger = logging.getLogger(__name__)

frequency = 60
hostname = os.uname()[1].split('.')[0]

@asyncio.coroutine
def docker_stats(agent):
    yield From(agent.run_event.wait())

    """
    After plugin installation, copy the configuration file
    from sentinella-plugin-template/conf/ to /etc/sentinella/conf.d/
    """
    config = agent.config['sentinella-docker']
    
    """
    The plugin Key is a unique UUID provided by Sentinel.la.
    If not valid, the plugin metrics will never be registered.
    """

    plugin_key = config['plugin_key']

    logger.info('starting "get_stats" task for plugin_key "%s"  and host "%s"'.format(plugin_key,hostname))

    while agent.run_event.is_set():
        yield From(asyncio.sleep(frequency))
        try:
            data = {'server_name': hostname,
                    'plugins': {}}
            logger.debug('connecting to data source')
            
            """
            Get the total number of containers and the following information of each of them:
            Container id, container name, status, cpu usage, memory usage
            Example output:
            
            Total number of containers: 4
            CONTAINER   NAME    STATUS  CPU     MEM
            52171d5537 neo4j running 11062784697 803483648
            f9b1282d05 nginx exited
            """

            data['plugins'].update({"{}".format(plugin_key):{}})
             
            client = docker.from_env()
            container_list = client.containers.list(all)
            data['plugins'][plugin_key].update({"number_of_containers": { "value":len(container_list),"type":"integer" }})

            for container in container_list:
                if container.status != 'running':
                    metric = "{0}-status".format(container.name)
                    data['plugins'][plugin_key].update({metric:{"value":container.status,"type": "string"}})
                else:
                    metric = "{0}-status".format(container.name)
                    data['plugins'][plugin_key].update({metric:{"value":container.status,"type":"string"}})
                    cpu = container.stats(decode=True, stream=False)['cpu_stats']['cpu_usage']['total_usage']
                    metric = "{0}-cpu".format(container.name)
                    data['plugins'][plugin_key].update({metric:{"value":cpu,"type":"integer"}})
                    metric = "{0}-memory".format(container.name)
                    mem = container.stats(decode=True, stream=False)['memory_stats']['usage']
                    data['plugins'][plugin_key].update({metric:{"value":mem,"type":"integer" }})
                    """
                    print (container.short_id,
                           container.name,
                           container.status,
                           container.stats(decode=True, stream=False)['cpu_stats']['cpu_usage']['total_usage'],
                           container.stats(decode=True, stream=False)['memory_stats']['usage'])
                    """

            logger.debug('{}: dockerplugin={}%'.format(hostname, data))

            yield From(agent.async_push(data))

        except:

            logger.exception('cannot get data source information')

    logger.info('get_stats terminated')
