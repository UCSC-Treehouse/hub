import os

c = get_config()
c.JupyterHub.debug_proxy = True

# Spawn a docker container per user
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.debug = True
c.DockerSpawner.remove_containers = True

# Spawn user containers from this image
c.DockerSpawner.container_image = 'jupyter'
# c.DockerSpawner.container_image = 'jupyter/datascience-notebook'

c.DockerSpawner.notebook_dir = '/home/jovyan/work'
c.DockerSpawner.volumes={'/data/notebooks/{username}': '/home/jovyan/work',
                         '/data': '/data',
                         '/var/run/docker.sock': '/var/run/docker.sock'}
# c.DockerSpawner.read_only_volumes = {'/data/notebooks/': '/home/jovyan/work/readonly'}
c.DockerSpawner.extra_create_kwargs.update({'volume_driver': 'local'})

# This is to ensure that a docker volume can be created when the user name
# contains special characters
# c.DockerSpawner.format_volume_name = c.DockerSpawner.volumenamingstrategy.escaped_format_volume_name

# Connect containers to this Docker network
network_name = os.environ['COMPOSE_PROJECT_NAME'] + '_default'
c.DockerSpawner.network_name = network_name
# c.DockerSpawner.extra_host_config.update({'network_mode': network_name})

# User containers will access hub by container name on the Docker network
c.DockerSpawner.container_ip = "0.0.0.0"
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080
c.JupyterHub.port = 8000

# Have the Spawner override the Docker run command
c.DockerSpawner.extra_create_kwargs.update({
    'command': '/usr/local/bin/start-singleuser.sh'
})
c.DockerSpawner.environment = {
    'JPY_USER': 'root',
    'GRANT_SUDO': '1'
}

# Persist hub data on volume mounted inside container
c.JupyterHub.db_url = 'sqlite:////data/jupyterhub/jupyterhub.sqlite'
c.JupyterHub.cookie_secret_file = '/data/jupyterhub/jupyterhub_cookie_secret'

c.JupyterHub.authenticator_class = 'remote_user.remote_user_auth.RemoteUserAuthenticator'
c.RemoteUserAuthenticator.header_name = 'X-Forwarded-User'
c.JupyterHub.base_url = '/jupyterhub/'
c.JupyterHub.hub_prefix = '/jupyterhub/'

# Authenticate users with GitHub OAuth
# c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
# c.GitHubOAuthenticator.client_id = os.environ['GITHUB_CLIENT_ID']
# c.GitHubOAuthenticator.client_secret = os.environ['GITHUB_CLIENT_SECRET']
# c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Whitlelist users and admins
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True
pwd = os.path.dirname(__file__)
with open(os.path.join(pwd, '/data/jupyterhub/userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
