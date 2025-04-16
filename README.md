# 华为手机固件包解包解包工具
##  说明：
-  华为的安卓系统固件包（即 harmonyOS 5 以前）使用的是 update.app 格式，可以使用 HuaweiUpdateExtractor 进行解包，获得各分区镜像。
-  从 harmonyOS 5 开始，华为固件包开始使用新的 update.bin 格式。这种格式无法用 HuaweiUpdateExtractor 解包。通过用十六进制查看 update.bin，发现是标准的 openharmony 升级包格式。
-  虽然官方的 [update_packaging_tools 库](https://gitee.com/openharmony/update_packaging_tools) 中提供了一个名为 unpack_update_package.py 的解包程序，但是直接运行不会有任何效果，仅仅只会生成一个包含 pyc 程序的__pycache__文件夹。即使在程序结尾添加上主程序，使其能正常运行，但是当解包到特大分区（system.img，>1G）时，会发生数据偏移值解析错误的问题，导致解包出的img远小于实际值。
-  经过对官方代码的阅读，解析了 update.bin 格式的数据结构，用 python 简单写了解包程序，即 unpack_huawei_package.py。本程序无须安装任何依赖库。若不希望安装 python ，本项目额外提供了可直接运行的 exe 程序。
-  使用过程中需要将 update.bin 与本程序放在同一目录下。也可以自行修改 unpack_huawei_package.py 第5行的 update.bin 文件路径。
