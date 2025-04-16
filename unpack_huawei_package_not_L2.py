import os
import struct

# 输入的二进制文件路径
input_file_path = "update.bin"
# 分块大小，可根据实际情况调整
chunk_size = 1024 * 1024  # 1MB
components = []

try:
    # 获取输入文件的大小
    input_file_size = os.path.getsize(input_file_path)

    # 打开输入的二进制文件
    with open(input_file_path, 'rb') as input_file:
        COMPINFO_LEN_OFFSET = 178
        input_file.seek(COMPINFO_LEN_OFFSET)
        compinfo_len_buffer = input_file.read(2)     #读取分区信息大小
        compinfo_all_size = struct.unpack("H", compinfo_len_buffer)[0]

        input_file.seek(COMPINFO_LEN_OFFSET + 2 + compinfo_all_size + 16)    #读取签名大小
        compinfo_len_buffer = input_file.read(2)
        type2 = struct.unpack("H", compinfo_len_buffer)[0]
        if type2 == 0x08:
            hashdata_len_buffer = input_file.read(4)
            hashdata_size = struct.unpack("I", hashdata_len_buffer)[0]
            data_start_offset = COMPINFO_LEN_OFFSET + 2 + compinfo_all_size + 16 + 2 + 4 + hashdata_size
        elif type2 == 0x06:
            hashdata_len_buffer = input_file.read(16)
            hashdata_len_buffer = input_file.read(4)
            hashdata_size = struct.unpack("I", hashdata_len_buffer)[0]
            data_start_offset = COMPINFO_LEN_OFFSET + 2 + compinfo_all_size + 16 + 18 + 4 + hashdata_size

        component_count = compinfo_all_size / 71
        count = 1
        OFFSET = COMPINFO_LEN_OFFSET + 2
        while count <= component_count:
            if count >1:
                data_start_offset += component_size
            input_file.seek(OFFSET)
            component_info = input_file.read(71)
            component_name = component_info.split(b"\x00")[0].decode('utf-8')
            component_name += ".img"
            component_name = component_name.lstrip("/")
            OFFSET += 31
            input_file.seek(OFFSET)
            component_info = input_file.read(8)    #读取分区大小
            component_size = struct.unpack("Q", component_info)[0]
            OFFSET += 40
            count += 1
            dict={}
            dict["name"] = component_name
            dict["offset"] = data_start_offset
            dict["size"] = component_size
            components.append(dict)
        
        for component in components:
            name = component["name"]
            offset = component["offset"]
            size = component["size"]

            # 检查是否会读取超出文件范围
            if offset + size > input_file_size:
                print(f"错误: 尝试读取 {name} 时超出文件范围")
                continue

            # 移动文件指针到指定偏移量
            input_file.seek(offset)

            # 创建并写入切割后的文件
            with open(name, 'wb') as output_file:
                remaining_size = size
                while remaining_size > 0:
                    read_size = min(remaining_size, chunk_size)
                    data = input_file.read(read_size)
                    output_file.write(data)
                    remaining_size -= read_size

            print(f"成功切割 {name}")

except FileNotFoundError:
    print(f"错误: 未找到输入文件 {input_file_path}")
except Exception as e:
    print(f"发生未知错误: {e}")
