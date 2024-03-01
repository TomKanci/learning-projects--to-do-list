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

function printArray() {
  const myarray = [];

  draggables.forEach((draggable, index, array) => {
    myarray.push(draggable.id);
  });
  console.log(myarray);
}

function runPyScript() {
  const myarray = [];
  draggables.forEach((draggable, index, array) => {
    myarray.push(draggable.id);
  });
  var jqXHR = $.ajax({
    type: "POST",
    url: "/save_order",
    async: false,
    data: { mydata: myarray },
  });

  // return jqXHR.responseText;
}
