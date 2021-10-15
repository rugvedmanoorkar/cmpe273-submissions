totalClasses = []
totalStudents = []


def student(_, info, id):
    for s in totalStudents:
        if s['id'] == id:
            return s
    return None


def students(_, info):
    return {
        'success': True,
        'errors': [],
        'students': totalStudents}


def classes(_, info, id):
    for c in totalClasses:
        if c['id'] == id:
            return c
    return None


def all_classes(_, info):
    return {
        'success': True,
        'errors': ['No errors. Found all Classes.'],
        'classes': totalClasses}


def create_student(_, info, name):
    if len(totalStudents) == 0:
        id = 1
    else:
        id = totalStudents[-1]['id'] + 1
    s = {
        'id': id,
        'name': name,
        
    }
    totalStudents.append(s)
    return {
        'success': True,
        'errors': [],
        'students': [s]}


def get_student_ids():
    ids = []
    for s in totalStudents:
        ids.append(s['id'])
    return ids


def create_class(_, info, name, student_ids):
    ids = get_student_ids()
    for id in student_ids:
        if id not in ids:
            return {
                'success': False,
                'errors': ['Student of given id not found.'],
                'classes': None}
    if len(totalClasses) == 0:
        id = 1
    else:
        id = totalClasses[-1]['id'] + 1
    c = {
        'id': id,
        'name': name,
        'students': [totalStudents[i - 1] for i in student_ids]
    }
    totalClasses.append(c)
    return {
        'success': True,
        'errors': ['Class created.'],
        'classes': [c]}


def add_student_to_class(_, info, id, student_id):
    ids = get_student_ids()
    if student_id not in ids:
        return {
            'success': False,
            'errors': ['Student not found.'],
            'class': None}
    newStudent = None
    for s in totalStudents:
        if s['id'] == student_id:
            newStudent = s
            break
    if newStudent is not None:
        for cl in totalClasses:
            if cl['id'] == id:
                cl['students'].append(newStudent)
                return {
                    'success': True,
                    'errors': [],
                    'class': cl}
        return {'success': False,
                'errors': ['Class not found. Error: 404'],
                'class': None}
    else:
        return {
            'success': False,
            'errors': ['Student not found. Error: 404'],
            'class': None
        }
