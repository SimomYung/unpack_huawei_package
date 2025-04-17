# 华为手机固件包解包工具
## 1.介绍:
- 华为安卓系统包 (harmonyOS 5 之前) 使用 update.app 格式。这种格式可以用 HuaweiUpdateExtractor 解包获得所有分区镜像.
- 从 harmonyOS 5 开始, 华为固件包开始使用新的 update.bin 格式。这种格式无法使用 HuaweiUpdateExtractor 解包。用十六进制编辑器打开，可以发现是标准的 openharmony 升级包格式。
- 尽管 openharmony 提供了解包工具[update_packaging_tools library](https://gitee.com/openharmony/update_packaging_tools)， 但是运行后并不会有任何效果。虽然在代码后加入主程序后可以正常运行，但是当分区大小特别大时(system.img，>1G)，会发生数据偏移值解析错误，导致解包镜像大小远小于实际值。
- 在阅读官方代码后，我用python写了 unpack_huawei_package.py。本项目无需安装任何依赖。如果你不想安装python，本项目额外提供了可直接运行的exe程序。
- 你需要将 update.bin 与程序放在同一目录下。你也可以通过修改 unpack_huawei_package.py 第5行指定 update.bin 文件路径。
## 2.update.bin 文件结构解析:
- update.bin 有两种型式，分别为 L2 和非 L2。harmonyOS 5 使用的是 L2 型，所以只解析 L2 型结构。
- 开头的 178 B 是文件头，包含版本和构建时间信息。
- 接下来的 2 B 是一个长度为 4 的小端序，表示分区信息的总长度。
- 分区信息的长度有2种版本。
- (1) L2 型每个分区信息长度是 87 B。48-55 共 8 B 是16位十六进制小端序，表示每个分区的长度。最后的 32 B 是 GUID 和 UUID。
- (2) 非 L2 型每个分区信息长度为 71 B。
- 根据每个分区信息的长度，你可以很快地判断你的 update.bin 是否是 L2 格式。你可以用 [Hexadecimal Editor](http://wxmedit.github.io/zh_CN/downloads.html)打开文件，如果每个分区信息长度为 87 B，即两个"/"之间间隔 87 B，则为 L2 型，反之为非 L2 型。
- 接下来的 16 B 为固定内容"update/info.bin "。
- 紧跟的 2 B 是长度为4的十六进制小端序，决定了接下来的签名要如何处理。
- (1)如果为"08"，则直接读取接下来的 4 B ，表示的是oem签名的长度。
- 数据起始偏移值 = 178 + 2 + 分区信息长度 + 16 + 2 + 4 + 签名长度
- (2)如果为"06"，则需要跳过 16 B，再读取 4 B 数据，即oem签名长度。
- 数据起始偏移量 = 178 + 2 + 分区信息长度 + 16 + 2 + 16 + 4 + 签名长度
