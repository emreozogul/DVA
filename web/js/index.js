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

async function loadProjects() {
  let projectData = await eel.get_projects()();  // Note the double parentheses to invoke the function
  return projectData;
}
var projects = [];


document.addEventListener('DOMContentLoaded', async () => {
  projects = await loadProjects();
  updateProjectList();

  document.getElementById('openbtn').addEventListener('click', openNav);

  document.getElementById('closebtn').addEventListener('click', closeNav);

  document.getElementById('prevBtnImport').addEventListener('click', prevPageImport);

  document.getElementById('sNewProjectBtn').addEventListener('click', showAddScreenProject);

  document.getElementById('sProjectListBtn').addEventListener('click', showProjectList);

  document.querySelector('.navContainer').addEventListener('click', function (event) {
    // Check if the clicked element is one of the divs you're interested in
    if (event.target.classList.contains('navItem')) {
      // Get the 'data-section' attribute of the clicked div
      var sectionId = event.target.getAttribute('data-section');
      console.log(sectionId);
      showSection(sectionId);
    }
  });

  document.getElementById("importForm").addEventListener('submit', async function (event) {
    event.preventDefault();
    var allImagesUploaded = checkPhaseImagesAreUploaded();
    var select = document.getElementById("project-select");
    var value = select.options[select.selectedIndex].value;
    var phaseQuantity = document.querySelector('.choicebox-container input[type="radio"][name="radio"]:checked').value;
    console.log("importForm -> select value", value)
    console.log("importForm -> phaseQuantity", phaseQuantity)
    console.log("importForm -> allImagesUploaded", allImagesUploaded)
    console.log("select", select)

    if (value === '' || value === undefined || value === null || value === "Select a project") {
      alert('Select a project first.');
      return;
    }
    else if (phaseQuantity === '' || phaseQuantity === undefined || phaseQuantity === null) {
      alert('Select the number of phases first.');
      return;
    } else {
      var phaseContainer = document.getElementById('phaseUpload');
      var imagePaths = [];
      if (phaseContainer.hasChildNodes()) {
        var labels = phaseContainer.getElementsByClassName('label');

        for (var i = 0; i < labels.length; i++) {
          imagePaths.push(labels[i].textContent);
        }
      }
      console.log("importForm -> imagePaths", imagePaths)
      var projectName = select.options[select.selectedIndex].value;
      var project = projects.find(project => project.name === projectName);
      console.log("importForm -> projectPath", projectPath)
      // eel.import_images(projectPath, imagePaths, phaseQuantity)();

    }

  });

  // Get the modal
  var modal = document.getElementById("myModal");

  // Get the button that opens the modal
  var btn = document.getElementById("HelpNav");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks on the button, open the modal 
  btn.onclick = function () {
    modal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  span.onclick = function () {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  function openModal(message) {

  }


  function updatePhaseUpload(phaseQuantity) {
    const phaseUploadDiv = document.getElementById('phaseUpload');

    // Clear existing content
    phaseUploadDiv.innerHTML = null;

    // Add new content based on phaseQuantity
    if (phaseQuantity === '2') {
      phaseUploadDiv.innerHTML =
        `<div class="phase-image-upload-container" id="phaseContainer">
        <div class="row" >
          <div style="display:flex; flex:1 ; align-items:center; justify-content:space-between ;">
            <p style="padding:6px ; font-weight: bold; font-size:20px ; color:#555555;">Upload Images</p>
            <svg width="32px" height="32px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#000000" stroke-width="0.264">
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
              <g id="SVGRepo_iconCarrier"> 
                <path d="M16.19 2H7.81C4.17 2 2 4.17 2 7.81V16.18C2 19.83 4.17 22 7.81 22H16.18C19.82 22 21.99 19.83 21.99 16.19V7.81C22 4.17 19.83 2 16.19 2ZM17.53 7.53L9.81 15.25H12.83C13.24 15.25 13.58 15.59 13.58 16C13.58 16.41 13.24 16.75 12.83 16.75H8C7.59 16.75 7.25 16.41 7.25 16V11.17C7.25 10.76 7.59 10.42 8 10.42C8.41 10.42 8.75 10.76 8.75 11.17V14.19L16.47 6.47C16.62 6.32 16.81 6.25 17 6.25C17.19 6.25 17.38 6.32 17.53 6.47C17.82 6.76 17.82 7.24 17.53 7.53Z" fill="#000000"></path> 
              </g>
            </svg>
          </div>
        </div>
        <div class="row" >
          <div class="phase-image-upload-button" data-label-id="image-path-1">Phase 1</div>
          <p class="label" id="image-path-1"></p>
        </div>
        <div class="row" >
          <div class="phase-image-upload-button" data-label-id="image-path-2">Phase 2</div>
          <p class="label" id="image-path-2"></p>
        </div>
      </div>`;

      var buttons = phaseUploadDiv.getElementsByClassName("phase-image-upload-button");

      for (var i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', function (event) {
          var labelId = event.target.getAttribute('data-label-id');
          triggerImageSelection(labelId);
        });
      }

    } else if (phaseQuantity === '3') {
      phaseUploadDiv.innerHTML =
        `<div class="phase-image-upload-container" id="phaseContainer">
        <div class="row" >
          <div style="display:flex; flex:1 ; align-items:center; justify-content:space-between ;">
            <p style="padding:6px ; font-weight: bold; font-size:20px ; color:#555555;">Upload Images</p>
            <svg width="32px" height="32px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#000000" stroke-width="0.264">
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
              <g id="SVGRepo_iconCarrier"> 
                <path d="M16.19 2H7.81C4.17 2 2 4.17 2 7.81V16.18C2 19.83 4.17 22 7.81 22H16.18C19.82 22 21.99 19.83 21.99 16.19V7.81C22 4.17 19.83 2 16.19 2ZM17.53 7.53L9.81 15.25H12.83C13.24 15.25 13.58 15.59 13.58 16C13.58 16.41 13.24 16.75 12.83 16.75H8C7.59 16.75 7.25 16.41 7.25 16V11.17C7.25 10.76 7.59 10.42 8 10.42C8.41 10.42 8.75 10.76 8.75 11.17V14.19L16.47 6.47C16.62 6.32 16.81 6.25 17 6.25C17.19 6.25 17.38 6.32 17.53 6.47C17.82 6.76 17.82 7.24 17.53 7.53Z" fill="#000000"></path> 
              </g>
            </svg>
            
          </div>
        </div>
        <div class="row" >
          <div class="phase-image-upload-button" data-label-id="image-path-1">Phase 1</div>
          <p class="label" id="image-path-1"></p>
        </div>
        <div class="row" >
          <div class="phase-image-upload-button" data-label-id="image-path-2" >Phase 2</div>
          <p class="label" id="image-path-2"></p>
        </div>
        <div class="row" >
          <div class="phase-image-upload-button" data-label-id="image-path-3" >Phase 1</div>
          <p class="label" id="image-path-3"></p>
        </div>
      </div>`;

      var buttons = phaseUploadDiv.getElementsByClassName("phase-image-upload-button");

      for (var i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', function (event) {
          var labelId = event.target.getAttribute('data-label-id');
          triggerImageSelection(labelId);
        });
      }
    }
  }

  // Listen for changes on the radio buttons
  document.querySelectorAll('.choicebox-container input[type="radio"][name="radio"]').forEach(radio => {
    radio.addEventListener('change', function () {
      updatePhaseUpload(this.value);
    });
  });

  document.getElementById('addProjectForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    var owner = document.getElementById('authorAdd').value;
    var projectName = document.getElementById('projectNameAdd').value;
    var description = document.getElementById('descriptionAdd').value;


    let response = await checkProjectExists(projectName);
    if (response) {
      alert('Project already exists.');
      return;
    }
    var newProject = {
      owner: owner,
      name: projectName,
      description: description,
      timestamp: new Date().toLocaleString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    };

    await eel.add_project(projectName, owner, description)();
    await eel.create_new_folder(projectName)();
    projects.push(newProject);

    updateProjectList();
    document.getElementById('authorAdd').value = '';
    document.getElementById('projectNameAdd').value = '';
    document.getElementById('descriptionAdd').value = '';
    showProjectList();
  });

  function updateProjectList() {
    var projectList = document.getElementById('projects');
    var projectSelect = document.getElementById('project-select');



    if (!projectList) {
      console.error('The "projects" element does not exist.');
      return;
    }
    projectList.innerHTML = '';
    projectSelect.innerHTML = '<option value="">Select a project</option>';


    // Add each project to the project list
    for (var i = 0; i < projects.length; i++) {
      console.log(projects[i]);
      // Create a new list item element for the project with project name title and owner as text and createdAt as text
      var projectItem = document.createElement('li');
      projectItem.innerHTML =
        `<div class="header">
      <p class="project-name">${projects[i].name}</p>
      <p class="project-owner">${projects[i].owner}</p>
    </div>
    <div class="separator"></div>
    <div class="content">
      <p class="project-description">${projects[i].description}</p>
    </div>
    <div class="footer">
      <div class="project-actions">
        <button class="project-action" onclick="overviewProject('${projects[i].name}')">Overview</button>
        <button class="project-action" style="background-color:#d83131; color:black;" onclick="deleteProject('${projects[i].name}')">Delete</button>
      </div>
      <p class="project-created-at">${projects[i].timestamp}</p>
    </div>`;

      projectList.appendChild(projectItem);
      projectSelect.innerHTML += `<option value="${projects[i].name}">${projects[i].name}</option>`;
    }
  }


});

