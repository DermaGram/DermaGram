function move() {
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, 2500);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
} 
