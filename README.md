# job_test_rs

## Apresentação
Demonstrar conhecimentos básicos em nginx, mount (fstab), python e fabric. Será apresentado as linhas de comando para realizar as tarefas de verificação do mountpoint, montagem, verificação do nginx, instalação, configuração e iniciação do serviço. E ao final será apresentado uma automatização desse processo com fabric.

Para montar a particição as premissas são:
- partição já listada no /etc/fstab;

Para a configuração do nginx as premissas são:

- Requisitar url webserver.com.br/app1 mostrar index.html (/), mas sem mostrar o nome do arquivo no final do url;
- Requisitar url webserver.com.br/app2 redirecionar para webserver.com.br/app1;
- Requisitar webserver.com.br/proxy mostrar página do host.proxy.com.br mas não mudar a URL;
- Persistir essas configurações mesmo com o reboot do servidor;

## Tarefas
Primeiro acesse o servidor, se for realizar local (locahost) pule essa parte.
```
ssh user@webserver.com.br
```

1. Check if mountpoint is mounted. Helper: is_mounted() on fabfile.py
	```
	sudo mount -l | grep /data
	```

2. Create directory to mountpoint if is not exists.
	```
	ls -l /data
	ls: cannot access /data: No such file or directory
	```
	```
	sudo mkdir /data
	```

3. Mount partition on mountpoint. If partition is on fstab, run ` sudo mount -a `. Helper: mount() on fabfile.py
	```
	sudo mount {path/partition} /data
	```

4. Check if nginx is installed. Helper: check_nginx() in fabfile.py 
	```
	sudo which nginx
	```

5. If you don't have nginx, install it and run. Helper: install_nginx() in fabfile.py
	```
	sudo apt-get update; sudo apt-get install nginx; sudo service nginx start;
	```

6. Create a configuration file ` /etc/nginx/sites-available/{project_name} `. Helper: create_and_link_site_project() in fabfile.py
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

	    location /%(extra_location)s{ # redirect to project_name
	        return 301 $scheme://$server_name/%(project_name)s;
	    }

	    location /%(proxy_location)s{ # proxy external host
	        proxy_pass http://%(proxy_host)s;
	        proxy_redirect http://%(proxy_host)s http://%(server_name)s/%(proxy_location)s/;
	    }
	}
	```

7. Create web file `/data/index.html`. Helper: create_index_html() in fabfile.py
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

8. Linking new configuration file to enabled folder on nginx. Helper: symb_link_enable_project_nginx() in fabfile.py
	```
	ln -sf /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled/{project_name}
	```

9. Restart nginx to changes takes effects. Helper: restart_nginx() in fabfile.py
	```
	sudo service nginx restart
	```

# Automação
Você prcisa do python instalado. Veja https://www.python.org/downloads/.
Recomendo criar uma virtualenv antes de instalar os requisitos de ` requirements.txt `. Veja https://virtualenv.pypa.io/en/stable/installation/.

## Criar virtualenv
```
virtualenv nginx_fabric
```

## Ativar sua nova virtualenv
```
source nginx_fabric/bin/active
```

## Instalar os requisitos
```
pip install -r requirements.txt

```

## Configurações
Agora basta configurar as variáveis no arquivo ` fabfile.py `:
```
env.project_name = '' # project_name

# server config
env.hosts = [''] # IP or hostname webserver
env.port = '' # port to connect
env.user = '' # create a diferente user like deploy

# fstab/mount configs
env.path_mountpoint = '' # complete path to mounted partition
env.path_partition = '' # complete path to partition to mount

# nginx configs
env.server_name = '' # same the env.hosts
env.page_index = '' # index root
env.access_log = '' # path to access logs
env.error_log = '' # path to error logs
env.proxy_host = '' # proxy host to serve
env.proxy_location = '' # path to proxy
env.extra_location = '' # extra location path
env.extra_index = '' # index name to extra location
```

## Executar
Depois de configurar faça um deploy completo:
```
fab webserver deploy
```

Ou, veja uma lista de tasks and helpers:
```
fab -l

Available commands:

    check_nginx                     Check if nginx is installed
    create_and_link_site_project    Create nginx configuration file to project
    create_index_html               Create index file
    deploy                          Make a full deploy
    install_nginx                   Install nginx
    is_mounted                      Check if mountpoint is mounted
    mount                           Mount partition on mountpoint
    restart_nginx                   Restart nginx
    setup                           Setup and mount partition
    start_nginx                     Start nginx
    symb_link_enable_project_nginx  Symbolic links to enable projects on nginx
    test_nginx                      Test configurations files for nginx
    webserver                       Use the webserver

```

Uso:
```
fab [webserver] [task]
```

## Referências
- https://www.freebsd.org/doc/handbook/mount-unmount.html
- http://nginx.org/en/docs/install.html
- http://nginx.org/en/docs/http/ngx_http_proxy_module.html
- http://docs.fabfile.org/en/1.12/api/contrib/files.html