# Maintainer: Hakan Dündar <hakandundar34coding@gmail.com>
pkgname=system-monitoring-center
_pkgver=1.29.0
pkgver=${_pkgver//-/.}
pkgrel=1
pkgdesc="Multi-featured system monitor."
arch=('any')
url="https://github.com/hakandundar34coding/system-monitoring-center"
license=('GPL3')
depends=('bash' 'dmidecode' 'gtk3' 'iproute2' 'polkit'
         'python-cairo' 'python-gobject' 'systemd' 'util-linux')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$_pkgver.tar.gz")
sha256sums=('7470b4f1c00f64b967cdec05877d06559c32a7c95157e846d7f60d4011f0bcbb')

build() {
  cd "$pkgname-$_pkgver"
  python setup.py build
}

package() {
  cd "$pkgname-$_pkgver"
  python setup.py install --root="$pkgdir" --optimize=1 --skip-build
}
