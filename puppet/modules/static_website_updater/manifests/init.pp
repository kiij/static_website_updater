class static_website_updater (
  $working_directory = '/srv',
  $source = 'git',
  $install = true
){

  exec { "apt-get update":
    path => "/usr/bin"
  }

  package { ["git", "python-pip"]:
    ensure => present,
    provider => apt,
    require => Exec["apt-get update"]
  }

  # Ruby

  exec { "rvm.gpg2":
    command => "gpg --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3",
    path => "/usr/bin"
  }

  class {
    '::rvm':
      gnupg_key_id => false,
      require => Exec["rvm.gpg2"]
  }

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

  file {
    $working_directory:
      ensure => "directory",
  }

  if $install {
    case $source {
      'git': {
        exec {
          "static_website_updater.download":
            path    => "/usr/bin",
            cwd     => $working_directory,
            command => "git clone https://github.com/kiij/static_website_updater.git",
            require => [
              Package["git"],
              File[$working_directory]
            ],
        }
      }
    }

    exec {
      "static_website_updater.install":
        path    => "/usr/bin",
        cwd     => "${working_directory}/static_website_updater",
        command => "python setup.py install",
        require => [
          Package["python-pip"],
          Exec["static_website_updater.download"]
        ],
    }
  }

}
