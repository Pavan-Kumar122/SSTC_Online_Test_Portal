const video = document.getElementById('video');
let detectAllFaces;
let count = 0;
var imagearr = [];
var canva;
var photo = document.getElementById('img_tag');
var getstream;
const time_limit = $('#time_limit').val();
var delay = time_limit/5;
//

 const getCameraSelection = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const videoDevices = devices.filter(device => device.kind === 'videoinput');
  console.log(videoDevices);
  //const options = videoDevices.map(videoDevice => {
    //return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
  //});
  //cameraOptions.innerHTML = options.join('');
};
 getCameraSelection();
//
Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/static/models')
]).then(startVideo);

function startVideo() {
  navigator.mediaDevices.getUserMedia({ video: true})
    .then(function (stream) {

      video.srcObject = stream;
      getstream = stream;
      video.onloadedmetadata = function(e) {
    video.play();
  };
    })
    .catch(function (err) {
      alert('Please give camera permission !!');
      window.location.reload();
    });
}

video.addEventListener('play', () => {
  var canvas = faceapi.createCanvasFromMedia(video);
  canva = canvas;
  //document.body.append(canvas);
  const displaySize = { width: 240, height: 297 };
  faceapi.matchDimensions(canvas, displaySize);
  detectAllFaces = setInterval(async () => {
      const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions());
      if (detections.length === 1) {
          clearphoto();
          var request = $.ajax({
              url: "/camera",
              method: "POST",
              data: $('form').serialize() + "&datauri="+(imagearr)+ "&test_id="+$('#exam_id').val(),
            });
          request.done(function (data) {
                console.log('ok');
          });
          request.fail(function (data) {
                console.log('err');
          });
    //       $.ajax({
    //    method: 'POST',
    //    url: '/camera',
    //    data: {datauri: imagearr, test_id: $('#exam_id').val()},
    //     success: function (data) {
    //        console.log('ok');
    //     },
    //     error: function (data) {
    //         console.log('no');
    //     }
    // });
          imagearr = [];
      }
      console.log(detections.length);
      const resizedDetections = faceapi.resizeResults(detections, displaySize);
      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)

    }, delay*1000)
  });

function clearphoto() {
  canva.getContext('2d').drawImage(video,0,0, 240,297);
  var data = canva.toDataURL('image/jpeg', 0.5);
  console.log(btoa(data));
  imagearr.push(btoa(data));//// <----
  // photo.src = data;
  count++;
  if (count === 5){
    getstream.getVideoTracks()[0].stop();
    console.log("length"+imagearr.length);
    clearInterval(detectAllFaces);
  }
}
