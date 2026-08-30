let form = document.querySelector("#score-form");

form.addEventListener("submit", function (event) {
  event.preventDefault();

  // mon1
  let mon1 = document.querySelector("#mon1").value;
  let mon2 = document.querySelector("#mon2").value;
  let mon3 = document.querySelector("#mon3").value;

  console.log("mon1:", mon1);
  console.log("mon2:", mon2);
  console.log("mon3:", mon3);

  //   Calculate the totel score
  let totalScore = Number(mon1) + Number(mon2) + Number(mon3);
  console.log("Total Score:", totalScore);

  let totalElement = document.querySelector("#total");
  totalElement.textContent = "Total Score: " + totalScore;
});
