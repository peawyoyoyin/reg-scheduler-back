import requests
import bs4
import re


class Scraper():
    '''prog 'S'ทวิภาค 'T'ตรีภาค 'I'ทวิ-นานาชาติ,
    semester '1'ภาคต้น '2'ภาคปลาย '3'ภาคฤดูร้อน,
    year พ.ศ.'''

    _listurl = 'https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseListNewServlet'
    _courseurl = 'https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseScheduleDtlNewServlet'

    def __init__(self, prog, year, semester):
        self.sesion = requests.Session()
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
                    'courseid': data[0].get_text().strip(),
                    'coursename': data[2].get_text().strip()
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
            'year_sem': datat2[0].get_text().strip(),
            'prog': datat2[1].get_text().strip(),
            'id': datat2[2].get_text().strip(),
            'name': datat2[3].get_text().strip(),
            'thai_name': datat2[4].get_text().strip(),
            'full_name': datat2[5].get_text().strip(),
            'faculty': datat2[6].get_text().strip().replace('\xa0', ' ')
        })

        datat4 = table4.find_all('font')
        result.update({
            'mid_exam': datat4[1].get_text().strip(),
            'final_exam': datat4[3].get_text().strip(),
        })

        secs = []
        datat3 = table3.find_all('tr')
        for idx, sec in enumerate(datat3):
            if idx > 1:
                data = sec.find_all('td')
                secs.append({
                    'status': ('open' if data[0].get_text().strip() == '' else 'close'),
                    'secno': re.search(r'\d+', data[1].get_text().strip()).group(),
                    'type': data[2].get_text().strip(),
                    'day': data[3].get_text().strip().split(),
                    'time': data[4].get_text().strip(),
                    'building': data[5].get_text().strip(),
                    'room': data[6].get_text().strip(),
                    'teacher': data[7].get_text().strip().split(','),
                    'note': data[8].get_text().strip(),
                    'seat': (data[9].get_text().strip() if len(data) > 9 else '')
                })
        result.update({'secs': secs})

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
        response = self.sesion.get(self._listurl, params=param)
        if 'Set-cookie' in response.headers:
            response = self.sesion.get(self._listurl, params=param)
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
        response = self.sesion.get(self._courseurl, params=param)
        return response.content.decode('thai')

    def getcourseinfo(self, courseno):
        '''return course info'''
        return Scraper._parsehtmlcourseinfo(self._gethtmlcourseinfo(courseno))


if __name__ == '__main__':
    scp = Scraper('S', 2560, 2)
    print(scp.getlist('2110332'))
    print(scp.getcourseinfo('2110332'))
