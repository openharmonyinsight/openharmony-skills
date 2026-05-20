# 服务端示例

> **说明：**
>
> 需要自行准备证书文件。

示例：

<!-- compile -->
```cangjie
import std.io.*
import std.fs.{File, OpenMode}
import std.net.{TcpServerSocket, TcpSocket}
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import stdx.net.tls.*

// 证书及私钥路径，用户需自备
let certificatePath = "./files/apiserver.crt"
let certificateKeyPath = "./files/apiserver.key"

main() {
    // 对证书以及私钥进行解析
    let pem = readTextFromFile(certificatePath)
    let keyText = readTextFromFile(certificateKeyPath)

    let certificate = X509Certificate.decodeFromPem(pem)
    let privateKey = PrivateKey.decodeFromPem(keyText)

    let config = TlsServerConfig(certificate, privateKey)

    // 可选：允许恢复 TLS 会话
    let sessions = TlsSessionContext.fromName("my-server")

    try (server = TcpServerSocket(bindAt: 8443)) {
        server.bind()

        server.acceptLoop {
            clientSocket => try (tls = TlsSocket.server(clientSocket, serverConfig: config, sessionContext: sessions)) {
                tls.handshake()
                let buffer = Array<Byte>(100, repeat: 0)
                tls.read(buffer)
                println(buffer)
            }
        }
    }
}

extend TcpServerSocket {
    func acceptLoop(handler: (TcpSocket) -> Unit) {
        while (true) {
            let client = accept()
            spawn {
                try {
                    handler(client)
                } finally {
                    client.close()
                }
            }
        }
    }
}

func readTextFromFile(path: String): String {
    var str = ""
    try (file = File(path, Read)) {
        str = String.fromUtf8(readToEnd(file))
    }
    str
}
```
