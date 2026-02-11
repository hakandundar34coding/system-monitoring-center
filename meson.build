project('system-monitoring-center',
    version: files('src/__version__'),
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')


subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
