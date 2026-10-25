pkgname=mailfetch
pkgver=1.0.0
pkgrel=1
pkgdesc="Fastfetch-style system information summary for Linux terminals"
arch=('any')
url="https://github.com/mailcatx/mailfetch"
depends=('python' 'pciutils')
source=()

package() {
    install -Dm755 "$startdir/main.py" "$pkgdir/usr/bin/mailfetch"
}
