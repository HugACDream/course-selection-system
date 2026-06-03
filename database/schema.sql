-- ============================================================
-- 选课系统 - 数据库表结构设计
-- ============================================================

-- 学院表
CREATE TABLE IF NOT EXISTS colleges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT DEFAULT ''
);

-- 用户表（包含系统管理员、学院管理员、教师、学生）
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    FOREIGN KEY (college_id) REFERENCES colleges(id)
);

-- 选课记录表
CREATE TABLE IF NOT EXISTS course_selections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

-- 消息表
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

-- 插入默认学院
INSERT OR IGNORE INTO colleges (id, name, description) VALUES (1, '计算机学院', '计算机科学与技术学院');

-- 插入默认系统管理员账号
INSERT OR IGNORE INTO users (username, password, role, name)
VALUES ('admin', 'admin123', 'admin', '系统管理员');

-- 插入默认学院管理员账号（属于计算机学院）
INSERT OR IGNORE INTO users (username, password, role, name, college_id)
VALUES ('college_admin', 'admin123', 'college_admin', '学院管理员', 1);

-- 插入默认教师账号（属于计算机学院）
INSERT OR IGNORE INTO users (username, password, role, name, college_id)
VALUES ('teacher1', 'admin123', 'teacher', '张教授', 1);

-- 插入默认学生账号（属于计算机学院）
INSERT OR IGNORE INTO users (username, password, role, name, college_id)
VALUES ('student1', 'admin123', 'student', '李同学', 1);
