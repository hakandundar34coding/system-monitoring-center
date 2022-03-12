# Maintainer: Hakan Dündar <hakandundar34coding@gmail.com>
pkgname=system-monitoring-center
_pkgver=1.5.0
pkgver=${_pkgver//-/.}
pkgrel=1
pkgdesc="System performance and usage monitoring tool"
arch=('any')
url="https://github.com/hakandundar34coding/system-monitoring-center"
license=('GPL3')
depends=('bash' 'dmidecode' 'gtk3' 'hwdata' 'iproute2' 'mesa-utils'
         'python-cairo' 'python-gobject' 'systemd' 'util-linux')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$_pkgver.tar.gz")
sha256sums=('07418ae8b51bcdae9ed6afe68d99ff3c34acd480783a8e654548fa80a0d715b9')

build() {
  cd "$pkgname-$_pkgver"
  python setup.py build
}

package() {
  cd "$pkgname-$_pkgver"
  python setup.py install --root="$pkgdir" --optimize=1 --skip-build
}
