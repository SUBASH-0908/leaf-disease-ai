const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");
const preview = document.getElementById("preview");

dropArea.addEventListener("dragover", e=>{
e.preventDefault();
dropArea.style.background="#e8ffe8";
});

dropArea.addEventListener("dragleave", ()=>{
dropArea.style.background="white";
});

dropArea.addEventListener("drop", e=>{
e.preventDefault();

const file = e.dataTransfer.files[0];
fileInput.files = e.dataTransfer.files;

showPreview(file);
});

fileInput.addEventListener("change", ()=>{
showPreview(fileInput.files[0]);
});

function showPreview(file){

const reader = new FileReader();

reader.onload = function(e){
preview.src = e.target.result;
preview.style.display="block";
}

reader.readAsDataURL(file);
}