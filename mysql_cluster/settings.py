def get_nodes():
  ret = []
  for node in nodes:
    ret.append('''[ndbd]
# Options for data node "%s":
hostname=%s                     # Hostname or IP address
datadir=%s/data                 # Directory for this data node's data files
''' % (node, node, mysql_dir))

  return ''.join(ret)

nodes = ['146.255.97.178', '146.255.97.179', '146.255.97.180', '146.255.97.181']
master = '146.255.97.182'
download_url = 'http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.4-linux2.6-x86_64.tar.gz/from/http://mysql.llarian.net/'
mysql_dir = '/var/lib/mysql'
data_memory = '80M'
index_memory = '18M'
port = '2202'
my_cnf = '''[mysqld]
# Options for mysqld process:
ndbcluster						# run NDB storage engine
datadir=%s/data
basedir=/%s
port=5000
''' % (mysql_dir, mysql_dir)
config_ini='''[nbdb default]
# Options affecting nbdb processes on all data nodes:
NoOfReplicas=%s   # Number of replicas
DataMemory=%s     # How much memory to allocate for data storage
IndexMemory=%s    # How much memory to allocate for index storage
                  # For DataMemory and IndexMemory, we have used the
                  # default values. Since the "world" database takes up
                  # only about 500KB, this should be more than enough for
                  # this example Cluster setup.
datadir=%s/data

[ndb_mgmd]
# Management process options:
hostname=%s                     # Hostname or IP address of MGM node
datadir=%s/data  # Directory for MGM node log files

# Nodes
%s

[mysqld]
# SQL node options:
nodeID=50
''' % (len(nodes), data_memory, index_memory, mysql_dir, master, mysql_dir, get_nodes())
