const delBtn = document.querySelectorAll(".delete");

delBtn.forEach((button) => {
  button.addEventListener("click", (e) => {
    const canDelete = confirm("Are you sure you want to delete this Place?");
    if (!canDelete) {
      e.preventDefault();
    }
  });
});

// nav
// function toggle() {
//   let links = document.getElementById("links");
//   let blob = document.getElementById("blob");
//   blob.classList.toggle("open");
//   if (links.style.display == "block") {
//     links.style.display = "none";
//   } else {
//     links.style.display = "block";
//   }
// }
