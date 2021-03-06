# 使用说明 (Web App Template SDK)

## 通过`Access Key`访问

第三方系统可以通过`Access Key ID`和`Access Secret`（`AK`）访问本Web APP.

### 1. 生成`AK`

`AK`可以在[Access Key management page](/access-keys)页面生成。

### 2. 对请求进行签名

对请求进行签名需要以下字段：

|       字段      |                       描述                      |                示例                |
|-----------------|-------------------------------------------------|------------------------------------|
| AK时间戳        | 当前UNIX时间戳（秒）                            | `1527532323`                       |
| AK随机数        | 一个随机字符串                                  | `0.15029408624960117`              |
| HTTP方法        | 全大写HTTP方法                                  | `POST`                             |
| 完整请求URL     | 请求URL（包含Quey参数）                         | `/api/v1/path?a=1&b=2`             |
| AK签名算法版本  | `v2`新增字段。`v1`不用传递                      | `v2`                               |
| 原始请求体MD5值 | `v2`新增字段。无请求体的以空字符串`''`计算MD5值 | `d41d8cd98f00b204e9800998ecf8427e` |

目前支持`v1`和`v2`两种签名算法：

1. `v1`签名为:

`Hmac-SHA1("<AK时间戳>&<AK随机数>&<HTTP方法>&<完整请求URL>", <AK Secret>)`

2. `v2`签名为:

`Hmac-SHA1("<AK签名算法版本>&<AK时间戳>&<AK随机数>&<HTTP方法>&<完整请求URL>&<原始请求体MD5值>", <AK Secret>)`

### 3. 将签名信息加入请求头

|         请求头          |                    描述                    |                    示例                    |
|-------------------------|--------------------------------------------|--------------------------------------------|
| `X-Wat-Ak-Id`           | Access Key ID                              | `ak-abcde12345`                            |
| `X-Wat-Ak-Timestamp`    | 签名时所使用的UNIX时间戳                   | `1527532323`                               |
| `X-Wat-Ak-Nonce`        | 签名时所使用的随机字符串                   | `0.15029408624960117`                      |
| `X-Wat-Ak-Sign`         | 签名结果                                   | `431f70c44d5f7c97dcc87c20060e2480acdf3a04` |
| `X-Wat-Ak-Sign-Version` | AK签名算法版本。`v2`新增字段，`v1`不用传递 | `v2`                                       |

#### 自定义签名用的HTTP请求头

使用`Header Fields`选项，可以将签名信息附带在指定的HTTP 请求头中：

- Python:
```python
header_fields = {
    'akSignVersion': 'X-Custom-Header-For-Ak-Sign-Version',
    'akId'         : 'X-Custom-Header-For-Ak-Id',
    'akTimestamp'  : 'X-Custom-Header-For-Ak-Timestamp',
    'akNonce'      : 'X-Custom-Header-For-Ak-Nonce',
    'akSign'       : 'X-Custom-Header-For-Ak-Sign',
}
client = WATClient(host=host, ak_id=ak_id, ak_secret=ak_secret, header_fields=header_fields)
```

- Javascript:
```javascript
var watClient = new WATClient({
  akId         : akId,
  akSecret     : akSecret,
  akSignVersion: akSignVersion,
  headerFields: {
    akSignVersion: 'X-Custom-Header-For-Ak-Sign-Version',
    akId         : 'X-Custom-Header-For-Ak-Id',
    akTimestamp  : 'X-Custom-Header-For-Ak-Timestamp',
    akNonce      : 'X-Custom-Header-For-Ak-Nonce',
    akSign       : 'X-Custom-Header-For-Ak-Sign',
  }
});
```

### 4. 发送请求

至此，发送请求即可

## 可用资源

下面是已经实现的HTTP客户端：

| 编程语言 |     文件地址     |                                    描述                                    |
|----------|------------------|----------------------------------------------------------------------------|
| Python   | `sdk/wat_sdk.py` | 无依赖、支持所有操作。 兼容Python 2.6 ～ 3.7。（文件上传依赖`requests`包） |
| Node.js  | `sdk/wat_sdk.js` | 无依赖、无需编译。（文件上传依赖`form-data`包）                            |
