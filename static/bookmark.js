"use strict";
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
          .then((response) => {
            response.json();
            alert(response);
          })
          .then((responseJson) => {
            alert(responseJson.status);
          });
  });
};

// Debug 34 and 35




