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
      faculty,
      fullName,
      id,
      name,
      prog,
      finalExam,
      midExam,
      secs: [Section]
    }

    Section {
      building,
      day: [Day],
      note,
      room,
      seat,
      secno,
      status,
      teacher: [String],
      time,
      type
    }
    ```
