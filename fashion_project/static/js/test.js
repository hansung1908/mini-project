// 현재 페이지의 주소 가져오기
var currentPage = window.location.pathname;
console.log("현재 페이지의 주소:", currentPage);

// 각 링크에 대해 현재 페이지와 비교하여 적절한 스타일 적용
var link1 = document.getElementById("link1");
var link2 = document.getElementById("link2");
var link3 = document.getElementById("link3");

if (link1) {
    if (currentPage === "/") {
        link1.classList.add("text-body-emphasis", "font-weight-bold");
    } else {
        link1.classList.add("text-muted", "opacity-50");
    }
}

if (link2) {
    if (currentPage === "/select") {
        link2.classList.add("text-body-emphasis", "font-weight-bold");
    } else {
        link2.classList.add("text-muted", "opacity-50");
    }
}

if (link3) {
    if (currentPage === "/view") {
        link3.classList.add("text-body-emphasis", "font-weight-bold");
    } else {
        link3.classList.add("text-muted", "opacity-50");
    }
}