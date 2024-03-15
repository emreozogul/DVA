// General 
function openNav() {
  document.getElementById("sidebar").style.width = "150px";
  for (var i = 0; i < document.getElementsByClassName("page").length; i++) {
    document.getElementsByClassName("page")[i].style.marginLeft = "150px";
  }
}
function closeNav() {
  document.getElementById("sidebar").style.width = "0";
  for (var i = 0; i < document.getElementsByClassName("page").length; i++) {
    document.getElementsByClassName("page")[i].style.marginLeft = "0px";
  }
}
function showSection(sectionId) {
  var sections = document.querySelectorAll('.page');
  sections.forEach(function (section) {
    section.style.display = 'none';
  });

  document.getElementById(sectionId).style.display = 'flex';
}
// Import
function nextPageImport() {
  document.getElementById('importPage1').style.display = 'none';
  document.getElementById('importPage2').style.display = 'flex';
}
function prevPageImport() {
  document.getElementById('importPage1').style.display = 'flex';
  document.getElementById('importPage2').style.display = 'none';
}
function nextPageImport2() {
  document.getElementById('importPage2').style.display = 'none';
  document.getElementById('importPage3').style.display = 'flex';
}

function prevPageImport2() {
  document.getElementById('importPage2').style.display = 'flex';
  document.getElementById('importPage3').style.display = 'none';
}


document.addEventListener('DOMContentLoaded', async () => {
  let projectData = await eel.get_projects();
  console.log(projectData);
  const projectList = document.getElementById('projects');



  if (projectData.length > 0) {
    projectData.forEach(project => {
      const projectItem = document.createElement('li');
      projectItem.textContent = project;
      projectList.appendChild(projectItem);
    });
  } else {
    const projectItem = document.createElement('li');
    projectItem.textContent = "No projects found";
    projectList.appendChild(projectItem);
  }


  const openbtn = document.getElementById('openbtn');
  openbtn.addEventListener('click', openNav);

  const closebtn = document.getElementById('closebtn');
  closebtn.addEventListener('click', closeNav);

  document.querySelector('.navContainer').addEventListener('click', function (event) {
    // Check if the clicked element is one of the divs you're interested in
    if (event.target.classList.contains('navItem')) {
      // Get the 'data-section' attribute of the clicked div
      var sectionId = event.target.getAttribute('data-section');
      console.log(sectionId);
      showSection(sectionId);
    }
  });

  const nextBtnImport = document.getElementById('nextBtnImport');
  nextBtnImport.addEventListener('click', nextPageImport);

  const prevBtnImport = document.getElementById('prevBtnImport');
  prevBtnImport.addEventListener('click', prevPageImport);

  const nextBtnImport2 = document.getElementById('nextBtnImport2');
  nextBtnImport2.addEventListener('click', nextPageImport2);

  const prevBtnImport2 = document.getElementById('prevBtnImport2');
  prevBtnImport2.addEventListener('click', prevPageImport2);

  const sNewProjectBtn = document.getElementById('sNewProjectBtn');
  sNewProjectBtn.addEventListener('click', showAddScreenProject);

  const sProjectListBtn = document.getElementById('sProjectListBtn');
  sProjectListBtn.addEventListener('click', showProjectList);

  const addProjectForm = document.getElementById('addProjectForm');
  addProjectForm.addEventListener('submit', function (event) {
    event.preventDefault();
    addProject();
  });
  var image = document.getElementById('image');
  var canvas = document.getElementById('canvas');
  var cropper;


  var buttons = document.querySelectorAll('.importButton');
  buttons.forEach((button) => {
    button.addEventListener('click', function (event) {
      console.log(event.target.id);
      document.getElementById('imageInput').click();
      var files = event.target.files;
      var reader = new FileReader();
      reader.onload = function (e) {
        image.src = e.target.result;
        image.style.display = 'block'; // Show the image

        if (cropper) {
          cropper.destroy(); // Destroy the old cropper instance
        }
        image.onload = function () {
          cropper = new Cropper(image, {
            aspectRatio: 1 / 1,
            background: false,
            highlight: false,
            zoomable: false,
            zoomOnTouch: false,
            zoomOnWheel: false,
            ready: function () {
              var width = image.offsetWidth;
              var height = image.offsetHeight;

              canvas.width = width;
              canvas.height = height;
              canvas.getContext('2d').clearRect(0, 0, width, height);
              canvas.getContext('2d').drawImage(
                image,
                0, 0, image.naturalWidth, image.naturalHeight,
                0, 0, width, height
              );
            }
          }
          );
        };
      };
      if (files && files.length > 0) {
        reader.readAsDataURL(files[0]);
      }
    });
  });




});


// project

function createFolder() {
  var folderName = document.getElementById('projectName').value;
  eel.create_new_folder(folderName);  // Call the Python function
}


async function addProject() {
  var name = document.getElementById('projectNameAdd').value;
  var author = document.getElementById('authorAdd').value;

  console.log(name);
  console.log(author);

  if ((name == '' || author == '') || (name == null && author == null)) {
    alert('Please fill in all fields');
    return;
  }

  let isOkey = await eel.check_project_name(name);
  if (isOkey == false) {
    alert('Project name already exists');
    return;
  }
  let response = await eel.add_project(name, author)();
  alert(response);

  const projectlist = document.getElementById('project-list');
  const projectItem = document.createElement('li');
  projectItem.textContent = name;
  projectlist.appendChild(projectItem);
  showProjectList();
}

async function readProject() {
  let response = await eel.read_project()();
  const projectlist = document.getElementById('project-list');

  response.forEach(project => {
    const projectItem = document.createElement('li');
    projectItem.textContent = project;
    projectlist.appendChild(projectItem);
  });

}


function showProjectList() {
  document.getElementById('projectPage1').style.display = 'flex';
  document.getElementById('projectPage2').style.display = 'none';
}

function showAddScreenProject() {
  document.getElementById('projectPage1').style.display = 'none';
  document.getElementById('projectPage2').style.display = 'flex';
}