function pushStack(str) {
    var xhr = new XMLHttpRequest();
    var url = "https://stack-string.herokuapp.com/PushStack?string=" + encodeURIComponent(str);
    xhr.open("POST", url, true);
    xhr.send("");
}

function popStack() {
    var xhr = new XMLHttpRequest();
    var url = "https://stack-string.herokuapp.com/PopStack"
    xhr.open("GET", url, false);
    xhr.send("");
    console.log(xhr.response);
}
