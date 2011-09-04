$share = '/tmp/vagrant-share'
$downloads = "$share/downloads"

define wget($source) {
  $destination = "$downloads/$name"
  exec { "/usr/bin/wget --output-document=$destination $source/$name":
    creates => $destination,
  }
}

define repo() {
  file { "$name.list":
    path => "/etc/apt/sources.list.d/$name.list",
    source => "$share/$name.list",
    notify => Exec['apt-get-update']
  }

  exec { 'ensure-apt-get-update-is-called-before-the-repo-is-used':
    command => '/bin/true',
    subscribe => File["$name.list"],
    require => Exec['apt-get-update'],
    refreshonly => true,
  }
}

exec { 'apt-get-update':
  command => '/usr/bin/apt-get update',
  refreshonly => true,
}

group { "puppet":
  ensure => "present",
}

$go_package = 'go-server-2.3.0-14056.deb'
wget { $go_package:
  source => 'http://download01.thoughtworks.com/go/2.3/ga',
}

package {'unzip':
  ensure => installed,
}

package { 'go-server':
  ensure => installed,
  provider => dpkg,
  source => "$downloads/$go_package",
  require => [Wget[$go_package], Package['sun-java6-jdk'], Package['unzip']],
}

package {'sun-java6-jdk':
  ensure => installed,
  responsefile => "$share/sun-java-licence.seeds",
  require => Repo['lucid-partner'],
}

service {'go-server':
  enable => true,
  ensure => running,
  hasstatus => true,
  hasrestart => true,
  require => Package['go-server'],
}

repo {'lucid-partner': }

package {'git-core':
  ensure => installed,
}
