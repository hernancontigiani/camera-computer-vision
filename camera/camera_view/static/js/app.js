const row = document.getElementById("rowCanvas");
let mqtt_connected = false;

const baseTopic = `cameracv`

const videoWidth = 416;
const videoHeight = 416;

const consoleOutput = document.getElementById("console");
const log = function (msg) {
    if(consoleOutput != null) {
        consoleOutput.innerText = `${consoleOutput.innerText}\n${msg}`;
    }
    console.log(msg);
}

// ---- MQTT Websockets ----
const mqttBroker = document.location.hostname;
const mqttUser = "";
const mqttPassword = "";

const client = new Paho.MQTT.Client(document.location.hostname, 9001, "iotcameracapture");

// set callback handlers
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    mqtt_connected = true;
    client.subscribe(`${baseTopic}/#`);
}

function doFail(e) {
    log(e.errorCode);
    console.log(e);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  mqtt_connected = false;
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost: " + responseObject.errorMessage);
    }
  }

// called when a message arrives
function onMessageArrived(message) {
  //console.log("onMessageArrived: " + message.destinationName + "  "+ message.payloadString);
  const msg = message.payloadString;
  if(message.destinationName.includes(baseTopic)) {
    const username = message.destinationName.split("/")[1]
    let canvas = document.getElementById(username);
    if(!canvas) {
      const div = document.createElement("div");
      div.classList.add("display-cover");
      div.innerHTML = `<canvas id=${username}></canvas>`;
      row.appendChild(div);
      canvas = document.getElementById(username);
    }
    canvas.width = videoWidth;
    canvas.height = videoHeight;
    let ctx = canvas.getContext('2d');
    const data = JSON.parse(msg);
    const imageData = data["imageData"];
    const image = new Image();
    image.src = imageData;
    image.onload = function() {
      ctx.drawImage(image, 0, 0);
    };
  }
  else {
      console.log("Tópico no soportado: "+ message.destinationName);
  }
}

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
const options = {
  onSuccess: onConnect,
  onFailure: doFail,
  userName: mqttUser,
  password: mqttPassword,
}
// connect the client
client.connect(options);

