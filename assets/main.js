var dropbox = document.getElementById('dropbox');
var qrsize = 100;
var dotsize = 5;  // size of box drawn on canvas
var padding = 10; // (white area around your QRCode)
var black = "rgb(0,0,0)";
var white = "rgb(255,255,255)";
var red = "rgb(255,0,0)";
var blue = "rgb(0,0,255)";
var QRCodeVersion = 15; // 1-40 see http://www.denso-wave.com/qrcode/qrgene2-e.html
var delay = 10;
var max_size = 512;

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
            showData(data,0,depth);
        },delay);
    }
    else if(depth % 2){
        drawCanvas(blankCanvas(red));
        setTimeout(function(){
            showData(data,offset,depth+1);
        },delay);
    }
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

dropbox.addEventListener("drop", function(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    files = evt.dataTransfer.files;
    if (files.length > 1){
        // todo: allow multiple files and gzip them
        alert('I can only handle one file at a time....');
        return 0;
    }
    reader = new FileReader();
    reader.onload = function(e){
        document.getElementById('dropbox').style.display = 'none';
        showData(e.target.result,0,0);
    }
    reader.readAsText(files[0]);
},false);
