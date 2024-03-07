document.addEventListener('DOMContentLoaded', function() {
     let sections = [{
        id: 'home',
        url: '../sections/home.html'
     }, {
        id: 'import',
        url: '../sections/imageSelection.html'
     }];

    sections.forEach(function(section) {
        fetch(section.url)
        .then(response => {
            return response.text();
        })
        .then(data => {
            document.getElementById(section.id).innerHTML = data;
        });
    });
});

function openNav() {
    document.getElementById("sidebar").style.width = "150px";
    for (var i = 0; i < document.getElementsByClassName("main-content").length; i++) {
        document.getElementsByClassName("main-content")[i].style.marginLeft = "150px";
    }
    document.getElementsByClassName("openbtn").style.display = "none";
}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";
    for (var i = 0; i < document.getElementsByClassName("main-content").length; i++) {
        document.getElementsByClassName("main-content")[i].style.marginLeft = "0px";
    }
    document.getElementsByClassName("openbtn").style.display = "block";
}

function showSection(sectionId) {
    var sections = document.querySelectorAll('.contentSection');
    sections.forEach(function(section) {
        section.style.display = 'none';
    });
    
    document.getElementById(sectionId).style.display = 'flex';
}