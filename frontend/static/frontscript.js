var GLOBAL_FLAG = 0
var FILE_STATUS = 0
var REFRESHMENT = 0
var RECORD_FLAG = 0
var REGIME_FLAG = 0

function saveFile(name, type, data) {
    if (data != null && navigator.msSaveBlob) {
        return navigator.msSaveBlob(new Blob([data], {type: type}), name);
    }
    let a = $("<a style='display: none;'/>");
    let url = window.URL.createObjectURL(new Blob([data], {type: type}));
    a.attr("href", url);
    a.attr("download", name);
    $("body").append(a);
    a[0].click();
    window.URL.revokeObjectURL(url);
    a.remove();
}

navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {
    handlerFunction(stream)
})

function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
        audioChunks.push(e.data);
        if (rec.state == "inactive") {
            let blob = new Blob(audioChunks, {type: 'audio/wav'});
            saveFile("Example.mp3", 'audio/wav', blob);

            let formData = new FormData();
            formData.append("fname", "record.wav");
            formData.append("file", blob);
            let url = '/upload'
            fetch(url, {
                method: 'POST',
                body: formData
            })
                .then((response) => {
                    return response;
                }).then((response) => {
                    return response.text()
                }).then((data) => {
                    alert(data)
                    let res = data.split(";");
                    alert(res[0])
                    document.getElementsByTagName("p")[0].innerHTML = res[0]
                    document.getElementsByTagName("p")[1].innerHTML = res[1]
            }).catch(() => {})

        }
    }
}

function checkStatus() {
    FILE_STATUS = document.getElementById("image-file").files.length;
    //   alert(document.getElementById("image-file").files.length)
    if ((FILE_STATUS != 0) && (REFRESHMENT == 1)) {

        let file = document.getElementById("image-file").files[0];
        let formData = new FormData();
        formData.append("file", file);
//        alert();
        let url = '/upload'
        let marker = 0;
        fetch(url, {
            method: 'POST',
            body: formData
        })
            .then((response) => {
                return response
            }).then((response) => {
           //         alert(response.headers.get("word"))
                    if (response.headers.get("word") == "yes") {
                        marker = 1;
                        return response.blob();
                    } else {
                        if (response.headers.get("word") == "no") {
                            marker = 2;
                            return response.blob();
                        } else {
                            return response.text();
                        }
                    }
                }).then((data) => {
         //           alert(marker)
                    if (marker == 1) {
                        saveFile("Converted_.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", data);
                    }
                    if (marker == 2) {
                        saveFile("Converted_.odt", "application/vnd.oasis.opendocument.text", data);
                    } else {
                        let res = data.split(";");
                        document.getElementsByTagName("p")[0].innerHTML = res[0];
                        document.getElementsByTagName("p")[1].innerHTML = res[1];
                    }
                    }).catch(() => {})
        REFRESHMENT = 0;
    }
}


window.onload = function () {


    record = document.getElementById("record");
    record_circle = document.getElementsByClassName("red_circle")[0];
    record.onclick = e => {

        if (RECORD_FLAG == 0) {
            console.log('Enabled')
            record.disabled = true;
            record_circle.style.backgroundColor = "white"
            record.disabled = false;
            audioChunks = [];
            rec.start();
            RECORD_FLAG = 1;
        } else {
            console.log("Disabled");
            record.disabled = false;
            stop.disabled = true;
            record_circle.style.backgroundColor = "red"
            rec.stop();
            RECORD_FLAG = 0;
        }
    }

    $(".textareas").click(function () {
        if (REGIME_FLAG == 0) {
            REGIME_FLAG = 1;
            $(".req").fadeOut(1000);
            setTimeout(function () {
                document.getElementsByClassName("req")[0].innerHTML = 'нажмите для обработки фрагмента текста';
            }, 1000);
            $(".req").fadeIn(1000);
        }
    });


    $("#button-back").click(function () {
        alert()
        $("body").fadeOut(1000);
        setTimeout(function () {
            location.href = "/"
        }, 1500);
    });

    $("body").fadeOut(1)
    $("body").fadeIn(1200)

    let fake = $('.req')


    fake.click(function (e) {
        if (REGIME_FLAG == 1) {
            REGIME_FLAG = 0;
            $(".req").fadeOut(1000);


            setTimeout(function () {
                document.getElementsByClassName("req")[0].innerHTML = 'нажмите на надпись или перетяните файл на экран';
            }, 1000);

            $(".req").fadeIn(1000);


            let url = '/submit'
            let formData = new FormData()
            formData.append('text', document.getElementsByTagName("p")[0].innerHTML)
            fetch(url, {
                method: 'POST',
                body: formData
            }).then((response) => {
                return response.text()
            }).then((data) => {
                document.getElementsByTagName("p")[1].innerHTML = data
            }).catch(() => {
            })
        } else {
            e.preventDefault()
            $('#image-file').trigger('click');
            REFRESHMENT = 1;
        }
    })
    setInterval(checkStatus, 1);


    let dropArea = document.getElementById('dropzone')

    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false)
    })

    function preventDefaults(e) {
        e.preventDefault()
        e.stopPropagation()
    }

    ;['dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false)
    })
    ;['drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false)
    })

    function highlight(e) {
        $(".zone").fadeIn(300)
    }

    function unhighlight(e) {
        $(".zone").fadeOut(300)
    }

    function uploadFile(file) {
        $(".req").fadeOut(300)
        let url = '/upload'
        let formData = new FormData()
        formData.append('file', file)

        fetch(url, {
            method: 'POST',
            body: formData
        })
            .then((response) => {
                return response
            }).then((response) => {
            return response.text()
        }).then((data) => {
            document.getElementsByTagName("p")[1].innerHTML = data
        }).catch(() => {
        })
    }

    function handleFiles(files) {
        ([...files]).forEach(uploadFile)
    }

    dropArea.addEventListener('drop', handleDrop, false)

    function handleDrop(e) {
        let dt = e.dataTransfer
        let files = dt.files
        handleFiles(files)
    }

};
