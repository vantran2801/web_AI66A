async function greet() {
    return "Hello, World!";
}

console.log(greet());

greet().then((response) => {
    console.log(response);
});

// c1
async function getData1() {
    let text = "";
    greet().then((response) => {
        text = response;
    });
    return text;
}

// c2
async function getData() {
    const text = await greet();
    return text;
}

console.log(getData());