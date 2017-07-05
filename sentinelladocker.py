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
            client = docker.from_env(version='auto')
            container_list = client.containers.list()
            
            # Number of containers
            containers = {
                            "number_of_containers":{
                                "row_name": "Containers",
                                "metric_name": "Number of containers",
                                "value":len(container_list),
                                "type":"number"
                            }
                        }

            data['plugins'][plugin_key].update(containers)

            for container in container_list:
                id = container.id
                if container.status != 'running':
                    
                    body = {
                            "container_status_{0}".format(id):{
                                "row_name": container.name,
                                "metric_name":"status",
                                "value":container.status,
                                "type":"String"
                            }
                        }

                    data['plugins'][plugin_key].update(body)

                else:

                    body = {
                            "container_status_{0}".format(id):{
                                "row_name": container.name,
                                "metric_name":"status",
                                "value":container.status,
                                "type":"String"
                            }
                        }

                    data['plugins'][plugin_key].update(body)
                    
                    cpu_total_usage = container.stats(decode=True, stream=False)['cpu_stats']['cpu_usage']['total_usage']
                    precpu_total_usage = container.stats(decode=True, stream=False)['precpu_stats']['cpu_usage']['total_usage']
                    cpuDelta = float(cpu_total_usage) - float(precpu_total_usage)

                    system_cpu_usage = container.stats(decode=True, stream=False)['cpu_stats']['system_cpu_usage']
                    system_precpu_usage = container.stats(decode=True, stream=False)['precpu_stats']['system_cpu_usage']
                    systemDelta = float(system_cpu_usage) - float(system_precpu_usage)

                    cpu_usage = cpuDelta / systemDelta * 100;

                    body = {
                            'container_cpu_{0}'.format(id):{
                                "row_name":container.name,
                                "metric_name":"cpu",
                                "value":round(cpu_usage,2),
                                "type":"%"
                            }
                        }

                    data['plugins'][plugin_key].update(body)

                    memory = container.stats(decode=True, stream=False)['memory_stats']['usage']
                    limit = container.stats(decode=True, stream=False)['memory_stats']['limit']
                    memory_usage = float(memory) / float(limit) * 100
                    
                    body = {
                            'container_memory_{0}'.format(id):{
                                "row_name":container.name,
                                "metric_name":"memory",
                                "value":round(memory_usage,2),
                                "type":"%"
                            }
                        }

                    data['plugins'][plugin_key].update(body)
                    


            logger.debug('{}: dockerplugin={}%'.format(hostname, data))

            yield From(agent.async_push(data))

        except:

            logger.exception('cannot get data source information')

    logger.info('get_stats terminated')