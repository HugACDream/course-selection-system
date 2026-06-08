-- ============================================================
-- 选课系统 - 数据库表结构设计
-- ============================================================

-- 学院表
CREATE TABLE IF NOT EXISTS colleges (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT DEFAULT ''
);

-- 用户表（包含系统管理员、学院管理员、教师、学生）
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'college_admin', 'teacher', 'student')),
    name VARCHAR(50) NOT NULL,
    college_id INTEGER,
    email VARCHAR(100) DEFAULT '',
    phone VARCHAR(20) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(id)
);

-- 课程表
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    credits REAL NOT NULL DEFAULT 0,
    teacher_id INTEGER NOT NULL,
    college_id INTEGER NOT NULL,
    max_students INTEGER NOT NULL DEFAULT 30,
    prerequisites TEXT DEFAULT '[]',
    syllabus TEXT DEFAULT '',
    course_material_path VARCHAR(500) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id),
    FOREIGN KEY (college_id) REFERENCES colleges(id),
    UNIQUE(teacher_id, name)
);

-- 确保已有表也有该约束（CREATE TABLE IF NOT EXISTS 不会重建已存在的表）
CREATE UNIQUE INDEX IF NOT EXISTS idx_courses_teacher_name ON courses(teacher_id, name);

-- 选课记录表
CREATE TABLE IF NOT EXISTS course_selections (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled')),
    selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE(student_id, course_id)
);

