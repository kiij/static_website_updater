# Misc packages

exec { "apt-get update":
  path => "/usr/bin",
}

package { ["git", "python-pip"]:
  ensure => present,
  provider => apt,
  require => Exec["apt-get update"],
}

# Ruby

class { '::rvm': }

rvm_system_ruby {
  'ruby-2.0':
    ensure => 'present',
    default_use => true;
}

rvm_gem {
  'bundler':
    name => 'bundler',
    ruby_version => 'ruby-2.0',
    ensure => latest,
    require => Rvm_system_ruby['ruby-2.0'];
}

# Jekyll gems

rvm_gem {
  'jekyll':
    name => 'jekyll',
    ruby_version => 'ruby-2.0',
    ensure => latest,
    require => Rvm_system_ruby['ruby-2.0'];
}

rvm_gem {
  'jekyll-paginate':
    name => 'jekyll-paginate',
    ruby_version => 'ruby-2.0',
    ensure => latest,
    require => Rvm_system_ruby['ruby-2.0'];
}
