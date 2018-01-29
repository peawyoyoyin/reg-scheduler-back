import requests
import bs4
import re
import datetime
import calendar

MONTH_NAMES = ['','ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
DAY_NAMES_TRANSFORM = {
    'MO': 'MON',
    'TU': 'TUE',
    'WE': 'WED',
    'TH': 'THU',
    'FR': 'FRI',
    'SA': 'SAT',
    'SU': 'SUN',
}

def _transformExamDate(examDate):
    '''
        exam dates comes in this format:
        15 พ.ค. 2561 เวลา 8:30-11:30 น.
    '''
    if examDate.startswith('TDF'):
        return {
            'date': 'tdf',
            'day': 'tdf',
            'start': 'tdf',
            'end': 'tdf',
        }
    
    tokens = examDate.split(' ')
    time = tokens[4].split('-')
    month_name = str(MONTH_NAMES.index(tokens[1]) if tokens[1] in MONTH_NAMES else '-1')
    day_index = datetime.datetime(int(tokens[2])-543, int(month_name), int(tokens[0])).weekday()
    day_name = calendar.day_abbr[day_index].upper()
    return {
        'day': day_name,
        'date': tokens[0].zfill(2) + '/' + month_name.zfill(2) + '/' + tokens[2],
        'start': time[0],
        'end': time[1],
    }

def _buildTimeRanges(time, days):
    '''
        time comes in this format:
        9:30-11:00
    '''
    tokens = time.split('-')
    if len(tokens) != 2:
        return {
            'day': 'tdf',
            'start': 'tdf',
            'end' : 'tdf',
        }
    
    return [{
        'day': DAY_NAMES_TRANSFORM.get(day, 'invalid-day'),
        'start': tokens[0],
        'end': tokens[1],
    } for day in days]

class Scraper():
    '''prog 'S'ทวิภาค 'T'ตรีภาค 'I'ทวิ-นานาชาติ,
    semester '1'ภาคต้น '2'ภาคปลาย '3'ภาคฤดูร้อน,
    year พ.ศ.'''

    _listurl = 'https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseListNewServlet'
    _courseurl = 'https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseScheduleDtlNewServlet'

    def __init__(self, prog, year, semester):
        self.session = requests.Session()
        self.setprop(prog, year, semester)

    def setprop(self, prog, year, semester):
        '''prog 'S'ทวิภาค 'T'ตรีภาค 'I'ทวิ-นานาชาติ,
        semester '1'ภาคต้น '2'ภาคปลาย '3'ภาคฤดูร้อน,
        year พ.ศ.'''
        self.prog = prog
        self.year = year
        self.semester = semester

    @staticmethod
    def _parsehtmllist(html):
        result = []
        page = bs4.BeautifulSoup(html, 'html.parser')
        table = page.find(id='Table4')
        if table:
            courses = table.find_all('tr')
            for course in courses:
                data = course.find_all('font')
                result.append({
                    'courseId': data[0].get_text().strip(),
                    'courseName': data[2].get_text().strip()
                })
        return result

    @staticmethod
    def _parsehtmlcourseinfo(html):
        result = {}
        page = bs4.BeautifulSoup(html, 'html.parser')
        table2 = page.find(id='Table2')
        table4 = page.find(id='Table4')
        table3 = page.find(id='Table3')

        if (not table2) or (not table3) or (not table4):
            return

        datat2 = table2.find_all('font')
        result.update({
            'yearSem': datat2[0].get_text().strip(),
            'prog': datat2[1].get_text().strip(),
            'id': datat2[2].get_text().strip(),
            'name': {
                'abbr':datat2[3].get_text().strip(),
                'th': datat2[4].get_text().strip(),
                'en': datat2[5].get_text().strip(),
            },
            'faculty': datat2[6].get_text().strip().replace('\xa0', ' ')
        })

        datat4 = table4.find_all('font')
        result.update({
            'midExamDate': _transformExamDate(datat4[1].get_text().strip()),
            'finalExamDate' : _transformExamDate(datat4[3].get_text().strip()),
        })

        secs = []
        datat3 = table3.find_all('tr')
        for idx, sec in enumerate(datat3):
            if idx > 1:
                data = sec.find_all('td')
                try:
                    secs.append({
                        'status': ('open' if data[0].get_text().strip() == '' else 'close'),
                        'sectionNumber': re.search(r'\d+', data[1].get_text().strip()).group(),
                        'type': data[2].get_text().strip(),
                        'building': data[5].get_text().strip(),
                        'room': data[6].get_text().strip(),
                        'teacher': data[7].get_text().strip().split(','),
                        'remark': data[8].get_text().strip(),
                        'seat': (data[9].get_text().strip() if len(data) > 9 else ''),
                        # 'day': data[3].get_text().strip().split(),
                        # 'time': data[4].get_text().strip(),
                        'timeRanges': _buildTimeRanges(data[4].get_text().strip(), data[3].get_text().strip().split())
                    })
                except:
                    pass
        result.update({'sections': secs})

        return result

    def _gethtmllist(self, courseno='', coursename='', coursetype='', genedcode=''):
        param = {
            'studyProgram': str(self.prog),
            'acadyear': str(self.year),
            'semester': str(self.semester),
            'courseno': str(courseno),
            'coursename': str(coursename),
            'coursetype': str(coursetype),
            'genedcode': str(genedcode)
        }
        response = self.session.get(self._listurl, params=param)
        if 'Set-cookie' in response.headers:
            response = self.session.get(self._listurl, params=param)
        return response.content.decode('thai')

    def getlist(self, courseno='', coursename='', coursetype='', genedcode=''):
        ''' gened coursetype=1
            genedcode   1:social
                        2:human
                        3:sci
                        4:coed
                        5:lang
        '''
        return Scraper._parsehtmllist(self._gethtmllist(courseno, coursename, coursetype, genedcode))

    def _gethtmlcourseinfo(self, courseno):
        self._gethtmllist(courseno)
        param = {
            'courseNo': str(courseno),
            'studyProgram': str(self.prog)
        }
        response = self.session.get(self._courseurl, params=param)
        return response.content.decode('thai')

    def getcourseinfo(self, courseno):
        '''return course info'''
        return Scraper._parsehtmlcourseinfo(self._gethtmlcourseinfo(courseno))


if __name__ == '__main__':
    scp = Scraper('S', 2560, 2)
    print(scp.getlist('2110332'))
    print(scp.getcourseinfo('2110332'))
