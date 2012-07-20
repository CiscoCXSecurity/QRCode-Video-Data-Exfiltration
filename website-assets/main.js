var dropbox = document.getElementById('dropbox');
var qrsize = 100;
var dotsize = 8;  // size of box drawn on canvas
var padding = 10; // (white area around your QRCode)
var black = "rgb(0,0,0)";
var white = "rgb(255,255,255)";
var green = "rgb(0,255,0)";
var blue = "rgb(0,0,255)";
// I beleive this variable controls the QR code depth = more bandwidth
// var QRCodeVersion = 15; // 1-40 see http://www.denso-wave.com/qrcode/qrgene2-e.html
var QRCodeVersion = 20; // 1-40 see http://www.denso-wave.com/qrcode/qrgene2-e.html
var delay = 200;
var max_size = 768;

function blankCanvas(color){
    var canvas=document.createElement('canvas');
    var CanvasContext = canvas.getContext('2d');
    canvas.setAttribute('height',(qrsize * dotsize) + padding);
    canvas.setAttribute('width',(qrsize * dotsize) + padding);
    CanvasContext.fillStyle = color;
    CanvasContext.fillRect(padding,padding,qrsize*dotsize,qrsize*dotsize);
    var imgElement = document.createElement("img");
    imgElement.src = canvas.toDataURL("image/png");
    return imgElement;
}

function drawCanvas(canvas){
    canvas_div = document.getElementById('qrcode');
    if(!canvas_div.children.length){
        canvas_div.appendChild(canvas);
    }
    else {
        canvas_div.replaceChild(canvas,canvas_div.children[0]);
    }
} //showQRCode('hello')

function showData(data,offset,depth){
    document.getElementById('status').innerHTML = "offset: " + offset;
    // looped all the way arround
    if(offset >= data.length){
        drawCanvas(blankCanvas(blue));
        setTimeout(function(){
            showData(data,0,depth+1);
        },delay);
    }
    // every other frame draw blank green
    else if(depth % 2){
        drawCanvas(blankCanvas(green));
        setTimeout(function(){
            showData(data,offset,depth+1);
        },delay);
    }
    // every other frame draw data
    else{
        size = data.length - offset;
        if(size > max_size){
            size = max_size;
        }
        chunk = data.slice(offset,offset+size);

        drawCanvas(showQRCode(chunk));
        setTimeout(function(){
            showData(data,offset+size,depth+1);
        },delay);
    }
}

// listen for files
dropbox.addEventListener("drop", function(evt) {
    // stop default actions
    evt.stopPropagation();
    evt.preventDefault();

    // get the files from the event
    files = evt.dataTransfer.files;

    // how many files were dropped
    target_len = files.length;

    // how many files have been loaded
    current_len = 1;

    // new zip container
    zip = new JSZip();

    // loop over the files
    for (i = 0, f=''; f = files[i]; i++) {

        // instantiate new FileReader
        reader = new FileReader();

        // closure to save file info
        reader.onload = (function(f){
            return function(e){

                // add file to archive
                zip.file(f.name,e.target.result,{binary:true});

                // if this is the last file, we generate QR code
                if ( current_len++ >= target_len ) {
                    document.getElementById('dropbox').style.display = 'none';
                    content = zip.generate({base64:false});
                    showData(content,0,0);
                }
            }
        })(f);
        
        // reader.readAsText(f);
        reader.readAsBinaryString(f);
    }
},false);
