var canvasWith = document.getElementById("canvas").offsetWidth;
var canvasHeight = document.getElementById("canvas").offsetHeight;

var WithOffset = canvasWith/2;
var heightOffset = canvasHeight - 35;

const IP_SERVER = "localhost";
const MAX_POINTS = 100;
const REQUEST_PERIOD = 100; //ms


var cmTopx = 5;
var current_points = {"points": [], "points_number": 0};
var group_name = "group0";


// Function to request the server
function getPointsFromServer() {
    fetch('http://' + IP_SERVER + ':8000/api/get_points?group_name=' + group_name)
        .then(response => response.json())
        .then(data => handleRecivedPoints(data))
        .catch(error => console.error('Error al obtener la lista:', error));
}

function handleRecivedPoints(data) {
    new_points = data.points;
    if (data.points_number <= 0){
        return
    } else {
        console.log(new_points);
        addPoints(new_points);
    }
    writePoints();

}

function writePoints() {
    if (current_points.points_number <= 0) {
        return
    }
    
    //Get the canvas element and its 2D context
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw dots for each point in the list
    current_points.points.forEach(function(point) {
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

function addPoints(new_points) {
    new_points.forEach(function(point) {
        addPoint(point);
    })

}

function addPoint(point) {
    if (current_points.points_number < MAX_POINTS) {
        current_points.points.push(point);
        current_points.points_number += 1;
    } else {
        current_points.points.shift();
        current_points.points.push(point);
    }
}

function fromAngleDistanceToXandY(point) {
    return { "x": WithOffset + cmTopx*point.distance*Math.cos(point.angle), "y": heightOffset - cmTopx*point.distance*Math.sin(point.angle)};
}

function save_group_name() {

    var value = document.getElementById("group_name_input").value.trim();

    var validation = validadeGroupName(value);
    if (validation == true) {
      group_name = encodeURIComponent(value).toLowerCase();
      document.getElementById("current_group").innerText = "Grup actual: " + group_name;
    } else {
      document.getElementById("current_group").innerText = "Si us plau ingresa un valor vàlid abans d'enviar. " + validation;
    }
  }

function validadeGroupName(value) {
    if (value == "") {
        return "El nom del grup no pot ser buit.";   
    } else if (value.length < 6 || value.length > 7) {
        return "El nom del grup introduit és incorrecte.";
    } else if(value.indexOf("group") == -1) {
        return "El nom del grup introduit és incorrecte. A";
    } else {
        return true;
    }
}

document.getElementById("group_name_input").addEventListener("keypress", function(event) {
    if (event.key === 'Enter') {
      document.getElementById("sendButton").click();
    }
});

// Call the function to obtain the points list every second
setInterval(getPointsFromServer, REQUEST_PERIOD);

