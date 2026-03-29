#外部库导入区
import random
import datetime
import os

#Studen类定义区
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




#功能函数区
def read_students_from_file(filename):
    """
    读取文件并创建学生对象列表的函数
    """
    students = []  # 用于存储所有学生对象的列表

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 1. 读取第一行（标题行）
            header = file.readline()

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

def search_student(student_list):
    """
    实现查找功能的函数
    """
    while True:
        # 1. 获取用户输入
        target_id = input("\n请输入要查询的学号 (输入 'q' 退出): ").strip()

        # 退出机制
        if target_id.lower() == 'q':
            break

        # 2. 遍历查找
        found = False
        for student in student_list:
            if student.student_id == target_id:
                # 3. 找到则打印并跳出循环
                print("\n" + "=" * 30)
                print(student)  # 这里会自动调用 __str__ 方法
                print("=" * 30)
                found = True
                break

        # 4. 未找到提示
        if not found:
            print(f"未找到学号为 {target_id} 的学生，请重试。")

def random_roll_call(student_list):
    """
    实现随机点名功能：
    1. 输入点名人数
    2. 验证输入（必须是数字，且不能大于总人数）
    3. 随机抽取不重复的学生
    """

    total_count = len(student_list)

    if total_count == 0:
        print("名单为空，无法点名！")
        return

    print(f"\n--- 随机点名系统 ---")
    print(f"当前班级总人数: {total_count}")

    while True:
        user_input = input("请输入要抽取的学生人数: ")

        # 1. 处理非数字字符输入
        if not user_input.isdigit():
            print("❌ 输入无效：请输入一个正整数（例如 1, 5）。")
            continue

        # 将输入转换为整数
        num_to_pick = int(user_input)

        # 2. 处理数字大于总人数的情况
        if num_to_pick > total_count:
            print(f"❌ 人数过多：班级总共只有 {total_count} 人，请输入小于或等于 {total_count} 的数字。")
            continue

        # 3. 处理数字为 0 或负数的情况 (虽然 isdigit 排除了负数，但逻辑上要排除 0)
        if num_to_pick <= 0:
            print("❌ 输入无效：抽取人数必须大于 0。")
            continue

        # --- 输入验证通过，开始点名 ---
        print(f"\n🎲 正在随机抽取 {num_to_pick} 位同学...\n")

        # 核心算法：random.sample
        # 作用：从列表中随机抽取指定数量的元素，且保证不重复
        selected_students = random.sample(student_list, num_to_pick)

        print("=== 🎉 中奖名单 🎉 ===")
        for i, student in enumerate(selected_students, 1):
            print(f"{i}. {student}")  # 调用 __str__ 方法
        print("======================")

        # 点名结束后退出循环
        break


def generate_seating_chart(student_list, filename="考场座位表.txt"):
    """
    生成考场座位表：
    1. 将学生名单乱序排列
    2. 分配座位号 (1 到 n)
    3. 写入文件，第一行为生成时间
    """

    if not student_list:
        print("错误：学生名单为空，无法生成座位表！")
        return

    # 1. 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. 复制一份名单并打乱顺序 (使用切片 [:] 复制，避免修改原始名单顺序)
    shuffled_students = student_list[:]
    random.shuffle(shuffled_students)

    # 3. 写入文件
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 写入第一行：文件生成时间
            f.write(f"生成时间: {current_time}\n")
            # 写入表头
            f.write(f"{'座位号':<10}{'姓名':<10}{'学号':<15}\n")
            f.write("-" * 35 + "\n")  # 分隔线

            # 遍历打乱后的列表，分配座位号
            for index, student in enumerate(shuffled_students, 1):
                # 格式化输出：座位号 | 姓名 | 学号
                # <10 表示左对齐并占用10个字符宽度，为了排版整齐
                line = f"{index:<10}{student.name:<10}{student.student_id:<15}\n"
                f.write(line)

        print(f"✅ 成功！座位表已生成。")
        print(f"📂 文件保存位置: {os.path.abspath(filename)}")
        print(f"⏰ 生成时间: {current_time}")

    except Exception as e:
        print(f"❌ 写入文件时发生错误: {e}")



# --- 主程序入口 ---
if __name__ == "__main__":
    # 指定文件名
    filename = "人工智能编程语言学生名单.txt"

    # 调用函数读取数据
    all_students = read_students_from_file(filename)

    if all_students:
        print(f"\n--- 共读取到 {len(all_students)} 个学生信息 ---")
        # 启动查找功能
        search_student(all_students)
        # 启动点名功能
        random_roll_call(all_students)
        # 启动生成考场安排功能
        generate_seating_chart(all_students)
    else:
        print("未加载到任何数据。")