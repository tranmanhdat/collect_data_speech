//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record
var arrRecordButton = [];
var arrStopButton = [];
var curId;
var arrBlob = [];
var fileNames = [];
for (var _id of id) {
    var recordButton = document.getElementById("recordButton_" + _id);
    var stopButton = document.getElementById("stopButton_" + _id);
    arrRecordButton.push(recordButton);
    arrStopButton.push(stopButton);
//add events to those 2 buttons
//     recordButton.addEventListener("click", startRecording);
//     stopButton.addEventListener("click", stopRecording);
}

//  arrRecordButton[0].addEventListener("click", function () {
//         startRecording(0);
//     }, false);
// arrRecordButton[1].addEventListener("click", function () {
//         startRecording(1);
//     }, false);
for (let i=0;i<id.length;i++ ) {
    console.log(i);
    arrRecordButton[i].addEventListener("click", function () {
        startRecording(i);
    }, false);
    arrStopButton[i].addEventListener("click", function () {
        stopRecording(i);
    }, false);
}


function startRecording(stt) {
    console.log("recordButton " + stt + " clicked");
    console.log(stt);
    var constraints = {audio: true, video: false};
    arrRecordButton[stt].disabled = true;
    arrStopButton[stt].disabled = false;
    // pauseButton.disabled = false
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        /*  assign to gumStream for later use  */
        gumStream = stream;
        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);
        /*
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input, {numChannels: 1});
        //start the recording process
        rec.record();
        console.log("Recording started");
    }).catch(function (err) {
        //enable the record button if getUserMedia() fails
        arrRecordButton[stt].disabled = false;
        arrStopButton[stt].disabled = true;
        // pauseButton.disabled = true
    });
}


function stopRecording(_id) {
    console.log("stopButton clicked");
    //disable the stop button, enable the record too allow for new recordings
    arrStopButton[_id].disabled = true;
    arrRecordButton[_id].disabled = false;
    // pauseButton.disabled = true;
    //reset button just in case the recording is stopped while paused
    // pauseButton.innerHTML = "Pause";
    //tell the recorder to stop the recording
    rec.stop();
    //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(createDownloadLink);
    curId = _id;
}



function createDownloadLink(blob) {
    console.log("current id : "+curId);
    let filename = user_name+curId+".wav";
    fileNames[curId] = filename;
    arrBlob[curId] = blob;
    let url = URL.createObjectURL(blob);
    let au = document.createElement('audio');
    // var li = document.createElement('li');
    // var link = document.createElement('a');
    //name of .wav file to use during upload and download (without extendion)
    //add controls to the <audio> element
    au.controls = true;
    au.src = url;
    //save to disk link
    // link.href = url;
    // link.download = filename + ".wav"; //download forces the browser to donwload the file using the  filename
    // link.innerHTML = "Save to disk";
    //add the new audio element to li
    // li.appendChild(au);
    //add the filename to the li
    // li.appendChild(document.createTextNode(filename + ".wav "))
    //add the save to disk link to li
    // li.appendChild(link);
    var theDiv = document.getElementById("colWav_"+id[curId]);
    theDiv.innerHTML = '';
    theDiv.append(au);
    //upload link
    // var upload = document.createElement('a');
    // upload.href = "#";
    // upload.innerHTML = "Upload";
    // upload.addEventListener("click", function (event) {
    //     var xhr = new XMLHttpRequest();
    //     xhr.onload = function (e) {
    //         if (this.readyState === 4) {
    //             console.log("Server returned: ", e.target.responseText);
    //         }
    //     };
    //     var fd = new FormData();
    //     fd.append("audio_data", blob, filename);
    //     xhr.open("POST", "/", true);
    //     xhr.send(fd);
    // })
    // li.appendChild(document.createTextNode(" "))//add a space in between
    // li.appendChild(upload)//add the upload link to li
    //
    // //add the li element to the ol
    // recordingsList.appendChild(li);
}

function upload() {
    if (Array.isArray(arrBlob) && arrBlob.length && arrBlob.length == id.length) {
        let xhr = new XMLHttpRequest();
        var fd = new FormData();
        // fd.append("audio_data", arrBlob[0], fileNames[0]);
        for (let j=0;j<id.length;j++){
            fd.append("audio_data", arrBlob[j], fileNames[j]);
            // console.log(arrBlob[j]);
        }
        xhr.open("POST", "http://127.0.0.1:5000/save_audios", true);
        xhr.send(fd);
}
    else{
        alert("Chưa đủ file thu âm!");
    }
}