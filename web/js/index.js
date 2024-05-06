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
var activeProject = null;

document.addEventListener('DOMContentLoaded', async () => {
  projects = await loadProjects();
  updateProjectList();

  document.getElementById('openbtn').addEventListener('click', openNav);

  document.getElementById('closebtn').addEventListener('click', closeNav);

  document.getElementById('sNewProjectBtn').addEventListener('click', showAddScreenProject);

  document.getElementById('sProjectListBtn').addEventListener('click', showProjectList);

  document.querySelector('.navContainer').addEventListener('click', function (event) {
    if (event.target.classList.contains('navItem')) {
      var sectionId = event.target.getAttribute('data-section');
      showSection(sectionId);
    }
  });

  document.getElementById("importForm").addEventListener('submit', async function (event) {
    event.preventDefault();
    var select = document.getElementById("project-select");
    var projectName = select.options[select.selectedIndex].value;
    var phaseQuantity = document.querySelector('.choicebox-container input[type="radio"][name="radio"]:checked').value;
    var scaleSelects = document.querySelectorAll('.import-custom-select');
    var cellName = document.getElementById('cellName').value;
    var scaleValues = [];
    scaleSelects.forEach(function (select) {
      scaleValues.push(select.querySelector('.scale-select').value);
    });

    if (projectName === '' || projectName === undefined || projectName === null || projectName === "Select a project") {
      openModal('Import', 'Select a project first.', 'error');
      return;
    } else if (phaseQuantity === '' || phaseQuantity === undefined || phaseQuantity === null) {
      openModal('Import', 'Select the number of phases first.', 'error');
      return;
    } else if (!checkPhaseImagesAreUploaded()) {
      openModal('Import', 'Upload images for each phase.', 'error');
      return;
    }

    try {
      var phaseContainer = document.getElementById('phaseUpload');
      var imagePaths = [];
      if (phaseContainer.hasChildNodes()) {
        var labels = phaseContainer.getElementsByClassName('label');
        for (var i = 0; i < labels.length; i++) {
          imagePaths.push(labels[i].textContent);
        }
      }
      var res = await eel.import_images(projectName, cellName, imagePaths, scaleValues)();
      var resultPage = document.getElementById("importPageResult");
      var importPage = document.getElementById("importPageInput");
      resultPage.style.display = 'flex';
      importPage.style.display = 'none';
      showResults(res);
    } catch (error) {
      console.error('An error occurred:', error);
      openModal('Import', 'Failed to import images. Please try again.', 'error');
    }
  });


  document.getElementById('backOverviewButton').addEventListener('click', function () {
    document.getElementById('projectPage1').style.display = 'none';
    document.getElementById('projectPage2').style.display = 'none';
    document.getElementById('projectPageOverview').style.display = 'none';
    showProjectList();
  });

  document.getElementById("exportBtn").addEventListener('click', async function () {
    let res = await eel.export_data(activeProject)();
    if (res) {
      openModal('Export', 'Data exported successfully.', 'success');
    } else {
      openModal('Export', 'Failed to export data.', 'error');
    }
  });

  document.getElementById("importToProject").addEventListener('click', function () {
    document.getElementById('Import').style.display = 'none';
    document.getElementById('Project').style.display = 'flex';
    showProjectList();

  });

  document.getElementById("resultToImport").addEventListener('click', function () {
    document.getElementById('importPageResult').style.display = 'none';
    document.getElementById('importPageInput').style.display = 'flex';

  });



  function clearOverviewTable() {
    // Clear previous project data
    var tableBody = document.getElementById("overviewTableBody");
    tableBody.innerHTML = "";
  }

  function displayProjectData(projectData) {
    var tableBody = document.getElementById("overviewTableBody");
    projectData.forEach(function (project) {
      var row = document.createElement("tr");
      var nameCell = document.createElement("td");
      nameCell.textContent = project.name;
      var ownerCell = document.createElement("td");
      ownerCell.textContent = project.owner;
      var descriptionCell = document.createElement("td");
      descriptionCell.textContent = project.description;
      row.appendChild(nameCell);
      row.appendChild(ownerCell);
      row.appendChild(descriptionCell);
      tableBody.appendChild(row);
    });
  }




  var modal = document.getElementById("myModal");
  var btn = document.getElementById("HelpNav");
  var span = document.getElementsByClassName("close")[0];
  btn.onclick = function () {
    modal.style.display = "block";
    var helpContent = "This is a help message.";
    openModal('Help', helpContent, 'plain');
  }
  span.onclick = function () {
    modal.style.display = "none";
    clearModal();
  }
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
      clearModal();
    }
  }


  function updatePhaseUpload(phaseQuantity) {
    const phaseUploadDiv = document.getElementById('phaseUpload');

    phaseUploadDiv.innerHTML = null;

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
        <div class="column">
          <div class="row" >
            <div class="phase-image-upload-button" data-label-id="image-path-1">Phase 1</div>
            <div class="import-custom-select">
              <select class="scale-select">
                  <option value="4x">4x</option>
                  <option value="10x">10x</option>
                </select>
            </div>
          </div>
          <div class="row" >
            <p class="label" id="image-path-1"></p>
          </div>
        </div>
        <div class="column">
          <div class="row" >
            <div class="phase-image-upload-button" data-label-id="image-path-2">Phase 2</div>
            <div class="import-custom-select">
              <select class="scale-select">
                  <option value="4x">4x</option>
                  <option value="10x">10x</option>
                </select>
            </div>
          </div>
          <div class="row" >
            <p class="label" id="image-path-2"></p>
          </div>
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
        <div class="column">
          <div class="row" >
            <div class="phase-image-upload-button" data-label-id="image-path-1">Phase 1</div>
            <div class="import-custom-select">
              <select class="scale-select">
                  <option value="4x">4x</option>
                  <option value="10x">10x</option>
                </select>
            </div>
          </div>
          <div class="row" >
            <p class="label" id="image-path-1"></p>
          </div>
        </div>
        <div class="column">
          <div class="row" >
            <div class="phase-image-upload-button" data-label-id="image-path-2">Phase 2</div>
            <div class="import-custom-select">
              <select class="scale-select">
                  <option value="4x">4x</option>
                  <option value="10x">10x</option>
                </select>
            </div>
          </div>
          <div class="row" >
            <p class="label" id="image-path-2"></p>
          </div>
        </div>
        <div class="column">
          <div class="row" >
            <div class="phase-image-upload-button" data-label-id="image-path-3">Phase 3</div>
            <div class="import-custom-select">
              <select class="scale-select">
                  <option value="4x">4x</option>
                  <option value="10x">10x</option>
                </select>
            </div>
          </div>
          <div class="row" >
            <p class="label" id="image-path-3"></p>
          </div>
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
      openModal('Add Project', 'Project already exists.', 'error');
      return;
    }
    var newProject = {
      owner: owner,
      name: projectName,
      description: description,
      timestamp: new Date().toLocaleString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    };

    await eel.add_project(projectName, owner, description)();
    projects.push(newProject);

    updateProjectList();
    document.getElementById('authorAdd').value = '';
    document.getElementById('projectNameAdd').value = '';
    document.getElementById('descriptionAdd').value = '';
    showProjectList();
  });

  function showResults(res) {
    try {
      var container = document.getElementById("import-result-container");
      container.innerHTML = ''; // Clear previous results
      if (Array.isArray(res)) {
        res.forEach((phase, index) => {
          const card = document.createElement("div");
          card.className = "import-result-card";

          function formatNumber(value) {
            return value !== undefined && value !== null ? value.toFixed(2) : 'N/A';
          }
          const cardHTML = `
                    <div class="header">
                        <h2>Results of Phase ${phase.phaseNo}</h1>
                        <p>${phase.viability !== undefined ? phase.viability : 'Unknown Viability'}</h2>
                    </div>
                    <div class="footer">
                      <div class = "result-actions">
                        <button id="viewResults-${index}" class="result-action">View Results</button>
                        <button id="addToModel-${index}" class="result-action">Add to the Model</button>
                      </div>
                    </div>
                `;
          card.innerHTML = cardHTML;
          container.appendChild(card);
          var roundness = phase.roundness * 100;
          document.getElementById(`viewResults-${index}`).addEventListener('click', () => {
            const viewResultContent = `
                        <div style="display:flex; flex-direction:column; gap:6px; font-weight:bold;">
                            <p><strong>Area:</strong> ${formatNumber(phase.area)} mm²</p>
                            <p><strong>Perimeter:</strong> ${formatNumber(phase.perimeter)} mm</p>
                            <p><strong>Diameter:</strong> ${formatNumber(phase.diameter)} mm</p>
                            <p><strong>Roundness:</strong> ${formatNumber(roundness)}</p>
                            <p><strong>Aspect Ratio:</strong> ${formatNumber(phase.aspectRatio)}</p>
                            <p><strong>Solidity:</strong> ${formatNumber(phase.solidity)}</p>
                            <p><strong>Convexity:</strong> ${formatNumber(phase.convexity)}</p>
                            <p><strong>Particles:</strong> ${phase.particles !== undefined ? phase.particles : 'N/A'}</p>
                            <p><strong>Scale:</strong> ${phase.scale !== undefined ? phase.scale : 'N/A'}</p>
                        </div>`;
            openModal('View Results', viewResultContent, 'plain');
          });
          document.getElementById(`addToModel-${index}`).addEventListener('click', () => {
            openModal('Add to the Model', '', 'plain');
          });
        });
      } else {
        console.error('Expected an array for response, received:', res);
      }
    } catch (error) {
      console.error('Failed to fetch result data:', error);
    }
  }
});


