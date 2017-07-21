function getDataURL (css_selector) {
    var image = document.querySelector(css_selector)
    image.crossOrigin = 'Anonymous'
    var canvas = document.createElement("canvas")
    canvas.width = image.width
    canvas.height = image.height
    canvas.getContext("2d").drawImage(image, 0, 0)
    data_base64 = canvas.toDataURL('image/png')
    if (data_base64.length > 0) {
        return data_base64.split(',')[1]
    }
    return ''    
}