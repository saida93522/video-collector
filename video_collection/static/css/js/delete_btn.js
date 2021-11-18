const delBtn = document.querySelectorAll(".delete");

delBtn.forEach((button) => {
  button.addEventListener("click", (e) => {
    const canDelete = confirm("Are you sure you want to delete this Place?");
    if (!canDelete) {
      e.preventDefault();
    }
  });
});
