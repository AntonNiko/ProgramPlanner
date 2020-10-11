/*
 * Copyright (c) 2020. by Anton Nikitenko
 * All rights reserved.
 */

let selectedDeleteScheduleName = null;


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

function get_schedule_sections(id, successCallbackHandler) {
    $.get("/api/section/get", { id: id}).done(function(data){
       successCallbackHandler(data);
    });
}

function get_section_meetings(crn, successCallbackHandler) {
    $.get("/api/meeting/get", { crn: crn}).done(function(data){
        successCallbackHandler(data);
    });
}