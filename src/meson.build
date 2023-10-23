pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'systemmonitoringcenter')

'''gnome.compile_resources(meson.project_name(),
    meson.project_name() + '.gresource.xml',
    gresource_bundle: true,
    install: true,
    install_dir: pkgdatadir,
)'''

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation().full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
    input: meson.project_name() + '.in',
    output: meson.project_name(),
    configuration: conf,
    install: true,
    install_dir: get_option('bindir')
)

system_monitoring_center_sources = [
    '__init__.py',
    'Common.py',
    'Config.py',
    'Cpu.py',
    'CpuMenu.py',
    'Disk.py',
    'DiskMenu.py',
    'Gpu.py',
    'GpuMenu.py',
    'Libsysmon.py',
    'Main.py',
    'MainWindow.py',
    'Memory.py',
    'MemoryMenu.py',
    'Network.py',
    'NetworkMenu.py',
    'Performance.py',
    'Processes.py',
    'ProcessesDetails.py',
    'ProcessesMenu.py',
    'Sensors.py',
    'SensorsMenu.py',
    'Services.py',
    'ServicesDetails.py',
    'ServicesMenu.py',
    'SettingsWindow.py',
    'Summary.py',
    'SummaryMenu.py',
    'System.py',
    'Users.py',
    'UsersDetails.py',
    'UsersMenu.py',
    '__version__',
]

install_data(system_monitoring_center_sources, install_dir: moduledir)
