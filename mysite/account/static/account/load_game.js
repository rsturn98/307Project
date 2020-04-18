
var canvas = document.getElementById("myGame");
var context = canvas.getContext("2d")
var x_char = 30;
var y_char = 50;

/*function drawCharacter() 
{
    var image1 = new Image();
    image1.src = "bard-drawing-5.png";
    var image2 = new Image();
    image2.src = "bard-drawing-4.png";
    context.imageSmoothingEnabled = false;
    image1.onload = function(){context.drawImage(image1, 0, 200-y_char, x_char, y_char); }
    image2.onload = function(){ context.drawImage(image2, 200-x_char, 100, x_char, y_char);}

} */
//resource: https://veerasundar.com/blog/2014/10/canvas-drawing-circle-meter-wi

function rad(deg)
{
    return (Math.PI/180)*deg;
}

function percentToRad(percent)
{
    return rad(270) + rad ((360 * percent) / 100);
}

function drawHealth(x,y, percent)
{
    
    context.lineWidth = 5;
    
    context.beginPath();    
    context.strokeStyle ='rgb(0,0,0)';
    context.arc(x,y, 4, rad(270), percentToRad(100), false);
    context.stroke();
    
    context.beginPath();
    context.strokeStyle = 'rgba(255,250,0,.8)';//'rgba(255,65,54,.8)';
    context.arc(x, y, 4, rad(270), percentToRad(percent), false);
    context.stroke();
    
    context.beginPath();
    context.fillStyle = 'rgb(0,100,204)';
    context.arc(x,y, 3, 0, 2*Math.PI, false);
    context.fill();
}

function animate(){
    context.clearRect(0,0,canvas.width,canvas.height);
    requestAnimationFrame(animate);
    update();
}

    //window.addEventListener ? 
    //window.addEventListener("load",drawCharacter,false) : 
    //window.attachEvent && window.attachEvent("onload",drawCharacter);
    drawHealth(10, 190-y_char, 50);//for character 1
    drawHealth(210-x_char, 90, 70); //for character 2

