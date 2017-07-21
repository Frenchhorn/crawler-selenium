function getDataURL2 (css_selector) {

    var encode = function (str) {
        var BASE64_ENCODE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        var out = "", i = 0, len = str.length, c1, c2, c3;
        while (i < len) {
            c1 = str.charCodeAt(i++) & 0xff;
            if (i === len) {
                out += BASE64_ENCODE_CHARS.charAt(c1 >> 2);
                out += BASE64_ENCODE_CHARS.charAt((c1 & 0x3) << 4);
                out += "==";
                break;
            }
            c2 = str.charCodeAt(i++);
            if (i === len) {
                out += BASE64_ENCODE_CHARS.charAt(c1 >> 2);
                out += BASE64_ENCODE_CHARS.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
                out += BASE64_ENCODE_CHARS.charAt((c2 & 0xF) << 2);
                out += "=";
                break;
            }
            c3 = str.charCodeAt(i++);
            out += BASE64_ENCODE_CHARS.charAt(c1 >> 2);
            out += BASE64_ENCODE_CHARS.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += BASE64_ENCODE_CHARS.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
            out += BASE64_ENCODE_CHARS.charAt(c3 & 0x3F);
        }
        return out;
    };

    var sendAJAX = function (url, method, data, async, settings) {
        var xhr = new XMLHttpRequest(),
            dataString = "",
            dataList = [];
        method = method && method.toUpperCase() || "GET";
        var contentType = settings && settings.contentType || "application/x-www-form-urlencoded";
        xhr.open(method, url, !!async);
        xhr.overrideMimeType("text/plain; charset=x-user-defined");
        if (method === "POST") {
            if (typeof data === "object") {
                for (var k in data) {
                    dataList.push(encodeURIComponent(k) + "=" + encodeURIComponent(data[k].toString()));
                }
                dataString = dataList.join('&');
            } else if (typeof data === "string") {
                dataString = data;
            }
            xhr.setRequestHeader("Content-Type", contentType);
        }
        xhr.send(method === "POST" ? dataString : null);
        return encode(xhr.responseText);
    };

    var image = document.querySelector(css_selector)
    var url = image.src

    return sendAJAX(url)
}
