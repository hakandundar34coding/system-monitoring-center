# Maintainer: Hakan Dündar <hakandundar34coding@gmail.com>
pkgname=system-monitoring-center
_pkgver=1.1.0
pkgver=${_pkgver//-/.}
pkgrel=1
pkgdesc="System performance and usage monitoring tool"
arch=('any')
url="https://github.com/hakandundar34coding/system-monitoring-center"
license=('GPL3')
depends=('bash' 'dmidecode' 'gtk3' 'hwids' 'iproute2' 'mesa-demos'
         'python-cairo' 'python-gobject' 'python-opengl' 'systemd' 'util-linux')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$_pkgver.tar.gz")
sha256sums=('201b4b2cb5b525336e50dbdbdbd737f987d828f56cd9e98417812fa86b37f5ab')

build() {
  cd "$pkgname-$_pkgver"
  python setup.py build
}

package() {
  cd "$pkgname-$_pkgver"
  python setup.py install --root="$pkgdir" --optimize=1 --skip-build
}
