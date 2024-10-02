class Main {
    constructor ({loginEndpoint, maxDataCount, maxNumbers = Infinity}) {
        this.maxNumbers = maxNumbers;
        this.maxDataCount = maxDataCount;
        this.loginEndpoint = loginEndpoint;
        this.mqttClient = "";
        this.chart = [];
        this.batt = [];
        this.topicData = "";
        this.labelData = "";
        this.payloadData = "";
        this.key = "";
        this.value = "";
        

        this._mqttConnect();
        this._mqttMessage();
        this._initCharts();

        //Initialize buttons
        this.sidebarBtn();
        this.promptBtn();
    }
    
    _mqttConnect() {
        this.mqttClient = mqtt.connect('wss://mqtt.flespi.io',{
            will: {
                topic: 'hello',
                payload: '100',
                qos: 0,
                retain: true,
                properties: {
                    willDelayInterval: 120 /* MQTT 5.0 property saying how many seconds to wait before publishing the LWT message */
                }
            },
            protocolVersion: 5,
            username: 'LCs6YZ8voHXTsbaxne2lduvjLmfePR51SAvrBqZMyUKZNovaS62jxOP3jkLsH4xe'
        });
        this.mqttClient.on("connect", () => {
            this.mqttClient.subscribe(["temperature", "yolo"], (err) => {
                if (!err) {
                    console.log("Connected Successfully");
                }
                else {
                    console.log("Connection Failed");
                }
            });
            
        });
    }

    _mqttMessage() {
        this.mqttClient.on("message", (topic, payload, packet) => {
            // Message Buffer
            const UnixTimestamp = packet.properties.userProperties.timestamp; // start with a Unix timestamp
            const myDate = new Date(UnixTimestamp * 1000).toLocaleString({hour12:false}).split(" "); // convert timestamp to milliseconds and construct Date object
            var time = myDate[1];
            var mdy = myDate[0];
        
            mdy = mdy.split('/');
            const month = parseInt(mdy[0]);
            const day = parseInt(mdy[1]);
            const year = parseInt(mdy[2]);
            this.labelData = `${month}/${day}/${time}`;
            this.topicData = topic;
            this.payloadData = payload.toString();
            
            // console.log(`Message: ${this.payloadData}, QoS: ${packet.qos}`);

            // Functions to distribute message coming from mqtt
            switch (this.topicData.toString()) {
                    
                case"yolo":
                    // console.log(`Message: ${this.payloadData}, QoS: ${packet.qos}`);
                    document.getElementById("alert").innerHTML += `<span class='sub-toggle-text-mqtt'>
                    MESSAGE:${this.payloadData}, QoS: ${packet.qos}</span><br>`;
                    break;
                    
                case "temperature":
                    this.addChartData(this.topicData.toString(),this.labelData,this.payloadData);
                    if(this.chart[this.topicData.toString()].data.labels.length > this.maxDataCount) {
                        this.removeChartFirstData(this.topicData.toString());
                    }
                    break;
            }
        })
    }
    
    // BUTTONS
    sidebarBtn() {
        let sideBtnInner = document.querySelector(".menu-icon");
        let sideBtnOuter = document.querySelector(".menu-outer");
        let sidebar = document.querySelector("#sidebar");

    //allow element to adjust dynamically based on sidebar size
        const gauge = document.querySelectorAll("#gauge");
        const appliance = document.querySelectorAll(".appliance-card");
        const solar = document.querySelectorAll(".pv-card");
        const canvas = document.querySelectorAll(".canvas-card");
        
        sideBtnInner.onclick = () => {
            sidebar.classList.toggle("active");
        }
        sideBtnOuter.onclick = () => {
            sidebar.classList.toggle("active");
        }
    }

    promptBtn() {
        const buttons = document.querySelectorAll(".prompt-btn");
        buttons.forEach(el => 
            { el.addEventListener("click", () => {
                this._unlockPrompt()});
            })
    }

    //PROMPT FEATURES
    _unlockPrompt() {
        const alert = document.getElementById("mainPinpad");
        alert.style.top = '-40%';
        alert.style.opacity = 0;
        document.getElementById('freezeLayer').style.display = 'none';
    }

    //CHART FEATURES
    _initCharts() {
        const charts = document.querySelectorAll(".chart-data");
        charts.forEach((el, index) => {
            this.chart.push(el.id);
            index = document.getElementById(el.id).getContext("2d");
            index.beginPath();
            index.setLineDash([]);
            index.lineTo(900, 600);
            
            this.chart[el.id] = new Chart(index, {
                type: "line",
                data: {datasets: [{ label: `${el.id.toUpperCase()}`,}],
            },
                options: {
                    legend: {labels:{color: 'white'}},
                    maintainAspectRatio: false,
                    responsive: true,
                    borderWidth: 1,
                    borderColor: ['rgba(255, 99, 132, 1)',],
                    scales: {
                        x: {
                            display: true,
                            grid: {
                                color: "#D3D3D3"
                                }
                            },
                        y: {
                            display: true,
                            grid: {
                                color: "#D3D3D3"
                            },
                        }
                    }
                }
            })
        })
    }
    // Add/Remove Data in Charts
    addChartData(arrVar, label, data) {
        this.chart[arrVar].data.labels.push(label);
        this.chart[arrVar].data.datasets.forEach((dataset) => {
            dataset.data.push(data);
        });
        this.chart[arrVar].update();
    }

    removeChartFirstData(arrVar) {
        this.chart[arrVar].data.labels.splice(0, 1);
        this.chart[arrVar].data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
    }
    
}