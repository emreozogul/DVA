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
  nextBtnImport.addEventListener('click', function (event) {
    var allImagesUploaded = checkPhaseImagesAreUploaded();

    if (!allImagesUploaded) {
      console.log('Not all images have been uploaded');
      event.preventDefault();

    } else {
      nextPageImport();
    }

  });

  const prevBtnImport = document.getElementById('prevBtnImport');
  prevBtnImport.addEventListener('click', prevPageImport);


  const sNewProjectBtn = document.getElementById('sNewProjectBtn');
  sNewProjectBtn.addEventListener('click', showAddScreenProject);

  const sProjectListBtn = document.getElementById('sProjectListBtn');
  sProjectListBtn.addEventListener('click', showProjectList);

  const addProjectForm = document.getElementById('addProjectForm');
  addProjectForm.addEventListener('submit', function (event) {
    event.preventDefault();
    addProject();
  });


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

