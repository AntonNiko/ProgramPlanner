/*
 * Copyright (c) 2020. by Anton Nikitenko
 * All rights reserved.
 */

let selectedDeleteScheduleName = null;

// TODO move this to a dedicated home page JS file
$(".delete-schedule").click(function(){
    selectedDeleteScheduleName = $(this).attr("value");
    $("#scheduleDeleteModalID").attr("value", selectedDeleteScheduleName);
});

/*
 *  Define conversions from schedule model year and term for Full Calendar start date
 */

let schedule_to_calendar = {
    "2020": {
        "1": "2020-01-06",
        "2": "2020-05-04",
        "3": "2020-09-09"
    },
    "2021": {
        "1": "2020-01-06",
        "2": "2020-05-05",
        "3": "2020-09-08"
    }
};

let meeting_days_to_numbers = {
    "meet_M": 1,
    "meet_T": 2,
    "meet_W": 3,
    "meet_R": 4,
    "meet_F": 5,
    "meet_S": 6,
    "meet_Z": 0
}

function convert_meeting_days_to_numbers_array(array) {
    let days = [];
    let index
    for (index of ["meet_M", "meet_T", "meet_W", "meet_R", "meet_F", "meet_S", "meet_Z"]){
        if (array[index] == true) {
            days.push(meeting_days_to_numbers[index])
        }
    }

    return days;
}

/**
 * Provides a set of methods that calls the course API methods (incl course offerings)
 */
class CourseProvider {

    /**
     * Returns the data for a particular course with an associated CRN
     * @param crn
     * @param successCallbackHandler
     */
    static get_course(crn, successCallbackHandler) {
        $.get("/api/data/course", { crn: crn}).done(function(data) {
            successCallbackHandler(data);
        });
    }
}

/**
 * Provides a set of methods that calls the schedule API methods.
 */
class ScheduleProvider {

    /**
     * Fetches all schedules associated with a logged in user.
     * @param successCallbackHandler
     */
    static get_user_schedules(successCallbackHandler) {
        $.get("/api/schedule/get").done(function(data){
            successCallbackHandler(data);
        });
    }

    /**
     * Fetches the user's schedule with a specific schedule ID.
     * @param id
     * @param successCallbackHandler
     */
    static get_user_schedule_by_id(id, successCallbackHandler) {
        $.get("/api/schedule/get", {id: id}).done(function(data){
            successCallbackHandler(data);
        });
    }

    /**
     * Returns data with all the sections associated with a particular schedule ID,
     * including meeting times
     * @param id
     * @param successCallbackHandler
     */
    static get_schedule_sections(id, successCallbackHandler) {
        $.get("/api/section/get", { id: id}).done(function(data){
            successCallbackHandler(data);
        });
    }

    /**
     * Returns data with all the meetings associated with a particular section CRN
     * @param crn
     * @param successCallbackHandler
     */
    static get_section_meetings(crn, successCallbackHandler) {
        $.get("/api/meeting/get", { crn: crn}).done(function(data){
            successCallbackHandler(data);
        });
    }
}