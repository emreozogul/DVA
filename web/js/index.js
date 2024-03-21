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


});

function triggerFileSelectionAndProcessing() {
  eel.select_and_process_image()(function (resultPath) {
    if (resultPath) {
      console.log('Image processed and saved to:', resultPath);
      // You can now display the processed image or inform the user
      // For example, update the 'src' of an img tag to show the processed image
      document.getElementById('processedImage').src = resultPath;
    } else {
      console.log('No image was selected.');
    }
  });
}


function uploadImage() {
  var input = document.getElementById('x');
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      // Send the image data to Python
      eel.process_image(e.target.result)(function (res) {
        console.log(res); // Log the response from Python
      });
    }

    reader.readAsDataURL(input.files[0]);
  }
}

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