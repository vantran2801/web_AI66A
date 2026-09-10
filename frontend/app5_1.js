// function fetchUsers() {
//   fetch("https://jsonplaceholder.typicode.com/users")
//     .then((response) => response.json())
//     .then((users) => {
//       const tableBody = document.getElementById("table-body");
//       tableBody.innerHTML = "";

//       users.forEach((user) => {
//         const row = document.createElement("tr");
//         row.innerHTML = `
//           <td>${user.id}</td>
//           <td>${user.name}</td>
//           <td>${user.username}</td>
//           <td>${user.email.toLowerCase()}</td>
//           <td>${user.website}</td>
//           <td>${user.address.street} - ${user.address.city}</td>
//         `;
//         tableBody.appendChild(row);
//       });
//     })
//     .catch((error) => console.error("Lỗi:", error));
// }

// Viết fetchUsers() bằng async/await
async function fetchUsers() {
  let users = [];
  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/users");
    users = await response.json();
  } catch (error) {
    console.error("Lỗi:", error);
  } finally {
    if (users.length > 0) {
      renderUsers(users);
    }
  }
}

    })


// fetchUsers();


