document.addEventListener('DOMContentLoaded', () => {
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
  
    function previewFile(file) {
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = function() {
        let img = document.createElement('img');
        img.src = reader.result;
        preview.appendChild(img);
      };
    }
  });
  