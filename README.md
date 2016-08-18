# job_test_rs

## Apresentação
Demonstrar conhecimentos em nginx, mount (fstab), python e fabric. Vou apresentar as linhas de comando para realizar as tarefas de: verificação do mountpoint, instalação do nginx, configuração e iniciação do serviço. E ao final irei apresentar uma automatização desse processo.

## Tarefas
Check if is mounted. Helper: is_mounted() on fabfile.py
```
sudo mount -l | grep /data
```

Create directory to mountpoint if is not exists.
```
sudo mkdir /data
```

Mount partition on mountpoint. If partition is on fstab, run ```mount -a```. Helper: mount() on fabfile.py
```
sudo mount {path/partition} /data 
```

Check if nginx is installed. Helper: check_nginx() in fabfile.py 
```
sudo which nginx
```

If you don't have nginx, install it and run.
```
sudo apt-get update; sudo apt-get install nginx; sudo service nginx start;
```

Create a configuration file ```/etc/nginx/sites-available/{project_name}```.
```
server {
    listen 80;
    server_name %(server_name)s;

    charset utf-8;

    root %(path_mountpoint)s;
    index %(page_index)s;

    access_log %(access_log)s;
    error_log %(error_log)s;

    location /%(project_name)s{
        try_files $uri $uri/ /index.html;
    }

    location /%(extra_location)s{
        return 301 $scheme://$server_name/%(project_name)s;
    }

    location /%(proxy_location)s{
        proxy_pass http://%(proxy_host)s;
        proxy_redirect http://%(proxy_host)s http://%(server_name)s/%(proxy_location)s/;
    }
}
```

Create web file ```/data/index.html```.
```
<!DOCTYPE html>
<html>
<head>
    <title>%(project_name)s</title>
    <style>
    body {
        width: 35em;
        margin: 0 auto;
        font­family: Tahoma, Verdana, Arial, sans­serif;
    }
    </style>
</head>
<body>
    <h1>This is my APP: %(project_name)s!</h1>
    <p>Your APP index page can be shown.</p>
</body>
</html>
```

Linking new configuration file to enabled folder on nginx.
```
ln -sf /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled/{project_name}
```

Restart nginx to changes takes effects.
```
sudo service nginx restart
```

# Automação

## Requisitos
```
virtualenv fabricenv

source fabricenv/bin/active

pip install fabric

```

## Configurações
Basta configurar o webserver e globals:
```
env.project_name = '' # project_name

env.hosts = [''] # webserver
env.port = '' # port to connect
env.user = '' # create a diferente user like deploy
env.path_mountpoint = '' # complete path to mounted partition
env.path_partition = '' # complete path to partition to mount
env.proxy_host = '' # proxy host to serve
env.server_name = '' # same the env.hosts
env.proxy_location = '' # path to proxy
env.access_log = '' # path to access logs
env.error_log = '' # path to error logs
env.page_index = '' # index root
env.extra_location = '' # extra location path
env.extra_index = '' # index name to extra location
```

Depois de configurado basta rodar:
```
fab webserver deploy
```

Para ver uma lista de tasks and helpers:
```
fab -l
```


## Referências
- https://www.freebsd.org/doc/handbook/mount-unmount.html
- http://nginx.org/en/docs/install.html
- http://nginx.org/en/docs/http/ngx_http_proxy_module.html
- http://docs.fabfile.org/en/1.12/api/contrib/files.html