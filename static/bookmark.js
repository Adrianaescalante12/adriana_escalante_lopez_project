"use strict";
// loop over each form
// Loop used to be up here but it loops over the n amount of articles n amount of times
const bookmark = document.querySelectorAll("#bookmark");

for (const x of bookmark) {
  x.addEventListener('click', (evt) => {
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




