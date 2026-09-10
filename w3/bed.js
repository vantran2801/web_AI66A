let posts = document.querySelectorAll(".card");

console.log("posts:");

for (let i = 0; i < posts.length; i++) {
    let title = posts[i].querySelector("h2");
    let content = posts[i].querySelector("p");
    
    let post = {
        title: title.textContent,
        content: content.textContent.trim(), 
    };

    arr.push(post);

    // console.log("Content:", content.textContent.trim());

    title.textContent = "hello" + (i + 1);
    title.style.color = "red";
}

console.log(arr);

letpost4 = document.createElement("section");
post4.classList.add("card");

let title4 = document.createElement("h2");
title4.textContent = "Post 4";
title4.style.color = "blue";

let content4 = document.createElement("p");
content4.textContent = "This is the content of post 4.";

post4.appendChild(title4);
post4.appendChild(content4);
document.body.appendChild(post4);

let post3 = document.querySelector("#totalScore");
post3.remove();
