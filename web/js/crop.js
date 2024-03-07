const fileInput = document.getElementById('fileInput');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const cropButton = document.getElementById('cropButton');

let image;
let isCropping = false;
let startX, startY, endX, endY;

// Kullanıcının yüklediği fotoğrafı al
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      image = new Image();
      image.src = event.target.result;
      image.onload = () => {
        drawImageScaled(image, ctx, canvas);
      }
    };
    reader.readAsDataURL(file);
  }
});

// Kırpma işlemine başlama ve görsel geri bildirim sağlama
canvas.addEventListener('mousedown', (e) => {
  isCropping = true;
  startX = e.offsetX;
  startY = e.offsetY;
});

canvas.addEventListener('mousemove', (e) => {
  if (isCropping) {
    // Geçici olarak kırpma alanını göster
    drawImageScaled(image, ctx, canvas); // Resmi yeniden çiz
    ctx.strokeStyle = '#FF0000'; // Kırpma alanının rengi
    ctx.lineWidth = 2;
    ctx.strokeRect(startX, startY, e.offsetX - startX, e.offsetY - startY);
  }
});

// Kırpma işlemini gerçekleştirme
canvas.addEventListener('mouseup', (e) => {
  if (isCropping) {
    isCropping = false;
    endX = e.offsetX;
    endY = e.offsetY;
    cropImage(startX, startY, endX - startX, endY - startY);
  }
});

// Kırpma işlemini tetikleme
cropButton.addEventListener('click', () => {
  if (endX > startX && endY > startY) { // Kırpma koordinatlarını kontrol et
    cropImage(startX, startY, endX - startX, endY - startY);
  }
});

// Fotoğrafı canvas'a ölçekli olarak çizme
function drawImageScaled(img, ctx, canvas) {
  const hRatio = canvas.width / img.width;
  const vRatio = canvas.height / img.height;
  const ratio = Math.min(hRatio, vRatio);
  const centerShiftX = (canvas.width - img.width * ratio) / 2;
  const centerShiftY = (canvas.height - img.height * ratio) / 2;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, img.width, img.height, centerShiftX, centerShiftY, img.width * ratio, img.height * ratio);
}

// Kırpma işlemini gerçekleştirme
function cropImage(x, y, width, height) {
  // Kırpılmış fotoğrafı al
  const croppedImage = document.createElement('canvas');
  const croppedCtx = croppedImage.getContext('2d');
  croppedImage.width = width;
  croppedImage.height = height;
  croppedCtx.drawImage(image, x, y, width, height, 0, 0, width, height);
  
  // Kırpılmış fotoğrafı bir <img> öğesine yerleştirme (opsiyonel)
  const croppedImgElement = document.createElement('img');
  croppedImgElement.src = croppedImage.toDataURL();
  document.body.appendChild(croppedImgElement); // Sayfanın sonuna ekler
}