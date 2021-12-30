# Maintainer: Hakan Dündar <hakandundar34coding@gmail.com>
pkgname=system-monitoring-center
_pkgver=0.3.2-beta1
pkgver=${_pkgver//-/.}
pkgrel=1
pkgdesc="System performance and usage monitoring tool"
arch=('x86_64')
url="https://github.com/hakandundar34coding/system-monitoring-center"
license=('GPL3')
depends=('bash' 'dmidecode' 'gtk3' 'hwids' 'iproute2' 'mesa-demos'
         'python-cairo' 'python-gobject' 'python-opengl' 'systemd' 'util-linux')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$_pkgver.tar.gz")
sha256sums=('c081f0297d826895a426ec10da308326831bd824f9f8551fd090924a9be245a7')

build() {
  cd "$pkgname-$_pkgver"
  python setup.py build
}

package() {
  cd "$pkgname-$_pkgver"
  python setup.py install --root="$pkgdir" --optimize=1 --skip-build
}
