var canvasWith = document.getElementById("canvas").offsetWidth;
var canvasHeight = document.getElementById("canvas").offsetHeight;



var WithOffset = canvasWith/2;
var heightOffset = canvasHeight - 35;
var cmTopx = 5;


// Función para realizar la solicitud al servidor y mostrar la lista
function getPointsFromServer() {
    fetch('http://192.168.1.50:8000/api/get_points?group_name=group1')
        .then(response => response.json())
        .then(data => writePoints(data.points))
        .catch(error => console.error('Error al obtener la lista:', error));
}

// Función para mostrar la lista en el HTML
function writePoints(points) {
    if (points.length <= 0) {
        return
    }
    
    //Get the canvas element and its 2D context
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    // Draw dots for each point in the list
    points.forEach(function(point) {
        point = fromAngleDistanceToXandY(point);
        console.log(point);
        drawDot(point.x, point.y, ctx);
        
    });
}

function drawDot(x, y, ctx) {
    ctx.beginPath();                      // Start a new path
    ctx.arc(x, y, 5, 0, 2 * Math.PI);   // Create a circle at (x, y) with a radius of 5
    ctx.fillStyle = "red";                // Set the fill color to red
    ctx.fill();                           // Fill the circle with the specified color
    ctx.stroke();                         // Draw the outline of the circle
}

function fromAngleDistanceToXandY(point) {
    return { "x": WithOffset + cmTopx*point.distance*Math.cos(point.angle), "y": heightOffset - cmTopx*point.distance*Math.sin(point.angle)};
}

// Llamar a la función para obtener la lista cada segundo
setInterval(getPointsFromServer, 1000);