define ppa($team, $ppa) {
  exec {"add-ppa-$name":
    command => "add-apt-repository ppa:$team/$ppa",
    path => ['/usr/bin'],
    creates => "/etc/apt/sources.list.d/$team-$ppa-$lsbdistcodename.list",
    require => Package['python-software-properties'],
    notify => Exec['apt-get-update'],
  }

  exec {"ensure-apt-get-update-is-called-before-ppa-$name-is-used":
    command => '/bin/true',
    subscribe => Exec["add-ppa-$name"],
    require => Exec['apt-get-update'],
    refreshonly => true,
  }
}

exec {'apt-get-update':
  command => '/usr/bin/apt-get update',
  refreshonly => true,
}

package {'python-software-properties': ensure => installed}

ppa {'openpgm-backport':
  team => 'chris-lea',
  ppa => 'libpgm',
}

ppa {'zeromq-backport':
  team => 'chris-lea',
  ppa => 'zeromq',
}

package {'libzmq1':
  ensure => installed,
  require => [Ppa['zeromq-backport'], Ppa['openpgm-backport']],
}
package {'libzmq-dev':
  ensure=>installed,
  require => Ppa['zeromq-backport'],
}
package {'python-dev': ensure=>installed}
package {'python-setuptools': ensure=>installed}

exec {'install-pip':
  command => '/usr/bin/easy_install pip',
  creates => '/usr/local/bin/pip',
  require => Package['python-setuptools'],
}

exec {'install-virtualenv':
  command => '/usr/local/bin/pip install virtualenv',
  creates => '/usr/local/bin/virtualenv',
  require => Exec['install-pip'],
}

exec {'install-virtualenvwrapper':
  command => '/usr/local/bin/pip install virtualenvwrapper',
  creates => '/usr/local/bin/virtualenvwrapper.sh',
  require => [Exec['install-pip'], Exec['install-virtualenv']],
}
