"use strict";
// const bookmark = document.querySelectorAll(".bookmark_this_article");
const bookmark = document.querySelectorAll(".bookmark");
// console.log(bookmark)
for (const x of bookmark) {
  x.addEventListener('click', (evt) => {
      evt.preventDefault();
      // debugger
      const bookmark_target = evt.target;
      console.log(bookmark_target);
      
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
            alert(responseJson.status);
          });
  });
};




