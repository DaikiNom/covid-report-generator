/* Author: @09_Aimer */

// hide the text box and the select box
document.getElementById('if-other').style.display = "none";
document.getElementById('if-myself-onset').style.display = "none";
document.getElementById('if-myself-symptom').style.display = "none";

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()

// switch text box between enabled and disabled based on the checkbox value
function chkEnabledControl(textBox) {
    document.getElementById(textBox).disabled = !document.getElementById(textBox).disabled;
}

// switch what is displayed based on the select value
function selectChanged(select) {
    if (select === "other") {
        document.getElementById('if-other').style.display = "block";
        document.getElementById('if-myself-onset').style.display = "none";
        document.getElementById('if-myself-symptom').style.display = "none";
        document.getElementById('other-reason').disabled = !document.getElementById('other-reason').disabled;
    } else if (select === "myself") {
        document.getElementById('if-other').style.display = "none";
        document.getElementById('if-myself-onset').style.display = "block";
        document.getElementById('if-myself-symptom').style.display = "block";
        if (document.getElementById('fever').checked) {
            document.getElementById('temperature').disabled = 'enabled';
            document.getElementById('temperature').value = '';
            document.getElementById('period').disabled = 'enabled';
            document.getElementById('period').value = '';
        }
    } else {
        document.getElementById('if-other').style.display = "none";
        document.getElementById('if-myself-onset').style.display = "none";
        document.getElementById('if-myself-symptom').style.display = "none";
    }
}