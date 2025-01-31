- ### 新增功能

  #### 1. **简写模式**

  - `-e`：`--execute` 的简写，用于实际执行删除操作。
  - `-o`：`--organize` 的简写，用于指定整理文件的目标目录。
  - `-r`：`--remove-empty-dirs` 的简写，用于删除空文件夹。
  - `-v`：`--version` 的简写，用于显示版本信息。

  #### 2. **帮助信息**

  - 使用 `argparse.RawTextHelpFormatter` 格式化帮助信息，使其更易读。
  - 添加了详细的示例说明，方便用户快速上手。

  ------

  ### 使用示例

  #### 1. **查看帮助信息**

  bash

  复制

  ```
  python dedup.py -h
  ```

  #### 2. **模拟运行**

  bash

  复制

  ```
  python dedup.py /path/to/directory -o /path/to/target -r
  ```

  #### 3. **实际执行**

  bash

  复制

  ```
  python dedup.py /path/to/directory -o /path/to/target -r -e
  ```

  #### 4. **删除空文件夹**

  bash

  复制

  ```
  python dedup.py /path/to/directory -r -e
  ```

  #### 5. **显示版本信息**

  bash

  复制

  ```
  python dedup.py -v
  ```

  ------

  ### 帮助信息示例

  运行 `python dedup.py -h` 将显示以下内容：

  复制

  ```
  usage: dedup.py [-h] [-e] [-o TARGET_DIR] [-r] [-v] directory
  
  渗透测试字典文件去重整理工具
  
  positional arguments:
    directory             要处理的根目录
  
  optional arguments:
    -h, --help            show this help message and exit
    -e, --execute         实际执行删除操作（默认模拟运行）
    -o TARGET_DIR, --organize TARGET_DIR
                          整理文件到指定目录（按扩展名分类）
    -r, --remove-empty-dirs
                          删除空文件夹
    -v, --version         显示版本信息
  
  示例:
    1. 模拟运行（仅显示操作日志）:
       python dedup.py /path/to/directory -o /path/to/target -r
  
    2. 实际执行（删除重复文件并整理）:
       python dedup.py /path/to/directory -o /path/to/target -r -e
  
    3. 删除空文件夹:
       python dedup.py /path/to/directory -r -e
  ```

  ------

  ### 总结

  - 添加了简写模式，提升命令行操作的便捷性。
  - 完善了帮助信息，包括参数说明和使用示例。
  - 保持了脚本的模块化设计，便于后续扩展和 GUI 开发。