window.onload = function () {
    $("#loading-gif").hide();
};

const toServer = function (file) {
    const httpPost = new XMLHttpRequest(),
        url = "/uploadImage",
        formData = new FormData();
    //
    formData.append("image-file", file);
    httpPost.open("POST", url, true);
    //
    $("#loading-gif").show();
    httpPost.onreadystatechange = () => {
        $("#loading-gif").hide();
        if (httpPost.readyState === 4) {
            if (httpPost.status === 200) {
                let data = JSON.parse(httpPost.responseText);
                $("#full-name").html(data["full_name"]);
                $("#number").html(data["number"]);
                $("#birthday").html(data["birthday"]);
                $("#class").html(data["class"]);
                $("#year").html(data["year"]);
                $("#faculty").html(data["faculty"]);
                $("#result-img").attr('src', 'data:image/png;base64,' + data['image']);
                console.log(data);
            } else {
                alert("Failed! :((")
            }
        }
    };
    httpPost.send(formData);
};

$(document).ready(function () {
    $("#input-img").change(function () {
        const selectedFile = this.files[0];
        toServer(selectedFile);
        this.value = null;
    });
});
