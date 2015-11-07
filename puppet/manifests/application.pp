import "dependencies.pp"

$working_directory = "/srv"

file {
  $working_directory:
    ensure => "directory",
}

exec {
  "git.clone application":
    path => "/usr/bin",
    cwd => $working_directory,
    command => "git clone https://github.com/kiij/static_website_updater.git",
    require => [
      Package["git"],
      File[$working_directory]
    ],
}

exec {
  "install application":
    path => "/usr/bin",
    cwd => "${working_directory}/static_website_updater",
    command => "python setup.py install",
    require => [
      Package["python-pip"],
      Exec["git.clone application"]
    ],
}
