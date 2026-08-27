const arr = [
  { name: "Jack", score: 9.0 },
  { name: "Lily", score: 8.5 },
  { name: "Tom",  score: 6.5 },
  { name: "Emma", score: 7.5 },
];

let totalScore = 0;
let scoreHigherThan8 = [];
let highestScore = 0;

for (let i = 0; i < arr.length; i++) {
    totalScore += arr[i].score;
    if (arr[i].score > 8) {
        scoreHigherThan8.push(arr[i].name);
    }

    if (highestScore == 0 || arr[i].score > highestScore) {
        highestScore = arr[i].score;
    }
}

console.log("Total Score:", totalScore);
console.log("Score > 8:", scoreHigherThan8);
console.log("Highest Score:", highestScore);

