function checkEmptyField() {
    let subject_field = document.getElementById("subject_field").value
    let trix_editor_nodes = document.getElementById("trixEditor").childElementCount
    let targets_csv = document.getElementById("dealCsv").files[0];
  
    let emailSubmitButton = document.getElementById('submitBtn')
    let errorMsg = document.getElementById("errorMsg")

    if (subject_field !== "" && trix_editor_nodes !== 0 && targets_csv !== undefined) {
        emailSubmitButton.disabled = false
        emailSubmitButton.style.cursor = "pointer"
        emailSubmitButton.style.backgroundColor = "rgb(76, 102, 175)"
        errorMsg.style.display = "none"
    } else {
        emailSubmitButton.disabled = true
        emailSubmitButton.style.cursor = "auto"
        emailSubmitButton.style.backgroundColor = "rgb(179 181 186)"
        errorMsg.style.display = "block"
    }
  }