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

  - GET `/courseinfo`

    returns information about the course with `courseId`

    result is `null` if the specified `courseId` is invalid

    #### url parameters

    | name | description |
    | ---- | ----------- |
    | courseId | Course Id **(required)**
