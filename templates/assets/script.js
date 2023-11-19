/* Author: Daiki Nomura */
// hide the text box and the select box
document.getElementById('if-myself-onset').style.display = "none";
document.getElementById('hospital-name').disabled = true;
document.getElementById('os-date').disabled = true;

window.onload = function () {
  var today = new Date();
  today.setDate(today.getDate());
  var yyyy = today.getFullYear();
  var mm = ("0" + (today.getMonth() + 1)).slice(-2);
  var dd = ("0" + today.getDate()).slice(-2);
  document.getElementById("str-date").value = yyyy + '-' + mm + '-' + dd;
  document.getElementById("ed-date").value = yyyy + '-' + mm + '-' + dd;
  document.getElementById("os-date").value = yyyy + '-' + mm + '-' + dd;
}

document.getElementById('submit').addEventListener('click', (function () {
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
})
);

// switch what is displayed based on the select value
function selectChanged(select) {
  if (select === "myself") {
    document.getElementById('hospital-name').disabled = false;
    document.getElementById('os-date').disabled = false;
    document.getElementById('if-myself-onset').style.display = "block";
  } else {
    document.getElementById('if-myself-onset').style.display = "none";
    document.getElementById('if-myself-onset').disabled = true;
    document.getElementById('os-date').disabled = true;
  }
}

// do selectChanged when the 'sel-reason' is changed
document.getElementById('sel-reason').addEventListener('change', function () {
  selectChanged(this.value);
});