-- 成绩表
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    score REAL,
    grade_point REAL,
    recorded_by INTEGER,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (recorded_by) REFERENCES users(id),
    UNIQUE(student_id, course_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_grades_student_course ON grades(student_id, course_id);

-- 课件表（支持多文件）
CREATE TABLE IF NOT EXISTS course_materials (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER DEFAULT 0,
    uploaded_by INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- 消息表
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    course_id INTEGER,
    content TEXT NOT NULL,
    reply_to INTEGER,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (reply_to) REFERENCES messages(id)
);

-- ============================================================
-- 学院（4个）
-- ============================================================
INSERT OR IGNORE INTO colleges (name, description) VALUES ('计算机学院', '计算机科学与技术学院');
INSERT OR IGNORE INTO colleges (name, description) VALUES ('数学与统计学院', '数学与统计学院');
INSERT OR IGNORE INTO colleges (name, description) VALUES ('外国语学院', '外国语学院');
INSERT OR IGNORE INTO colleges (name, description) VALUES ('物理学院', '物理学院');

-- ============================================================
-- 系统管理员
-- ============================================================
INSERT OR IGNORE INTO users (username, password, role, name)
VALUES ('admin', 'admin123', 'admin', '系统管理员');

-- ============================================================
-- 学院管理员（每个学院一个）
-- ============================================================
INSERT OR IGNORE INTO users (username, password, role, name, college_id)
SELECT 'college_admin', 'admin123', 'college_admin', '计算机学院管理员', id FROM colleges WHERE name='计算机学院';
INSERT OR IGNORE INTO users (username, password, role, name, college_id)
SELECT 'math_admin', 'admin123', 'college_admin', '数学学院管理员', id FROM colleges WHERE name='数学与统计学院';
INSERT OR IGNORE INTO users (username, password, role, name, college_id)
SELECT 'english_admin', 'admin123', 'college_admin', '外语学院管理员', id FROM colleges WHERE name='外国语学院';
INSERT OR IGNORE INTO users (username, password, role, name, college_id)
SELECT 'physics_admin', 'admin123', 'college_admin', '物理学院管理员', id FROM colleges WHERE name='物理学院';

-- ============================================================
-- 教师（每个学院2-3位）
-- ============================================================
-- 计算机学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher1', 'admin123', 'teacher', '张教授', 'zhang@cs.edu.cn', '13800001001', id FROM colleges WHERE name='计算机学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher2', 'admin123', 'teacher', '王老师', 'wang@cs.edu.cn', '13800001002', id FROM colleges WHERE name='计算机学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher3', 'admin123', 'teacher', '李教授', 'li@cs.edu.cn', '13800001003', id FROM colleges WHERE name='计算机学院';
-- 数学与统计学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher4', 'admin123', 'teacher', '刘教授', 'liu@math.edu.cn', '13800002001', id FROM colleges WHERE name='数学与统计学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher5', 'admin123', 'teacher', '陈老师', 'chen@math.edu.cn', '13800002002', id FROM colleges WHERE name='数学与统计学院';
-- 外国语学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher6', 'admin123', 'teacher', '周教授', 'zhou@eng.edu.cn', '13800003001', id FROM colleges WHERE name='外国语学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher7', 'admin123', 'teacher', '吴老师', 'wu@eng.edu.cn', '13800003002', id FROM colleges WHERE name='外国语学院';
-- 物理学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'teacher8', 'admin123', 'teacher', '杨教授', 'yang@phy.edu.cn', '13800004001', id FROM colleges WHERE name='物理学院';

-- ============================================================
-- 学生（每个学院3-4位，密码均为123456便于测试）
-- ============================================================
-- 计算机学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student1', '123456', 'student', '李同学', 'stu1@cs.edu.cn', '13900001001', id FROM colleges WHERE name='计算机学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student2', '123456', 'student', '王同学', 'stu2@cs.edu.cn', '13900001002', id FROM colleges WHERE name='计算机学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student3', '123456', 'student', '赵同学', 'stu3@cs.edu.cn', '13900001003', id FROM colleges WHERE name='计算机学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student4', '123456', 'student', '周同学', 'stu4@cs.edu.cn', '13900001004', id FROM colleges WHERE name='计算机学院';
-- 数学与统计学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student5', '123456', 'student', '钱同学', 'stu5@math.edu.cn', '13900002001', id FROM colleges WHERE name='数学与统计学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student6', '123456', 'student', '孙同学', 'stu6@math.edu.cn', '13900002002', id FROM colleges WHERE name='数学与统计学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student7', '123456', 'student', '吴同学', 'stu7@math.edu.cn', '13900002003', id FROM colleges WHERE name='数学与统计学院';
-- 外国语学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student8', '123456', 'student', '郑同学', 'stu8@eng.edu.cn', '13900003001', id FROM colleges WHERE name='外国语学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student9', '123456', 'student', '冯同学', 'stu9@eng.edu.cn', '13900003002', id FROM colleges WHERE name='外国语学院';
-- 物理学院
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student10', '123456', 'student', '陈同学', 'stu10@phy.edu.cn', '13900004001', id FROM colleges WHERE name='物理学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student11', '123456', 'student', '褚同学', 'stu11@phy.edu.cn', '13900004002', id FROM colleges WHERE name='物理学院';
INSERT OR IGNORE INTO users (username, password, role, name, email, phone, college_id)
SELECT 'student12', '123456', 'student', '卫同学', 'stu12@phy.edu.cn', '13900004003', id FROM colleges WHERE name='物理学院';

-- ============================================================
-- 课程（8门，覆盖不同学院、不同教师）
-- ============================================================
-- 计算机学院课程
INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT 'C语言程序设计', 'C语言基础语法与编程入门', 3.0, u.id, c.id, 60, '[]', '第1章 引言, 第2章 数据类型, 第3章 控制流, 第4章 函数, 第5章 指针'
FROM users u, colleges c WHERE u.username='teacher2' AND c.name='计算机学院';

INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '数据结构', '线性表、树、图等经典数据结构', 4.0, u.id, c.id, 50, '["C语言程序设计"]', '第1章 绪论, 第2章 线性表, 第3章 栈与队列, 第4章 树, 第5章 图, 第6章 查找, 第7章 排序'
FROM users u, colleges c WHERE u.username='teacher1' AND c.name='计算机学院';

INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '操作系统', '进程管理、内存管理、文件系统', 4.0, u.id, c.id, 45, '["数据结构"]', '第1章 概述, 第2章 进程管理, 第3章 内存管理, 第4章 文件系统, 第5章 I/O管理'
FROM users u, colleges c WHERE u.username='teacher3' AND c.name='计算机学院';

INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '数据库原理', '关系模型、SQL、事务管理', 3.5, u.id, c.id, 50, '["数据结构"]', '第1章 绪论, 第2章 关系模型, 第3章 SQL, 第4章 规范化, 第5章 事务与并发'
FROM users u, colleges c WHERE u.username='teacher2' AND c.name='计算机学院';

INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '计算机网络', 'TCP/IP协议栈、网络编程', 3.0, u.id, c.id, 55, '["C语言程序设计"]', '第1章 概述, 第2章 物理层, 第3章 数据链路层, 第4章 网络层, 第5章 传输层, 第6章 应用层'
FROM users u, colleges c WHERE u.username='teacher1' AND c.name='计算机学院';

-- 数学与统计学院课程
INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '高等数学', '微积分、级数与微分方程', 5.0, u.id, c.id, 80, '[]', '第1章 函数与极限, 第2章 导数, 第3章 积分, 第4章 级数, 第5章 微分方程'
FROM users u, colleges c WHERE u.username='teacher4' AND c.name='数学与统计学院';

INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '线性代数', '矩阵、向量空间、特征值', 4.0, u.id, c.id, 70, '[]', '第1章 行列式, 第2章 矩阵, 第3章 向量空间, 第4章 线性方程组, 第5章 特征值与特征向量'
FROM users u, colleges c WHERE u.username='teacher5' AND c.name='数学与统计学院';

-- 外国语学院课程
INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '大学英语', '英语听说读写综合训练', 3.0, u.id, c.id, 60, '[]', 'Unit 1-16: Listening, Speaking, Reading, Writing'
FROM users u, colleges c WHERE u.username='teacher6' AND c.name='外国语学院';

-- 物理学院课程
INSERT OR IGNORE INTO courses (name, description, credits, teacher_id, college_id, max_students, prerequisites, syllabus)
SELECT '大学物理', '力学、热学、电磁学基础', 4.0, u.id, c.id, 70, '["高等数学"]', '第1章 质点力学, 第2章 刚体, 第3章 热学, 第4章 电磁学, 第5章 光学'
FROM users u, colleges c WHERE u.username='teacher8' AND c.name='物理学院';

-- ============================================================
-- 选课记录
-- ============================================================
-- student1 选了 C语言、数据结构(已确认)、高等数学、大学英语
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'confirmed'
FROM users u, courses co WHERE u.username='student1' AND co.name='C语言程序设计';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'confirmed'
FROM users u, courses co WHERE u.username='student1' AND co.name='数据结构';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'pending'
FROM users u, courses co WHERE u.username='student1' AND co.name='高等数学';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'pending'
FROM users u, courses co WHERE u.username='student1' AND co.name='大学英语';

-- student2 选了 C语言(已确认)、数据结构(pending)、计算机网络(pending)
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'confirmed'
FROM users u, courses co WHERE u.username='student2' AND co.name='C语言程序设计';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'pending'
FROM users u, courses co WHERE u.username='student2' AND co.name='数据结构';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'pending'
FROM users u, courses co WHERE u.username='student2' AND co.name='计算机网络';

-- student3 选了 高等数学(已确认)、线性代数(confirmed)
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'confirmed'
FROM users u, courses co WHERE u.username='student3' AND co.name='高等数学';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'confirmed'
FROM users u, courses co WHERE u.username='student3' AND co.name='线性代数';

-- student4 选了 数据库原理(pending)、操作系统(pending)
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'pending'
FROM users u, courses co WHERE u.username='student4' AND co.name='数据库原理';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'pending'
FROM users u, courses co WHERE u.username='student4' AND co.name='操作系统';

-- student5 选了 高等数学(confirmed)、大学物理(pending)
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'confirmed'
FROM users u, courses co WHERE u.username='student5' AND co.name='高等数学';
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'pending'
FROM users u, courses co WHERE u.username='student5' AND co.name='大学物理';

-- student6 选了 C语言(confirmed)
INSERT OR IGNORE INTO course_selections (student_id, course_id, status)
SELECT u.id, co.id, 'confirmed'
FROM users u, courses co WHERE u.username='student6' AND co.name='C语言程序设计';

-- ============================================================
-- 成绩（为 confirmed 的选课录入成绩）
-- ============================================================
-- student1: C语言 92分, 数据结构 85分
INSERT OR IGNORE INTO grades (student_id, course_id, score, grade_point)
SELECT u.id, co.id, 92.0, 4.0
FROM users u, courses co WHERE u.username='student1' AND co.name='C语言程序设计';
INSERT OR IGNORE INTO grades (student_id, course_id, score, grade_point)
SELECT u.id, co.id, 85.0, 3.0
FROM users u, courses co WHERE u.username='student1' AND co.name='数据结构';

-- student2: C语言 78分
INSERT OR IGNORE INTO grades (student_id, course_id, score, grade_point)
SELECT u.id, co.id, 78.0, 2.0
FROM users u, courses co WHERE u.username='student2' AND co.name='C语言程序设计';

-- student3: 高等数学 95分, 线性代数 88分
INSERT OR IGNORE INTO grades (student_id, course_id, score, grade_point)
SELECT u.id, co.id, 95.0, 4.0
FROM users u, courses co WHERE u.username='student3' AND co.name='高等数学';
INSERT OR IGNORE INTO grades (student_id, course_id, score, grade_point)
SELECT u.id, co.id, 88.0, 3.0
FROM users u, courses co WHERE u.username='student3' AND co.name='线性代数';

-- student5: 高等数学 73分
INSERT OR IGNORE INTO grades (student_id, course_id, score, grade_point)
SELECT u.id, co.id, 73.0, 2.0
FROM users u, courses co WHERE u.username='student5' AND co.name='高等数学';

-- student6: C语言 61分
INSERT OR IGNORE INTO grades (student_id, course_id, score, grade_point)
SELECT u.id, co.id, 61.0, 1.0
FROM users u, courses co WHERE u.username='student6' AND co.name='C语言程序设计';

-- ============================================================
-- 消息（教师与学生的互动）
-- ============================================================
-- 张教授 -> student1
INSERT OR IGNORE INTO messages (sender_id, receiver_id, course_id, content)
SELECT t.id, s.id, co.id, '李同学，你的C语言作业完成得很好，继续保持！'
FROM users t, users s, courses co WHERE t.username='teacher1' AND s.username='student1' AND co.name='C语言程序设计';

-- student1 -> 张教授（回复）
INSERT OR IGNORE INTO messages (sender_id, receiver_id, course_id, content, reply_to)
SELECT s.id, t.id, co.id, '谢谢张教授，我会努力的！',
    (SELECT id FROM messages WHERE content LIKE '%李同学，你的C语言作业完成得很好%')
FROM users s, users t, courses co WHERE s.username='student1' AND t.username='teacher1' AND co.name='C语言程序设计';

-- 王老师 -> student2
INSERT OR IGNORE INTO messages (sender_id, receiver_id, course_id, content)
SELECT t.id, s.id, co.id, '王同学，请在本周五前提交C语言实验报告。'
FROM users t, users s, courses co WHERE t.username='teacher2' AND s.username='student2' AND co.name='C语言程序设计';

-- student1 -> 王老师
INSERT OR IGNORE INTO messages (sender_id, receiver_id, course_id, content)
SELECT s.id, t.id, co.id, '王老师您好，请问数据库原理的课件什么时候上传？'
FROM users s, users t, courses co WHERE s.username='student1' AND t.username='teacher2' AND co.name='数据库原理';
