$share = '/tmp/vagrant-share'
$downloads = "$share/downloads"

define wget($source) {
  $destination = "$downloads/$name"
  exec {"/usr/bin/wget --output-document=$destination $source/$name":
    creates => $destination,
  }
}

define repo() {
  file {"$name.list":
    path => "/etc/apt/sources.list.d/$name.list",
    source => "$share/$name.list",
    notify => Exec['apt-get-update']
  }

  exec {'ensure-apt-get-update-is-called-before-$name-is-used':
    command => '/bin/true',
    subscribe => File["$name.list"],
    require => Exec['apt-get-update'],
    refreshonly => true,
  }
}

exec {'apt-get-update':
  command => '/usr/bin/apt-get update',
  refreshonly => true,
}

group {"puppet":
  ensure => "present",
}

repo {'lucid-partner': }

package {'git-core':
  ensure => installed,
}

package {'sun-java6-jdk':
  ensure => installed,
  responsefile => "$share/sun-java-licence.seeds",
  require => Repo['lucid-partner'],
}

package {'unzip':
  ensure => installed,
}

$go_server_package = 'go-server-2.3.0-14056.deb'
wget {$go_server_package:
  source => 'http://download01.thoughtworks.com/go/2.3/ga',
}

$go_agent_package = 'go-agent-2.3.0-14056.deb'
wget {$go_agent_package:
  source => 'http://download01.thoughtworks.com/go/2.3/ga',
}

package {'go-server':
  ensure => installed,
  provider => dpkg,
  source => "$downloads/$go_server_package",
  require => [Wget[$go_server_package], Package['sun-java6-jdk'], Package['unzip']],
}

package {'go-agent':
  ensure => installed,
  provider => dpkg,
  source => "$downloads/$go_agent_package",
  require => [Wget[$go_agent_package], Package['sun-java6-jdk']],
  notify => Service['go-agent'],
}

service {'go-server':
  enable => true,
  ensure => running,
  hasstatus => true,
  hasrestart => true,
  require => Package['go-server'],
}

service {'go-agent':
  enable => true,
  ensure => running,
  hasstatus => true,
  hasrestart => true,
  require => Package['go-agent'],
}

file {'go-config':
  ensure => link,
  path => '/etc/go/cruise-config.xml',
  target => '/tmp/vagrant-share/cruise-config.xml',
  owner => go,
  group => go,
  notify => Service['go-server'],
  require => Package['go-server'],
}
