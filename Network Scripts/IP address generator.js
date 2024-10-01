function generateRandomIP() {
    let ip = "";
    for (let i = 0; i < 4; i++) {
        let segment = Math.floor(Math.random() * 256);
        // if segment is 0 or 255, try again
        if (segment == 0 || segment == 255) {
            i--;
            continue;
        }
        ip += segment.toString();
        // append a period if not last segment
        if (i != 3) {
            ip += ".";
        }
    }
    return ip;
}

var ip = generateRandomIP();
console.log(ip);