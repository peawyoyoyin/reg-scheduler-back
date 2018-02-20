# reg-scheduler-back
The backend for phootip/reg-scheduler. Functionalities include getting data from the reg and transform HTML into pretty JSON responses

## API endpoints

 - GET `/courselist`

    returns the result of querying the *reg* with given parameters

    #### url parameters
    | name | description |
    | ---- | ----------- |
    | courseId | Course Id |
    | courseName | Course Name |

    #### response schema
    ```
    Response [
      {
        courseid: String,
        coursename: String
      },
      ...
    ]
    ```

  - GET `/courseinfo`

    returns information about the course with `courseId`

    result is `null` if the specified `courseId` is invalid

    #### url parameters

    | name | description |
    | ---- | ----------- |
    | courseId | Course Id **(required)**

    #### response schema
    ```
    Response {
      id,
      name: {
        abbr,
        th,
        en
      },
      faculty,
      prog,
      finalExamDate: ExamTimeRange,
      midExam: ExamTimeRange,
      secs: [Section]
    }

    Section {
      building,
      remark,
      room,
      seat,
      sectionNumber,
      status,
      teacher: [String],
      type,
      timeRanges: [TimeRange]
    }

    ExamTimeRange {
      day,
      month,
      year,
      time: {
        start,
        end
      }
    }

    TimeRange {
      day,
      end,
      start
    }
    ```

## Notes
This project is currently broken due to this bug: https://github.com/shazow/urllib3/pull/1283.

To solve this, edit the local files inside `lib/urllib3` (after installing) according to the pull request.
