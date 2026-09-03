let form = document.querySelector("#score-form");

form.addEventListener("submit", function (event) {
    //Prevent the default form submission behavior
    event.preventDefault();

    //mon1
    let mon1 = document.querySelector("#mon1").value;
    let mon2 = document.querySelector("#mon2").value;
    let mon3 = document.querySelector("#mon2").value;
    console.log("mon1:", mon1);
    console.log("mon2:", mon2);
    console.log("mon3:", mon3);

    // Calculate the total score
    let totalScore = parseFloat(mon1) + parseFloat(mon2) + parseFloat(mon3);
    console.log("Total Score:", totalScore);

    let sum = document.createElement("p");
    sum.textContent = "Total Score: " + totalScore;
    document.body.appendChild(sum);

})