// project


async function deleteProject(projectName) {
  await eel.delete_project(projectName)();
  projects = projects.filter(project => project.name !== projectName);
  updateProjectList();
}

function updateProjectList() {
  var projectList = document.getElementById('projects');
  var projectSelect = document.getElementById('project-select');

  if (!projectList) {
    console.error('The "projects" element does not exist.');
    return;
  }
  projectList.innerHTML = '';
  projectSelect.innerHTML = '<option value="">Select a project</option>';

  // Add each project to the project list
  for (var i = 0; i < projects.length; i++) {
    // Create a new list item element for the project with project name title and owner as text and createdAt as text
    var projectItem = document.createElement('li');
    projectItem.innerHTML =
      `<div class="header">
      <p class="project-name">${projects[i].name}</p>
      <p class="project-owner">${projects[i].owner}</p>
    </div>
    <div class="separator"></div>
    <div class="content">
      <p class="project-description">${projects[i].description}</p>
    </div>
    <div class="footer">
      <div class="project-actions">
        <button class="project-action" onclick="overviewProject('${projects[i].name}')">Overview</button>
        <button class="project-action" style="background-color:#d83131; color:black;" onclick="deleteProject('${projects[i].name}')">Delete</button>
      </div>
      <p class="project-created-at">${projects[i].timestamp}</p>
    </div>`;
    projectList.appendChild(projectItem);
    projectSelect.innerHTML += `<option value="${projects[i].name}">${projects[i].name}</option>`;
  }
}

