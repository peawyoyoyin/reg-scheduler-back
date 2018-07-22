from bs4 import BeautifulSoup
from .base import BaseScraper

class CourseInfo(BaseScraper):
    def __repr__(self):
        return \
'''<ClassInfo 
\t%s
\t%s
\t%s
\t%s
\t%s
\t%d sections
>''' \
% (
    self.class_id,
    self.class_name_en,
    self.class_name_th,
    self.midterm_exam_date,
    self.final_exam_date,
    len(self.sections)
)

    @property
    def course_id(self):
        return self._soup.select('#Table2 > tr')[3].select('font')[0].text
    
    @property
    def course_name_th(self):
        return self._soup.select('#Table2 > tr')[4].select('font')[0].text
    
    @property
    def course_name_en(self):
        return self._soup.select('#Table2 > tr')[5].select('font')[0].text
    
    @property
    def midterm_exam_date(self):
        text = self._soup.select('#Table4 font')[1].text.strip()
        if text.startswith('TDF'):
            return 'TDF'
        return text
    
    @property
    def final_exam_date(self):
        text = self._soup.select('#Table4 font')[3].text.strip()
        if text.startswith('TDF'):
            return 'TDF'
        return text
    
    @property
    def sections(self):
        result = []
        els = self._soup.select('#Table3 tr')[2:]
        for el in els:
            result.append(SectionItem(el))
        return result

class SectionItem(BaseScraper):
    def __repr__(self):
        return '<SectionItem %s %s %s %s %s %s %s>' % \
            (self.section_number, ' '.join(self.days), self.time, self.building, self.room, self.teacher, self.capacity)

    @property
    def section_number(self):
        return self._soup.select('font')[0].text.strip()
    
    @property
    def days(self):
        return self._soup.select('font')[2].text.strip().split()
    
    @property
    def time(self):
        return self._soup.select('font')[3].text.strip()
    
    @property
    def building(self):
        return self._soup.select('font')[4].text.strip()
    
    @property
    def room(self):
        return self._soup.select('font')[5].text.strip()
    
    @property
    def teacher(self):
        return self._soup.select('font')[6].text.strip()
    
    @property
    def notes(self):
        return self._soup.select('font')[7].text.strip()
    
    @property
    def capacity(self):
        return self._soup.select('font')[8].text.split('/')[1]


if __name__ == '__main__':
    with open('info.html') as f:
        class_info = ClassInfo(BeautifulSoup(f.read(), 'lxml'))
    
    print(class_info)
    print(class_info.sections)
    
