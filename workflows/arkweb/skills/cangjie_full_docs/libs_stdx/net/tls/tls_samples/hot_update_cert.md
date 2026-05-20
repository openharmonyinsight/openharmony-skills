# 证书热更新

示例：

<!-- run -->
```cangjie
import std.net.StreamingSocket
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import stdx.net.tls.*

class MyServer {
    private var currentConfig: TlsServerConfig

    init(initialConfig: TlsServerConfig) {
        currentConfig = initialConfig
    }

    // 更改带有密钥的证书只会影响新的连接
    public mut prop certificate: ?(Array<X509Certificate>, PrivateKey) {
        get() {
            currentConfig.serverCertificate
        }
        set(newCertificate) {
            currentConfig.serverCertificate = newCertificate
        }
    }

    public func onAcceptedConnection(client: StreamingSocket) {
        try (tls = TlsSocket.server(client, serverConfig: currentConfig)) {
            tls.handshake()
        }
    }
}

main() {}
```
