# 陈硕勋-25343004-第二次人工智能编程作业
## 1. 任务拆解与 AI 协作策略
 步骤1：建立本地仓库和云端仓库链接
 步骤2：创建Student类
 步骤3：读取文件转化成列表
 步骤4：创建学号查找学生信息功能的函数
 步骤5：创建随机点名功能函数
 步骤5：创建生成考场安排功能的函数
 步骤6：创建生成准考证功能的函数
## 2. 核心 Prompt 迭代记录
本项目的开发过程是一个典型的“小步快跑”的迭代过程。每一次功能请求都像一个精准的 prompt，引导程序向更完善的方向演进。
 初代Prompt：接下来要写一个生成考场座位表安排的程序，将学生乱序排列，包含考场座位（1到n），姓名和学号，第一行是文件生成时间，要求生成在程序根目录下
 AI生成的问题：在记录时间时使用了datetime库，并不是上课提及的time标准库
 追问：datetime是标准库吗？和time库有什么区别？
 AI回答：datetime 绝对是 Python 的标准库。datetime 是给人看的（日历、日期、业务逻辑），time 是给机器看的（时间戳、性能测试、底层操作）。
## 3. Debug 与异常处理记录
 异常记录：初次读取文件时报错没有读取到
 原因：“人工智能编程语言学生名单.txt”与执行文件不在一个根目录下
## 4. 人工代码审查 (Code Review)
def generate_seating_chart(student_list, filename="考场座位表.txt"):

    # 确保是有效名单
    if not student_list:
        print("名单为空！")
        return

    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 复制并打乱名单
    shuffled_students = student_list[:] 
    random.shuffle(shuffled_students)
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"生成时间: {current_time}\n") # 第一行写时间
        f.write(f"{'座位号':<10}{'姓名':<10}{'学号':<15}\n") # 表头
        f.write("-" * 35 + "\n")

        #一边遍历列表一边生成从1开始的座位号
        for index, student in enumerate(shuffled_students, 1):
            f.write(f"{index:<10}{student.name:<10}{student.student_id:<15}\n")
            
    print(f"✅ 座位表已生成：{filename}")
 