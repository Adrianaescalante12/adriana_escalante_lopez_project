"use strict";
console.log("jsisworking")
// const bookmark = document.querySelectorAll(".bookmark_this_article");
const bookmark = document.querySelectorAll(".bookmark");
// console.log(bookmark)
for (const x of bookmark) {
  x.addEventListener('click', (evt) => {
      evt.preventDefault();
      // debugger
      const bookmarkTarget = evt.target;
      console.log(bookmarkTarget);
      
      const formInputs = {
        
          source:evt.target.getAttribute('data-source'),
          title: evt.target.getAttribute('data-title'),
          author: evt.target.getAttribute('data-author'),
          description: evt.target.getAttribute('data-description'),
          url: evt.target.getAttribute('data-url')
      };

      fetch("/handle-bookmarks", {
          method: "POST",
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(formInputs),
          })
          .then((response) => response.json())
          .then((responseJson) => {
            console.log(responseJson);
            alert(responseJson.message);
          });
  });
};




const unbookmark = document.querySelectorAll(".unbookmark");

for (const x of unbookmark) {
  x.addEventListener('click', (evt) => {
      // debugger
      const unbookmarkTarget = evt.target;
      console.log(unbookmarkTarget);
      
      const formInputs = {
          url: evt.target.getAttribute('data-url')
      };

      fetch("/handle-unbookmark", {
          method: "POST",
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(formInputs),
          })
          .then((response) => response.json())
          .then((responseJson) => {
            console.log(responseJson);
            alert(responseJson.message);
          });
  });
};