function createFolder() {
  var folderName = document.getElementById('projectName').value;
  eel.create_new_folder(folderName);  // Call the Python function
}


async function fetchProjects() {
  let response = await eel.get_projects()();
  return response;
}

function showProjectList() {
  document.getElementById('projectPage1').style.display = 'flex';
  document.getElementById('projectPage2').style.display = 'none';
}

function showAddScreenProject() {
  document.getElementById('projectPage1').style.display = 'none';
  document.getElementById('projectPage2').style.display = 'flex';
}

function checkPhaseImagesAreUploaded() {
  var phaseContainer = document.getElementById('phaseUpload');
  // this holds the value of path of image <p class="label" id="uploadedImageName"></p>
  console.log("checkPhaseImagesAreUploaded -> phaseContainer", phaseContainer)
  if (phaseContainer.hasChildNodes()) {
    var labels = phaseContainer.getElementsByClassName('label');
    console.log("checkPhaseImagesAreUploaded -> labels", labels)

    if (labels.length === 0) {
      alert('Select the number of phases first.');
      return false;
    }
    for (var i = 0; i < labels.length; i++) {
      if (labels[i].textContent === '') {
        alert('Please upload an image for phase ' + (i + 1));
        return false;
      }
    }
    return true;
  }


  return false;
}


function triggerImageSelection(labelId) {
  // Get the label element by its id
  var label = document.getElementById(labelId);

  // Make sure the label element exists
  if (!label) {
    console.error('Label element not found:', labelId);
    return;
  }

  eel.select_image()(function (result) {
    if (result) {
      console.log('File selected:', result);
      label.textContent = result;
    } else {
      console.log('No file was selected.');
    }
  });
}

function checkProjectExists(projectName) {
  projects.map(project => console.log(project.name));
  let isExists = projects.find(project => project.name === projectName);
  console.log("checkProjectExists -> isExists", isExists)
  return isExists;
}




