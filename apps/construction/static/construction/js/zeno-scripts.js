// test function that writes out a string
function halloballo(name) {
    document.write("Halloballo" + name);
}

// draws frame on canvas
function draw_frame() {
    var canvas = document.getElementById('goalsystem');
    w = canvas.width
    h = canvas.height
    a = 10
    b = 20
    if (canvas.getContext) {
        var ctx = canvas.getContext('2d');
        ctx.fillRect(a, a, w - (2 * a), h - (2 * a));
        ctx.clearRect(2 * a, 2 * a, w - (4 * a), (h - (4 * a)));
    }
}
