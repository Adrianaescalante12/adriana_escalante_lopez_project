"use strict";
// loop over each form
for (const x of bookmark) {
  const bookmarkButton = document.querySelectorAll("#bookmark");

  bookmarkButton.addEventListener('click', (evt) => {
      evt.preventDefault();
      const bookmarkButton = evt.target;
      console.log(evt.target);});
}
//       const formInputs = {
//           source: evt.target.source
//           // title: document.querySelector("#title").value,
//           // author: document.querySelector("#author").value,
//           // description: document.querySelector("#description").value,
//           // url: document.querySelector("#url").value
//       };

//       fetch("/handle-bookmarks", {
//           method: "POST",
//           headers: {
//               'Content-Type': 'application/json'
//           },
//           body: JSON.stringify(formInputs),
//           })
//           .then((response) => response.json())
//           .then((responseJson) => {
//             alert(responseJson.status);
//           });
//   });
// }




