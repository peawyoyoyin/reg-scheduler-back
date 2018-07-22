from bs4 import BeautifulSoup
from .base import BaseScraper

class CourseList(BaseScraper):
    def __repr__(self):
        return '<ClassList (%d classes)>' % len(self.classes)

    @property
    def courses(self):
        els = self._soup.select('#Table4 > tr')
        result = []
        for el in els:
            result.append(CourseListItem(el))
        return result

class CourseListItem(BaseScraper):
    def __repr__(self):
        return '<ClassListItem <%s %s>>' % (self.class_id, self.class_name)

    @property
    def course_id(self):
        return self._soup.select('font')[0].text.strip()

    @property
    def course_name(self):
        return self._soup.select('font')[2].text.strip()

if __name__ == '__main__':
    with open('list.html') as f:
        class_list = ClassList(BeautifulSoup(f.read(), 'lxml'))
    
    print(class_list)
    print(class_list.classes)
    