function animate_subheading(button) {
    console.log('start');
    let sh = button.parentNode;
    let qrc = document.querySelector(`#qr_${sh.dataset.transaction}`)
    if (qrc) {
        qrc.classList.add("fadeUp")
        setTimeout(function() {
            qrc.remove()
        }, 480);
    } else {
        fetch(`get_qr?transaction_id=${parseInt(sh.dataset.transaction)}`)
        .then(response=>response.json())
        .then(data => {
            let qrc = document.createElement("img");
            qrc.src = data.url;
            qrc.id = `qr_${sh.dataset.transaction}`;
            qrc.classList.add("qr_code_sm", "fadeDown");
            sh.appendChild(qrc);
        })
    }
    
}