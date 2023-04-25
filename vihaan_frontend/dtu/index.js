const constraints = {
    video: true,
    audio: true,
};

let mediaRecorder;
let chunks = [];

navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
    const videoElement = document.querySelector("video");
    videoElement.srcObject = stream;
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => chunks.push(event.data);
    mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, {
            type: "video/mp4",
        });
        chunks = [];
        const videoUrl = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = videoUrl;
        console.log(videoUrl);
        console.log(a.href);

        a.download = "recording.mp4";
        a.click();
    };
});

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const pauseBtn = document.getElementById("pauseBtn");
const resumeBtn = document.getElementById("resumeBtn");

startBtn.addEventListener("click", () => {
    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
    pauseBtn.disabled = false;
    resumeBtn.disabled = true;
    resumeBtn.hidden = true;
});

pauseBtn.addEventListener("click", () => {
    mediaRecorder.pause();
    stopBtn.disabled = false;
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    resumeBtn.disabled = false;
    resumeBtn.hidden = false;
    pauseBtn.hidden = true;
});

resumeBtn.addEventListener("click", () => {
    mediaRecorder.resume();
    stopBtn.disabled = false;
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    resumeBtn.disabled = true;
    resumeBtn.hidden = true;
    pauseBtn.hidden = false;
});

stopBtn.addEventListener("click", () => {
    mediaRecorder.stop();
    stopBtn.disabled = true;
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    resumeBtn.disabled = true;
    resumeBtn.hidden = true;
    pauseBtn.hidden = false;
});

function openPage() {
    window.open('index.html', '_self');
}