import requests
from requests_toolbelt.adapters.appengine import monkeypatch

monkeypatch()

SESSION_URL = "https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.QueryCourseScheduleNewServlet"
PARAM_BASEURL = "https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseListNewServlet"
DATA_BASEURL = "https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseScheduleDtlNewServlet"

class Fetcher:
    def __init__(self):
        self._session = requests.Session()
        self._session.verify = False
    
    def _get_session(self):
        self._session.get(SESSION_URL)
    
    def get_course_list(self, semester, year, course_number='%%',study_program='S'):
        payload = {
            'studyProgram'  : study_program,
            'semester'      : semester,
            'courseno'      : course_number,
            'acadyear'      : year
        }
        response = self._session.get(PARAM_BASEURL, params=payload)
        if 'Set-cookie' in response.headers:
            self._get_session()
            response = self._session.get(PARAM_BASEURL, params=payload)
        
        return response.content
    
    def get_course_info(self, semester, year, course_number, study_program='S'):
        payload = {
            'courseNo': course_number,
            'studyProgram': study_program
        }
        self.get_course_list(semester, year)
        response = self._session.get(DATA_BASEURL, params=payload)

        return response.content

if __name__ == '__main__':
    fetcher = Fetcher()
    r = fetcher.get_course_list(2, 2560)
    with open('out_list.html', 'wb') as f:
        f.write(r)
    r = fetcher.get_course_info(2, 2560, 2110332)
    with open('out_info.html', 'wb') as f:
        f.write(r)
