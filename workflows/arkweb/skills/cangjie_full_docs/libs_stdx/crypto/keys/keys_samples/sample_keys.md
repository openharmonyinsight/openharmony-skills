# keys 使用

## RSA 密钥示例

### 生成 rsa 公钥及私钥，并使用公钥的 OAEP 填充模式加密，用私钥的 OAEP 填充模式解密

示例：

<!-- verify -->
```cangjie
import stdx.crypto.keys.*
import stdx.crypto.digest.*
import std.io.*
import std.crypto.digest.*

main() {
    var rsaPri = RSAPrivateKey(2048)
    var rsaPub = RSAPublicKey(rsaPri)

    var str: String = "hello world, hello cangjie"
    var bas1 = ByteBuffer()
    var bas2 = ByteBuffer()
    var bas3 = ByteBuffer()
    bas1.write(str.toArray())

    var encOpt = OAEPOption(SHA1(), SHA256())
    rsaPub.encrypt(bas1, bas2, padType: OAEP(encOpt))
    var encOpt2 = OAEPOption(SHA1(), SHA256())
    rsaPri.decrypt(bas2, bas3, padType: OAEP(encOpt2))

    var buf = Array<Byte>(str.size, repeat: 0)
    bas3.read(buf)
    if (str.toArray() == buf) {
        println("success")
    } else {
        println("fail")
    }
}
```

运行结果：

```text
success
```

### 从文件中读取 rsa 公钥和私钥，并使用私钥的 PKCS1 填充模式签名，用公钥的 PKCS1 填充模式验证签名结果

**说明：**
>
> - 需要自行准备公私钥文件。

示例：

<!-- compile -->
```cangjie
import stdx.crypto.keys.*
import stdx.crypto.digest.*
import std.crypto.digest.*
import std.fs.*
import std.io.*

main() {
    var pemPri = String.fromUtf8(readToEnd(File("./files/rsaPri.pem", Read)))
    var rsaPri = RSAPrivateKey.decodeFromPem(pemPri)

    var pemPub = String.fromUtf8(readToEnd(File("./files/rsaPub.pem", Read)))
    var rsaPub = RSAPublicKey.decodeFromPem(pemPub)

    var str: String = "helloworld"
    var sha512Instance = SHA512()
    sha512Instance.write(str.toArray())
    var md: Array<Byte> = sha512Instance.finish()

    var sig = rsaPri.sign(sha512Instance, md, padType: PKCS1)
    if (rsaPub.verify(sha512Instance, md, sig, padType: PKCS1)) {
        println("verify successful")
    }
}
```

运行结果：

```text
verify successful
```

## ECDSA 密钥示例

### 生成 ECDSA 公钥及私钥，并使用私钥签名，公钥验证签名结果

示例：

<!-- verify -->
```cangjie
import stdx.crypto.keys.*
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*

main() {
    var ecPri = ECDSAPrivateKey(P224)
    var ecPub = ECDSAPublicKey(ecPri)

    var str: String = "helloworld"
    var sha512Instance = SHA512()
    sha512Instance.write(str.toArray())
    var md: Array<Byte> = sha512Instance.finish()

    var sig = ecPri.sign(md)
    if (ecPub.verify(md, sig)) {
        println("verify successful")
    }
}
```

运行结果：

```text
verify successful
```

## SM2 密钥示例

### 生成 SM2 公钥及私钥，并使用私钥签名，公钥验证签名结果

示例：

<!-- verify -->
```cangjie
import stdx.crypto.keys.*
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import std.fs.*
import std.io.*

main(): Unit {
    /* 无参生成公钥私钥 */
    let sm2PrivateKey = SM2PrivateKey()
    let sm2PublicKey = SM2PublicKey(sm2PrivateKey)

    /* 公钥和私钥导出 */
    let priPem = sm2PrivateKey.encodeToPem()
    let file1: File = File("./sm2Pri.pem", Write)
    file1.write(priPem.encode().toArray())
    file1.close()

    let pubPem = sm2PublicKey.encodeToPem()
    let file2: File = File("./sm2Pub.pem", Write)
    file2.write(pubPem.encode().toArray())
    file2.close()

    /* 公钥加密，私钥解密 */
    let str: String = "helloworld"
    let encresult = sm2PublicKey.encrypt(str.toArray())
    let decresult = sm2PrivateKey.decrypt(encresult)
    println(String.fromUtf8(decresult))

    /* 私钥签名，公钥验证 */
    let strSig: String = "helloworld"
    let sigRe = sm2PrivateKey.sign(strSig.toArray())
    let verifyre = sm2PublicKey.verify(strSig.toArray(), sigRe)
    println(verifyre)

    /* 私钥公钥导入 */
    let pemPri = String.fromUtf8(readToEnd(File("./sm2Pri.pem", Read)))
    let sm2PrivateKeyNew = SM2PrivateKey.decodeFromPem(pemPri)
    println(sm2PrivateKeyNew)
    let pemPub = String.fromUtf8(readToEnd(File("./sm2Pub.pem", Read)))
    let sm2PublicKeyNew = SM2PublicKey.decodeFromPem(pemPub)
    println(sm2PublicKeyNew)
}
```

运行结果：

```text
helloworld
true
SM2 PRIVATE KEY
SM2 PUBLIC KEY
```
