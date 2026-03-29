class Student:
    """
    学生数据类
    用于存储和展示学生信息
    """

    def __init__(self, raw_data_list):
        """
        初始化方法：将列表中的数据映射到对象属性
        注意：根据你的txt文件结构，数据顺序为：
        [序号, 姓名, 性别, 班级, 学号, 学院]
        """
        # 去除可能存在的多余空格并赋值
        self.id = raw_data_list[0].strip()
        self.name = raw_data_list[1].strip()
        self.gender = raw_data_list[2].strip()
        self.class_num = raw_data_list[3].strip()
        self.student_id = raw_data_list[4].strip()
        self.college = raw_data_list[5].strip()

    def __str__(self):
        """
        友好打印方法：定义 print(对象) 时的输出格式
        """
        return f"[学生] 姓名:{self.name}, 学号:{self.student_id}, 班级:{self.class_num}, 学院:{self.college}, 性别:{self.gender}"


def read_students_from_file(filename):
    """
    读取文件并创建学生对象列表的函数
    """
    students = []  # 用于存储所有学生对象的列表

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 1. 读取第一行（标题行）
            header = file.readline()
            print(f"文件标题: {header.strip()}")

            # 2. 逐行读取剩余内容
            for line in file:
                line = line.strip()  # 去除首尾空白字符

                # 跳过空行
                if not line:
                    continue

                # 3. 数据清洗与切分
                # 由于你的数据是直接连在一起的（如 "1张三男1..."），我们需要按逻辑切分
                # 这里假设每个字段长度固定（序号1位，姓名2位，性别1位，班级1位，学号7位，学院2-3位）
                # 但为了通用性，我们使用更智能的切分逻辑（基于正则或空格判断）

                # 简单处理：利用正则表达式在数字和汉字之间、汉字和汉字之间进行分割
                import re
                # 匹配数字 或 非数字（汉字/字母）
                parts = re.findall(r'\d+|[^\d\s]+', line)

                # 过滤掉空字符串
                parts = [part for part in parts if part]

                # 4. 检查数据完整性（确保有6个字段）
                if len(parts) >= 6:
                    # 创建学生对象并添加到列表
                    student = Student(parts)
                    students.append(student)
                    # print(f"成功创建: {student}") # 调试用
                else:
                    print(f"警告：数据格式错误，跳过该行: {line}")

    except FileNotFoundError:
        print(f"错误：找不到文件 {filename}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

    return students


# --- 主程序入口 ---
if __name__ == "__main__":
    # 指定文件名
    filename = "人工智能编程语言学生名单.txt"

    # 调用函数读取数据
    all_students = read_students_from_file(filename)

    print(f"\n--- 共读取到 {len(all_students)} 个学生信息 ---")

