import multiprocessing
from . import app_config
from . import orion


# -- Configuration defaults --
# Debugging
# reload = false
# reload_engine = 'auto'
# reload_extra_files = []
# spew = False
# check_config = False
# print_config = False

# Logging
# accesslog = None
# disable_redirect_access_to_syslog = False
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
# errorlog = '-'
# loglevel = 'info'
# capture_output = False
# logger_class = 'gunicorn.glogging.Logger'
# logconfig = None

logconfig = './configuration/logging.conf'

# logconfig_dict = {}
# syslog_addr = 'udp://localhost:514'
# syslog = False
# syslog_prefix = None
# syslog_facility = 'user'
# enable_stdio_inheritance = False
# statsd_host = None
# dogstatsd_tags = ''
# statsd_prefix = ''

# Process Naming
# proc_name = None
# default_proc_name = 'gunicorn'

# SSL
# keyfile = None
# certfile = None
# ssl_version = <_SSLMethod.PROTOCOL_TLS: 2>
# cert_reqs = <VerifyMode.CERT_NONE: 0>
# ca_certs = None
# suppress_ragged_eofs = True
# do_handshake_on_connect = False
# ciphers = None

# Security
# limit_request_line = 4094
# limit_request_fields = 100
# limit_request_field_size = 8190


# Server Hooks
def on_starting(server):
    orion.purge_subscriptions()
    orion.configure_entity_sub()
    pass


# def on_reload(server):
#     pass
#
# def when_ready(server):
#     pass
#
# def pre_fork(server, worker):
#     pass
#
# def post_fork(server, worker):
#     pass
#
# def post_worker_init(worker):
#     pass
#
# def worker_init(worker):
#     pass
#
# def worker_abort(worker):
#     pass
#
# def pre_exec(server):
#     pass
#
# def pre_request(worker, req):
#     worker.log.debug("%s %s" % (req.method, req.path))
#
# def post_request(worker, req, environ, resp):
#     pass
#
# def child_exit(server, worker):
#     pass
#
# def worker_exit(server, worker):
#     pass
#
# def nworkers_changed(server, new_value, old_value):
#     pass
#
# def on_exit(server):
#     pass

# Server Mechanics
# preload_app = False
# sendfile = None
# reuse_port = False
# chdir = '/home/docs/checkouts/readthedocs.org/user_builds/gunicorn-docs/checkouts/latest/docs/source'
# daemon = False
# raw_env = []
# pidfile = None
# worker_tmp_dir = None
# user = 1005
# group = 205
# umask = 0
# initgroups = False
# tmp_upload_dir = None
# secure_scheme_headers = {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}
# forwarded_allow_ips = '127.0.0.1'
# pythonpath = None
# paste = None
# proxy_protocol = False
# proxy_allow_ips = '127.0.0.1'
# raw_paste_global_conf = []
# strip_header_spaces = False

# Server Socket
# bind = ['127.0.0.1:8000']

bind = ['0.0.0.0:{}'.format(app_config.host_port)]

# backlog = 2048

# Worker Processes
# workers = 1

workers = multiprocessing.cpu_count() * 2 + 1

# worker_class = 'sync'
# threads = 1
# worker_connections = 1000
# max_requests = 0
# max_requests_jitter = 0
# timeout = 30
# graceful_timeout = 30
# keepalive = 2

