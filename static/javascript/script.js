function toggleMenu() {
    var menu = document.getElementById('menu');
    var formContainer = document.getElementById('form-container');
  
    if (menu.style.left === '-200px') {
      menu.style.left = '0';
      formContainer.style.display = 'none';
    } else {
      menu.style.left = '-200px';
    }
  }
  
  function openForm1() {
    var formContainer1 = document.getElementById('form-container1');
    formContainer1.style.display = 'block';
  }
  function openForm2() {
    var formContainer2 = document.getElementById('form-container2');
    formContainer2.style.display = 'block';
  }
  function openForm3() {
    var formContainer3 = document.getElementById('form-container3');
    formContainer3.style.display = 'block';
  }
  function openForm4() {
    var formContainer4 = document.getElementById('form-container4');
    formContainer4.style.display = 'block';
  }
  
  
// CRUD
const userForm = document.querySelector("#userForm");

let users = [];
let editing = false;
let userId = null;

window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/api/users");
  const data = await response.json();
  users = data;
  renderUser(users);
});

userForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = userForm["username"].value;
  const puesto = userForm["puesto"].value;
  const fecha = userForm["fecha"].value;
  const sueldo = userForm["sueldo"].value;
  const edad = userForm["edad"].value;

  if (!editing) {
    // send user to backend
    const response = await fetch("/api/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        puesto,
        fecha,
        sueldo,
        edad,
      }),
    });

    const data = await response.json();
    users.push(data);
    renderUser(users);
  } else {
    const response = await fetch(`/api/users/${userId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        puesto,
        fecha,
        sueldo,
        edad,
      }),
    });
    const updatedUser = await response.json();

    users = users.map((user) =>
      user.id === updatedUser.id ? updatedUser : user
    );
    console.log(users)
    renderUser(users);

    editing = false;
    userId = null;
  }
  userForm.reset();
});

function renderUser(users) {
  const userList = document.querySelector("#userList");
  userList.innerHTML = "";
  users.forEach((user) => {
    const userItem = document.createElement("li");
    userItem.classList = "table-prymary";
    userItem.innerHTML = `
    <header class="d-flex justify-content-between align-items-center bg-info">
          <h3>Nombre: ${user.nombre_aa}</h3>
          <div>
            <button data-id="${user.id}" class="btn-delete btn btn-danger btn-sm">Delete</button>
            <button data-id="${user.id}" class="btn-edit btn btn-secondary btn-sm">Edit</button>
          </div>
        </header>
        <p class="bg-info">Puesto: ${user.puesto_aa} <br>
        Fecha ingreso: ${user.fecha_ingreso_aa}<br>
        Sueldo: ${user.sueldo_aa}<br>
        Edad: ${user.edad_aa}</p>           
    `;

    // Handle delete button
    const btnDelete = userItem.querySelector(".btn-delete");

    btnDelete.addEventListener("click", async (e) => {
      const response = await fetch(`/api/users/${user.id}`, {
        method: "DELETE",
      });

      const data = await response.json();

      users = users.filter((user) => user.id !== data.id);
      renderUser(users);
    });

    userList.appendChild(userItem);

    // Handle edit button
    const btnEdit = userItem.querySelector(".btn-edit");

    btnEdit.addEventListener("click", async (e) => {
      const response = await fetch(`/api/users/${user.id}`);
      const data = await response.json();

      userForm["username"].value = data.nombre_aa;
      userForm["puesto"].value = data.puesto_aa;
      userForm["fecha"].value = data.fecha_ingreso_aa;
      userForm["sueldo"].value = data.sueldo_aa;
      userForm["edad"].value = data.edad_aa;


      editing = true;
      userId = user.id;
    });
  });
}
