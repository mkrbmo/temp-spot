window.onload = (event) => {
    let form = document.getElementById('analysis_form')
    form.addEventListener('submit', (event) => {
        let card = document.getElementById('form-card')
        if (card.style.display === "none") {
            card.style.display = "block";
          } else {
            card.style.display = "none";
          }       
    })
}