function updateProjectList() {
  var projectList = document.getElementById('projects');
  var projectSelect = document.getElementById('project-select');

  projectList.innerHTML = '';
  projectSelect.innerHTML = '<option value="">Select a project</option>';

  for (var i = 0; i < projects.length; i++) {
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

function showProjectList() {
  document.getElementById('projectPageOverview').style.display = 'none';
  document.getElementById('projectPage1').style.display = 'flex';
  document.getElementById('projectPage2').style.display = 'none';
}

function showAddScreenProject() {
  document.getElementById('projectPageOverview').style.display = 'none';
  document.getElementById('projectPage1').style.display = 'none';
  document.getElementById('projectPage2').style.display = 'flex';
}

function checkPhaseImagesAreUploaded() { // 
  var phaseContainer = document.getElementById('phaseUpload');
  if (phaseContainer.hasChildNodes()) {
    var labels = phaseContainer.getElementsByClassName('label');
    if (labels.length === 0) {
      openModal('Import', 'Upload images for each phase.', 'error');
      return false;
    }
    for (var i = 0; i < labels.length; i++) {
      if (labels[i].textContent === '') {
        openModal('Import', ('Please upload an image for phase ' + (i + 1)), 'error');
        return false;
      }
    }
    return true;
  }
  return false;
}


function triggerImageSelection(labelId) { // 
  var label = document.getElementById(labelId);
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
  return projects.find(project => project.name === projectName);
}

async function overviewProject(projectName) {
  try {
    activeProject = projectName;
    const pageSize = 12;
    const totalCount = await eel.get_total_cells_count(projectName)();
    const maxPages = Math.ceil(totalCount / pageSize);

    var currentPage = 1;
    var projectData = await eel.paginate_project_data(projectName, currentPage, pageSize)();

    const tableContent = document.getElementById('tableContent');
    const buttonContainer = document.getElementById('overviewProjectButtons');

    setupUI(projectName, tableContent, buttonContainer, projectData, currentPage, maxPages, pageSize);

  } catch (error) {
    console.error('Failed to fetch project data:', error);
  }
}

function setupUI(projectName, tableContent, buttonContainer, projectData, currentPage, maxPages, pageSize) {
  document.getElementById('projectPage1').style.display = 'none';
  document.getElementById('projectPage2').style.display = 'none';
  document.getElementById('projectPageOverview').style.display = 'flex';

  fillTable(tableContent, projectData);

  buttonContainer.innerHTML = `
      <div class="button small" id="paginateBackward"><svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M8 5L3 10L8 15" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M3 10H11C16.5228 10 21 14.4772 21 20V21" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg></div>
      <div class="button small" id="paginateForward"> <svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M16 5L21 10L16 15" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M21 10H13C7.47715 10 3 14.4772 3 20V21" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg></div>
    `;

  document.getElementById("paginateForward").addEventListener('click', async () => {
    if (currentPage < maxPages) {
      currentPage++;
      projectData = await eel.paginate_project_data(projectName, currentPage, pageSize)();
      fillTable(tableContent, projectData);
    } else {
      openModal('Pagination', 'No more data to display.', 'error');
    }
  });

  document.getElementById("paginateBackward").addEventListener('click', async () => {
    if (currentPage > 1) {
      currentPage--;
      projectData = await eel.paginate_project_data(projectName, currentPage, pageSize)();
      fillTable(tableContent, projectData);
    } else {
      openModal('Pagination', 'No more data to display.', 'error');
    }
  });
}

function fillTable(tableContent, projectData) {
  tableContent.innerHTML = '';
  if (Array.isArray(projectData)) {
    projectData.forEach(data => {
      const row = document.createElement('tr');
      let dataRoundnessOverHundreds = data.roundness * 100;
      row.innerHTML = `
        <td>${data.cellName}</td>
        <td>${parseFloat(data.area).toFixed(2)}</td>
        <td>${parseFloat(data.perimeter).toFixed(2)}</td>
        <td>${parseFloat(dataRoundnessOverHundreds).toFixed(2)}%</td>
        <td>${data.particleCount}</td>
        <td>${data.viability}</td>
      `;
      tableContent.appendChild(row);
    });
  } else {
    console.error('Expected an array for project data, received:', projectData);
  }
}


function openModal(title, content, type) {
  var modal = document.getElementById("myModal");
  var modalTitle = document.getElementById("modalTitle");
  var modalContent = document.getElementById("modalContent");

  modalTitle.textContent = title;
  modalContent.innerHTML = content;

  if (type === 'success') {
    modalBody.style.color = 'green';
  }
  else if (type === 'error') {
    modalBody.style.color = 'red';
  } else if (type === 'plain') {
    modalBody.style.color = 'black';
  }

  modal.style.display = "block";
}

function clearModal() {
  var modal = document.getElementById("myModal");
  var modalTitle = document.getElementById("modalTitle");
  var modalContent = document.getElementById("modalContent");

  modalTitle.textContent = '';
  modalContent.textContent = '';
}