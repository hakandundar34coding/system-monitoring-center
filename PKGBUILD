# Maintainer: Hakan Dündar <hakandundar34coding@gmail.com>
pkgname=system-monitoring-center
_pkgver=0.2.0-beta1
pkgver=${_pkgver//-/.}
pkgrel=1
pkgdesc="System performance and usage monitoring tool"
arch=('x86_64')
url="https://github.com/hakandundar34coding/system-monitoring-center"
license=('GPL3')
depends=('bash' 'dmidecode' 'gtk3' 'hwids' 'libwnck3' 'mesa-demos' 'python-cairo'
         'python-gobject' 'python-opengl' 'systemd' 'util-linux')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$_pkgver.tar.gz")
sha256sums=('97d3a8de141347b7c25a005aba9861b15441a20fa5a779d135bf5f35d693a839')

build() {
  cd "$pkgname-$_pkgver"
  python setup.py build
}

package() {
  cd "$pkgname-$_pkgver"
  python setup.py install --root="$pkgdir" --optimize=1 --skip-build
}
