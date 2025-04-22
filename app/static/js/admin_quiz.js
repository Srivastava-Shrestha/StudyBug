
let course_element = document.getElementById("course_id");

function change_option () {
    let course_id = course_element.value;
    let course_detail = courses_list.find(course => course.course_id == course_id);

    let chapter_element = document.getElementById("chapter_id");
    chapter_element.innerHTML = "";  

    if (course_detail) {
        course_detail.chapters.forEach(chapter => {
            let option = document.createElement("option");
            option.value = chapter.chapter_id;
            option.textContent = chapter.name;
            chapter_element.appendChild(option);
        });
    }
}

course_element.addEventListener("change",change_option );

