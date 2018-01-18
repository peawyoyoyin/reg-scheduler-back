import requests


class Scraper():

    _listurl = 'https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseListNewServlet'
    _courseurl = 'https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseScheduleDtlNewServlet'

    def __init__(self, prog, year, semester):
        self.sesion = requests.Session()
        self.setprop(prog, year, semester)

    def setprop(self, prog, year, semester):
        self.prog = prog
        self.year = year
        self.semester = semester


    def _createsession(self):
        self.sesion.get(self._listurl)

    @staticmethod
    def parsehtmlList(html):
        # need to implement
        print(html)

    @staticmethod
    def parsehtmlCourseinfo(html):
        # need to implement
        print(html)

    def getlist(self, courseno='', coursename='', coursetype='', genedcode=''):
        self._createsession()
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
        return response.content.decode('thai')

    def getcourseinfo(self, courseno):
        self._createsession()
        self.getlist(courseno)
        param = {
            'courseNo': str(courseno),
            'studyProgram': str(self.prog)
        }
        response = self.sesion.get(self._courseurl, params=param)
        return response.content.decode('thai')


if __name__ == '__main__':
    scp = Scraper('S', 2560, 2)
    print(scp.getcourseinfo('2110332'))
