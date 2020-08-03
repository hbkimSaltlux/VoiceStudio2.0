import docker
from docker.models.containers import Container
from typing import Dict, List, Union
from core.saltlux.utils.custom_exception import CustomError


def run_container_bg(name: str, command: Union[List, str], image: str, working_dir: str, run_time: str = 'runc',
                     volumes: Dict = {}, ports: Dict = {}, auto_remove: bool = True) -> Container:
    client = docker.from_env()
    container = client.containers.run(name=name, command=command, image=image, runtime=run_time,
                                      working_dir=working_dir, volumes=volumes, ports=ports, auto_remove=auto_remove,
                                      detach=True)
    return container


def run_container_fg(name: str, command: Union[List, str], image: str, working_dir: str, run_time: str = 'runc',
                     volumes: Dict = {}, ports: Dict = {}, auto_remove: bool = True) -> str:
    client = docker.from_env()

    logs = client.containers.run(name=name, command=command, image=image, runtime=run_time,
                                 working_dir=working_dir, volumes=volumes, ports=ports, auto_remove=True,
                                 detach=False, stdout=True, stderr=True)

    return logs


def get_container(key: str) -> Union[Container, None]:
    client = docker.from_env()

    containers = client.containers.list(filters={'name': key})

    size = len(containers)
    if size > 1:
        raise CustomError(-1, '키에 해당하는 컨테이너가 여러개 입니다. (key : {})'.format(key))

    elif size == 1:
        return containers[0]

    else:
        return None


def get_containers_status(key: str) -> Union[Dict, None]:
    container = get_container(key)

    state = {}
    if container is None:
        return None

    else:
        container_attrs = container.attrs
        state['status'] = container_attrs['State']['Status']
        state['startTime'] = container_attrs['State']['StartedAt']
        state['image'] = container_attrs['Config']['Image']

        return state


if __name__ == '__main__':
    client = docker.from_env()
    # for container in client.containers.list():
    #     print(container.attrs['HostConfig']['Runtime'])

    containers = client.containers.list(filters={'name': 'amt_hikim'})
    print(len(containers))
    for container in containers:
        import json
        print(json.dumps(container.attrs))

