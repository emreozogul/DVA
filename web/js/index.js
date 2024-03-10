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
    sections.forEach(function(section) {
        section.style.display = 'none';
    });
    
    document.getElementById(sectionId).style.display = 'flex';
}

function nextPageImport() {
    document.getElementById('importPage1').style.display = 'none';
    document.getElementById('importPage2').style.display = 'flex';
}
function prevPageImport() {
  document.getElementById('importPage1').style.display = 'flex';
  document.getElementById('importPage2').style.display = 'none';
}
document.addEventListener('DOMContentLoaded', () => {

  const openbtn = document.getElementById('openbtn');
  openbtn.addEventListener('click', openNav);

  const closebtn = document.getElementById('closebtn');
  closebtn.addEventListener('click', closeNav);

  document.querySelector('.navContainer').addEventListener('click', function(event) {
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



  const dropZone = document.getElementById('dropZone');
  const preview = document.getElementById('preview');
    
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
  });
  
  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }
  
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
  });
  
  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
  });
  
  function highlight(e) {
    dropZone.classList.add('highlight');
  }
  
  function unhighlight(e) {
    dropZone.classList.remove('highlight');
  }
  
  dropZone.addEventListener('drop', handleDrop, false);
  
  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
  
    handleFiles(files);
  }
  
  function handleFiles(files) {
    ([...files]).forEach(previewFile);
  }
  var cropper;

  function initializeCropper(imageSrc) {
    if (cropper) {
        cropper.destroy();
        cropper = null;
      }
  
      // Load the new image
    var image = new Image();
    image.src = imageSrc;
    image.onload = function () {
      canvas.width = image.width;
      canvas.height = image.height;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(image, 0, 0, image.width, image.height);
          
      // Initialize Cropper.js on the image
      cropper = new Cropper(canvas, {
        aspectRatio: 1 / 1, // Optional: Set the aspect ratio
        crop(event) {
          console.log(event.detail.x);
          console.log(event.detail.y);
          console.log(event.detail.width);
          console.log(event.detail.height);
          console.log(event.detail.rotate);
          console.log(event.detail.scaleX);
          console.log(event.detail.scaleY);
        },
      });
    };
  }
  function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
      let img = document.createElement('img');
      img.src = reader.result;
      img.addEventListener('click', () => {initializeCropper( reader.result);});
      preview.appendChild(img);
    };
  }
});

  
