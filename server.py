from flask import Flask, jsonify, request, render_template
import json
from scraper import Scraper

scp = Scraper('S', 2560, 2)
app = Flask(__name__)

@app.route('/')
def apiInfoPage():
    return render_template('index.html')

@app.route('/courselist')
def queryCourseList():
    '''
        courseNo,
        courseName,
        courseType,
        genedCode
    '''
    course_name = request.args.get('courseName', '')
    course_no = request.args.get('courseId', '')
    course_type = request.args.get('courseType', '')
    gened_code = request.args.get('genedCode', '')
    return jsonify({
            'courses': scp.getlist(course_no, course_name, course_type, gened_code)
        })

@app.route('/courseinfo')
def getCourseData():
    '''
        courseNo
    '''
    course_no = request.args.get('courseId')
    if course_no is None:
        return 'courseId is required', 400
    return jsonify(
        scp.getcourseinfo(course_no)
    )

if __name__ == '__main__':
    app.run()
