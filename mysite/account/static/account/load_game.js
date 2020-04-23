var canvas = document.getElementById('myGame');
var context = canvas.getContext('2d');
var x_char = 30;
var y_char = 50;
var height = canvas.height;
var width = canvas.width;

function rad(deg) {
  return (Math.PI / 180) * deg;
}

function percentToRad(percent) {
  return rad(270) + rad((360 * percent) / 100);
}

function drawHealth(x, y, percent) {
  context.lineWidth = 5;

  context.beginPath();
  context.strokeStyle = 'rgb(0,0,0)';
  context.arc(x, y, 4, rad(270), percentToRad(100), false);
  context.stroke();

  context.beginPath();
  context.strokeStyle = 'rgba(255,250,0,.8)';
  context.arc(x, y, 4, rad(270), percentToRad(percent), false);
  context.stroke();

  context.beginPath();
  context.fillStyle = 'rgb(0,100,204)';
  context.arc(x, y, 3, 0, 2 * Math.PI, false);
  context.fill();
}

function animate() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  requestAnimationFrame(animate);
  update();
}

drawHealth(10, height - 10 - y_char, 50); //for character 1
drawHealth(width + 10 - x_char, height / 2 - 10, 70); //for character 2
