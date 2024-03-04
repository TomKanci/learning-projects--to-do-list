////////////////////////////////////////////////
// 1. Drag and Drop
// taken from https://www.youtube.com/watch?v=jfYWwQrtzzY
////////////////////////////////////////////////
const draggables = document.querySelectorAll(".draggable");
const boxes = document.querySelectorAll(".box");

draggables.forEach((draggable) => {
  draggable.addEventListener("dragstart", () => {
    draggable.classList.add("dragging");
  });
  draggable.addEventListener("dragend", () => {
    draggable.classList.remove("dragging");
  });
});

boxes.forEach((box) => {
  box.addEventListener("dragover", (e) => {
    e.preventDefault();
    const afterElement = getDraggedAfterElement(box, e.clientY);
    const draggable = document.querySelector(".dragging");
    if (afterElement == null) {
      box.appendChild(draggable);
    } else {
      box.insertBefore(draggable, afterElement);
    }
  });
});

function getDraggedAfterElement(box, y) {
  const draggableElements = [
    ...box.querySelectorAll(".draggable:not(.dragging)"),
  ];

  return draggableElements.reduce(
    (closest, child) => {
      const box = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child };
      } else {
        return closest;
      }
    },
    { offset: Number.NEGATIVE_INFINITY }
  ).element;
}

////////////////////////////////////////////////
// 2. Save order of tasks
////////////////////////////////////////////////

document
  .querySelector("#save-order-button")
  .addEventListener("click", function () {
    // Gather the current order of tasks for each group
    let taskOrder = {
      "box-today": Array.from(
        document.querySelectorAll("#box-today .task")
      ).map((task) => task.id),
      "box-week": Array.from(document.querySelectorAll("#box-week .task")).map(
        (task) => task.id
      ),
      "box-later": Array.from(
        document.querySelectorAll("#box-later .task")
      ).map((task) => task.id),
    };

    // Send this order to the server
    fetch("/save_order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(taskOrder),
    });
  });

////////////////////////////////////////////////
// 3. Set task as checked = done
////////////////////////////////////////////////

document.querySelectorAll(".task-checkbox").forEach(function (checkbox) {
  checkbox.addEventListener("change", function () {
    fetch("/update_task/" + this.id.replace("task-checkbox-", ""), {
      method: "PUT",
    }).then(function () {
      location.reload();
    });
  });
});
