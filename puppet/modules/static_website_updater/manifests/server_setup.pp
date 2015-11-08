class static_website_updater::server_setup {
  file {
    "/etc/init.d/static_website_updater":
      ensure  => present,
      owner   => root,
      group   => root,
      mode    => '0755',
      content => template('static_website_updater/initd_script.erb')
  }

  exec {
    "update-rc.d":
      command => "update-rc.d static_website_updater defaults",
      path => "/usr/sbin:/usr/bin",
      require => File["/etc/init.d/static_website_updater"]
  }
}