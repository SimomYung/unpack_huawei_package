# 华为手机固件包解包工具
## 1.介绍:
- 华为安卓系统包 (harmonyOS 5 之前) 使用 update.app 格式。这种格式可以用 HuaweiUpdateExtractor 解包获得所有分区镜像.
- 从 harmonyOS 5 开始, 华为固件包开始使用新的 update.bin 格式。这种格式无法使用 HuaweiUpdateExtractor 解包。Looking at the update.bin in hexadecimal format, it was found to be the standard OpenHarmony upgrade package format.
- Although the official [update_packaging_tools library](https://gitee.com/openharmony/update_packaging_tools) provides an unpacker called unpack_update_package.py, running it directly will have no effect, and will only generate a __pycache__ containing the pyc program Folder. Even if the main program is added at the end of the program to make it run normally, when unpacking to a very large partition (system.img, >1G), the data offset value will be parsed incorrectly, resulting in the unwrapped img being much smaller than the actual value.
- After reading the official code, I use python write unpack_huawei_package.py. This program does not require any dependencies to be installed. If you don't want to install python, this project provides an additional exe program that can be run directly.
- You need to put update.bin in the same directory as this program. You can also modify the update.bin file path on line 5 of unpack_huawei_package.py yourself.
## 2.update.bin 文件结构解析:
- update.bin There are two formats, L2 and non-L2. harmonyOS 5 uses the L2 format, so only the L2 format is parsed.
- The first 178 B is the file header, indicating the version information and build time.
- The next 2 B is a hexadecimal little-endian of length 4, which represents the length of the partition information.
- The length of partition information varies depending on the type.
- (1)The information of each partition of the L2 type is 87 B long. 48-55 of 8 B is a 16-bit hexadecimal little-endian order, which indicates the size of the partition. The last 32 B's are GUID and UUID, respectively.
- (2) The information for each partition of the non-L2 type is 71 B long.
- Based on the length of the partition information, you can quickly determine whether the update.bin is L2. If you open a file with the [Hexadecimal Editor](http://wxmedit.github.io/zh_CN/downloads.html), if the length of each partition information is 87 B, that is, the interval between every two "/" is 87 hexadecimal numbers, it is L2. The opposite is non-L2.
- This is followed by 16 B fixed content with "update/info.bin"
- The next 2 B is a hexadecimal little-endian of length 4, which indicates the type of signature and determines what is done next.
- (1)If it is "08", the next 4 B data is read, which is the OEM signature length.
- Data start offset value: 178 + 2 + partition information length + 16 + 2 + 4 + signature length
- (2) If it is "06", skip 16 B and read the next 4 B data, that is, the OEM signature length.
- Data start offset value: 178 + 2 + partition information length + 16 + 2 + 16 + 4 + signature length
