/**
 * API 通信层 - 封装所有后端接口调用
 */

const API_BASE = '/api';

const api = {
    /**
     * 通用请求方法
     */
    async request(method, url, data = null, isFormData = false) {
        const options = {
            method,
            headers: isFormData ? {} : { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
        };
        if (data && !isFormData) {
            options.body = JSON.stringify(data);
        } else if (data && isFormData) {
            options.body = data;
        }
        try {
            const resp = await fetch(API_BASE + url, options);
            const json = await resp.json();
            return json;
        } catch (err) {
            console.error('API请求失败:', err);
            return { success: false, message: '网络错误，请稍后重试' };
        }
    },

    get(url) { return this.request('GET', url); },
    post(url, data) { return this.request('POST', url, data); },
    put(url, data) { return this.request('PUT', url, data); },
    delete(url) { return this.request('DELETE', url); },
    upload(url, formData) { return this.request('POST', url, formData, true); },

    // ============================================================
    // 认证接口
    // ============================================================
    auth: {
        login: (username, password) => api.post('/auth/login', { username, password }),
        logout: () => api.post('/auth/logout'),
        currentUser: () => api.get('/auth/current_user'),
        changePassword: (oldPwd, newPwd) => api.post('/auth/change_password', { old_password: oldPwd, new_password: newPwd }),
    },

    // ============================================================
    // 系统管理员接口
    // ============================================================
    admin: {
        // 学生CRUD
        listStudents: (params) => api.get('/admin/students?' + new URLSearchParams(params)),
        createStudent: (data) => api.post('/admin/students', data),
        getStudent: (id) => api.get('/admin/students/' + id),
        updateStudent: (id, data) => api.put('/admin/students/' + id, data),
        deleteStudent: (id) => api.delete('/admin/students/' + id),

        // 教师CRUD
        listTeachers: (params) => api.get('/admin/teachers?' + new URLSearchParams(params)),
        createTeacher: (data) => api.post('/admin/teachers', data),
        getTeacher: (id) => api.get('/admin/teachers/' + id),
        updateTeacher: (id, data) => api.put('/admin/teachers/' + id, data),
        deleteTeacher: (id) => api.delete('/admin/teachers/' + id),

        // 课程CRUD
        listCourses: (params) => api.get('/admin/courses?' + new URLSearchParams(params)),
        createCourse: (data) => api.post('/admin/courses', data),
        getCourse: (id) => api.get('/admin/courses/' + id),
        updateCourse: (id, data) => api.put('/admin/courses/' + id, data),
        deleteCourse: (id) => api.delete('/admin/courses/' + id),

        // 成绩CRUD
        listGrades: (params) => api.get('/admin/grades?' + new URLSearchParams(params)),
        createGrade: (data) => api.post('/admin/grades', data),
        updateGrade: (id, data) => api.put('/admin/grades/' + id, data),
        deleteGrade: (id) => api.delete('/admin/grades/' + id),

        // 学院管理
        listColleges: () => api.get('/admin/colleges'),
        createCollege: (data) => api.post('/admin/colleges', data),

        // 111
        // 选课记录CRUD
        listSelections: (params) => api.get('/admin/selections?' + new URLSearchParams(params)),
        createSelection: (data) => api.post('/admin/selections', data),
        updateSelection: (id, data) => api.put('/admin/selections/' + id, data),
        deleteSelection: (id) => api.delete('/admin/selections/' + id),

        // 选课统计（需求2）
        getCourseSelectionStats: () => api.get('/admin/statistics/course-selection'),
        exportStats: () => api.get('/admin/statistics/course-selection/export'),
    },

    // ============================================================
    // 学院管理员接口
    // ============================================================
    collegeAdmin: {
        // 教师管理
        listTeachers: (params) => api.get('/college-admin/teachers?' + new URLSearchParams(params)),
        createTeacher: (data) => api.post('/college-admin/teachers', data),
        updateTeacher: (id, data) => api.put('/college-admin/teachers/' + id, data),
        deleteTeacher: (id) => api.delete('/college-admin/teachers/' + id),

        // 学生管理
        listStudents: (params) => api.get('/college-admin/students?' + new URLSearchParams(params)),
        createStudent: (data) => api.post('/college-admin/students', data),
        updateStudent: (id, data) => api.put('/college-admin/students/' + id, data),
        deleteStudent: (id) => api.delete('/college-admin/students/' + id),

        // 课程管理
        listCourses: (params) => api.get('/college-admin/courses?' + new URLSearchParams(params)),
        createCourse: (data) => api.post('/college-admin/courses', data),
        updateCourse: (id, data) => api.put('/college-admin/courses/' + id, data),
        deleteCourse: (id) => api.delete('/college-admin/courses/' + id),

        // 选课管理
        listSelections: (params) => api.get('/college-admin/selections?' + new URLSearchParams(params)),

        // 成绩管理
        listGrades: (params) => api.get('/college-admin/grades?' + new URLSearchParams(params)),
        createGrade: (data) => api.post('/college-admin/grades', data),
        updateGrade: (id, data) => api.put('/college-admin/grades/' + id, data),
        deleteGrade: (id) => api.delete('/college-admin/grades/' + id),

        // 抽签（需求4）
        lottery: (courseId, data) => api.post('/college-admin/lottery/' + courseId, data),
        getLotteryResult: (courseId) => api.get('/college-admin/lottery/' + courseId + '/result'),
        exportLotteryResult: (courseId) => api.get('/college-admin/lottery/' + courseId + '/export'),
    },

    // ============================================================
    // 教师接口
    // ============================================================
    teacher: {
        // 课程管理
        listMyCourses: () => api.get('/teacher/courses'),
        getCourseDetail: (id) => api.get('/teacher/courses/' + id),
        updateCourse: (id, data) => api.put('/teacher/courses/' + id, data),
        uploadMaterial: (courseId, formData) => api.upload('/teacher/courses/' + courseId + '/upload-material', formData),
        listMaterials: (courseId) => api.get('/teacher/courses/' + courseId + '/materials'),
        deleteMaterial: (materialId) => api.delete('/teacher/materials/' + materialId),

        // 中签学生
        getConfirmedStudents: (courseId) => api.get('/teacher/courses/' + courseId + '/confirmed-students'),

        // 成绩管理（需求6）
        listCourseGrades: (courseId) => api.get('/teacher/courses/' + courseId + '/grades'),
        saveGrades: (courseId, data) => api.post('/teacher/courses/' + courseId + '/grades', data),
        getGradeStatistics: (courseId) => api.get('/teacher/courses/' + courseId + '/statistics'),

        // 消息（需求7）
        sendMessage: (data) => api.post('/teacher/messages/send', data),
        listReceivedMessages: (params) => api.get('/teacher/messages/received?' + new URLSearchParams(params)),
        listSentMessages: (params) => api.get('/teacher/messages/sent?' + new URLSearchParams(params)),
        markRead: (id) => api.put('/teacher/messages/' + id + '/read'),
    },

    // ============================================================
    // 学生接口
    // ============================================================
    student: {
        // 个人信息
        getProfile: () => api.get('/student/profile'),
        updateProfile: (data) => api.put('/student/profile', data),

        // 课程浏览
        listCourses: (params) => api.get('/student/courses?' + new URLSearchParams(params)),
        getCourseDetail: (id) => api.get('/student/courses/' + id),

        // 选课（需求8/9/10）
        listMySelections: () => api.get('/student/my-selections'),
        selectCourse: (courseId) => api.post('/student/select-course', { course_id: courseId }),
        cancelSelection: (selectionId) => api.post('/student/cancel-selection/' + selectionId),

        // 课件下载
        listCourseMaterials: (courseId) => api.get('/student/courses/' + courseId + '/materials'),

        // 成绩查询
        listMyGrades: () => api.get('/student/my-grades'),

        // 课件下载
        downloadMaterial: (courseId) => api.get('/student/courses/' + courseId + '/download-material'),

        // 消息（需求12）
        sendMessage: (data) => api.post('/student/messages/send', data),
        listReceivedMessages: (params) => api.get('/student/messages/received?' + new URLSearchParams(params)),
        listSentMessages: (params) => api.get('/student/messages/sent?' + new URLSearchParams(params)),
        markRead: (id) => api.put('/student/messages/' + id + '/read'),
        replyMessage: (id, content) => api.post('/student/messages/' + id + '/reply', { content }),
    },
};
