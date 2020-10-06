/*
 * Copyright (c) 2020. by Anton Nikitenko
 * All rights reserved.
 */

let selectedDeleteScheduleName = null;


$(".delete-schedule").click(function(){
    selectedDeleteScheduleName = $(this).attr("value");
    $("#scheduleDeleteModalID").attr("value", selectedDeleteScheduleName);
});