import os
import hashlib
import shutil
import argparse
from typing import Dict, List, Tuple


class FileDeduplicator:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.file_hashes: Dict[str, str] = {}
        self.duplicates: List[str] = []
        self.report: List[str] = []

    def calculate_hash(self, file_path: str) -> str:
        """计算文件的MD5哈希值（分块读取大文件）"""
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {e}")
            return ""

    def find_duplicates(self):
        """遍历目录查找重复文件"""
        print(f"开始深度遍历目录: {self.root_dir}")
        for dirpath, _, filenames in os.walk(self.root_dir):
            print(f"扫描目录: {dirpath}")  # 调试日志
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if not os.path.isfile(file_path):
                    continue

                print(f"处理文件: {file_path}")  # 调试日志
                file_hash = self.calculate_hash(file_path)
                if not file_hash:
                    continue

                if file_hash in self.file_hashes:
                    self.duplicates.append(file_path)
                    self.report.append(f"DUPLICATE: {file_path} -> Original: {self.file_hashes[file_hash]}")
                else:
                    self.file_hashes[file_hash] = file_path
                    self.report.append(f"UNIQUE: {file_path}")

    def remove_duplicates(self, dry_run: bool = True) -> Tuple[int, int]:
        """删除重复文件（默认模拟运行）"""
        removed_count = 0
        error_count = 0

        if dry_run:
            print("\n模拟运行结果（使用 --execute 参数实际执行删除）:")

        for dup in self.duplicates:
            try:
                if dry_run:
                    # 模拟运行时，检查文件是否存在
                    if os.path.exists(dup):
                        self.report.append(f"TO REMOVE: {dup}")
                    else:
                        self.report.append(f"FILE NOT FOUND: {dup}")
                else:
                    # 实际执行删除
                    os.remove(dup)
                    removed_count += 1
                    self.report.append(f"REMOVED: {dup}")
            except Exception as e:
                error_count += 1
                self.report.append(f"ERROR removing {dup}: {str(e)}")

        return removed_count, error_count

    def organize_files(self, target_dir: str, dry_run: bool = True):
        """将唯一文件按扩展名分类存储到新目录（支持模拟运行）"""
        if dry_run:
            print("\n模拟整理文件（使用 --execute 参数实际执行）:")

        os.makedirs(target_dir, exist_ok=True)

        for file_hash, original_path in self.file_hashes.items():
            # 获取文件扩展名
            filename = os.path.basename(original_path)
            file_ext = os.path.splitext(filename)[1].lower()
            category_dir = os.path.join(target_dir, file_ext[1:] if file_ext else "no_extension")

            if dry_run:
                # 模拟运行时，仅打印操作日志
                self.report.append(f"TO MOVE: {original_path} -> {category_dir}")
            else:
                # 实际执行移动
                os.makedirs(category_dir, exist_ok=True)
                dest_path = os.path.join(category_dir, filename)

                # 处理目标文件名冲突
                counter = 1
                while os.path.exists(dest_path):
                    base, ext = os.path.splitext(filename)
                    dest_path = os.path.join(category_dir, f"{base}_{counter}{ext}")
                    counter += 1

                try:
                    shutil.move(original_path, dest_path)
                    self.report.append(f"MOVED: {original_path} -> {dest_path}")
                except Exception as e:
                    self.report.append(f"ERROR moving {original_path}: {str(e)}")

    def remove_empty_dirs(self, dry_run: bool = True) -> Tuple[int, int]:
        """删除空文件夹（默认模拟运行）"""
        removed_count = 0
        error_count = 0

        if dry_run:
            print("\n模拟删除空文件夹（使用 --execute 参数实际执行）:")

        # 从最深层的目录开始遍历
        for dirpath, dirnames, filenames in sorted(os.walk(self.root_dir, topdown=False), key=lambda x: x[0], reverse=True):
            if not dirnames and not filenames:  # 如果目录为空
                try:
                    if dry_run:
                        # 模拟运行时，仅打印操作日志
                        self.report.append(f"TO REMOVE EMPTY DIR: {dirpath}")
                    else:
                        # 实际执行删除
                        os.rmdir(dirpath)
                        removed_count += 1
                        self.report.append(f"REMOVED EMPTY DIR: {dirpath}")
                except Exception as e:
                    error_count += 1
                    self.report.append(f"ERROR removing {dirpath}: {str(e)}")

        return removed_count, error_count

    def generate_report(self, report_file: str = "dedup_report.txt"):
        """生成处理报告"""
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("文件去重处理报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"扫描根目录: {self.root_dir}\n")
            f.write(f"找到唯一文件: {len(self.file_hashes)}\n")
            f.write(f"发现重复文件: {len(self.duplicates)}\n\n")

            f.write("\n处理详情:\n")
            f.write("-" * 50 + "\n")
            f.write("\n".join(self.report))


def main():
    parser = argparse.ArgumentParser(description="渗透测试字典文件去重整理工具")
    parser.add_argument("directory", help="要处理的根目录")
    parser.add_argument("--execute", action="store_true", help="实际执行删除操作（默认模拟运行）")
    parser.add_argument("--organize", metavar="TARGET_DIR", help="整理文件到指定目录（按扩展名分类）")
    parser.add_argument("--remove-empty-dirs", action="store_true", help="删除空文件夹")
    args = parser.parse_args()

    processor = FileDeduplicator(args.directory)

    print("开始扫描文件...")
    processor.find_duplicates()
    print(f"扫描完成，找到 {len(processor.file_hashes)} 个唯一文件")
    print(f"发现 {len(processor.duplicates)} 个重复文件")

    removed, errors = processor.remove_duplicates(dry_run=not args.execute)
    print(f"\n去重操作结果:")
    print(f"已删除文件: {removed}")
    print(f"删除失败: {errors}")

    if args.organize:
        print(f"\n开始整理文件到 {args.organize}...")
        processor.organize_files(args.organize, dry_run=not args.execute)
        print("文件整理完成")

    if args.remove_empty_dirs:
        print("\n开始删除空文件夹...")
        removed_dirs, dir_errors = processor.remove_empty_dirs(dry_run=not args.execute)
        print(f"删除空文件夹结果:")
        print(f"已删除空文件夹: {removed_dirs}")
        print(f"删除失败: {dir_errors}")

    processor.generate_report()
    print("\n已生成处理报告：dedup_report.txt")

    if args.execute:
        print("\n警告：实际删除了文件或文件夹！操作不可逆！")
    else:
        print("\n注意：本次为模拟运行，使用 --execute 参数实际执行删除")


if __name__ == "__main__":
    main()