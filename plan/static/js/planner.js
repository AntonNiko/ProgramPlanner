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


function get_schedule_sections(id) {
    $.get("/api/section/get", { id: id}).done(function(data){
       console.log("Done!");
    });
}