# Copyright (C) 2012 Oscar Campos <oscar.campos@member.fsf.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import with_statement
from fabric.api import env, run, hosts, cd

import settings

@hosts(settings.nodes)
def deploy_MySQL_nodes():
    """
    Deply a MySQL node on node hosts
    """
    if env.get('host') not in settings.nodes:
        return

    run('mv /tmp/mysql-cluster-gpl-7.2.4-linux2.6-x86_64/* %s' % (settings.mysql_dir))

    run('scripts/mysql_install_db --user=mysql --no-defaults')

    run('chown -R root .')
    run('chown -R mysql data')
    run('chgrp -R mysql .')

    run('sed -i "s/usr\/local/var\/lib/" support-files/mysql.server')
    run('cp support-files/mysql.server /etc/rc.d/init.d/')
    run('chmod +x /etc/rc.d/init.d/mysql.server')
    run('chkconfig --add mysql.server')


def deploy():
    """
    Prepare CentOS for deployment
    """
    run('yum -y install wget')
    run('yum -y install libaio')

    run('mkdir -p %s' % (settings.mysql_dir))
    run('groupadd mysql')
    run('useradd -d %s -r -g mysql mysql' % (settings.mysql_dir))    
    with cd(settings.mysql_dir):
        run('wget %s' % settings.download_url)
        run('tar -C /tmp -xzvf mysql-cluster-gpl-7.2.4-linux2.6-x86_64.tar.gz')
        deploy_MySQL_master()
        deploy_MySQL_nodes()
        run('echo "export PATH=\"${PATH}:/%s/bin\"" >> ${HOME}/.bashrc' % (settings.mysql_dir))
        run('export PATH="${PATH}:/%s/bin"')
        run('rm -Rf /tmp/mysql-cluster-gpl-7.2.4-linux2.6-x86_64')
        run('rm -Rf %s/mysql-cluster-gpl-7.2.4-linux2.6-x86_64.tar.gz' % (settings.mysql_dir))
        
        run('echo "%s" > /etc/my.cnf' % (settings.my_cnf))
        run('echo "%s" > %s/config.ini' % (settings.config_ini, settings.mysql_dir))


def deploy_MySQL_master():
    """
    Deploy the MySQL NDB Manager at master host only
    """

    if env.get('host') != settings.master:
        return
    
    run('mkdir -p %s/bin' % (settings.mysql_dir))
    run('mv /tmp/mysql-cluster-gpl-7.2.4-linux2.6-x86_64/bin/ndb_mgm* %s/bin/' % (settings.mysql_dir))
    run('mkdir %s/data')
    run('mkdir %s/mysql-cluster' % (settings.mysql_dir))
    run('chown -R mysql %s/data' % (settings.mysql_dir))
    run('chgrp -R mysql %s' % (settings.mysql_dir))

