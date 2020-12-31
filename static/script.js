swal({
  title: "Welcome!",
  text: "This site is in progress, I am working on it",
  icon: "success",
  button: "Ok, I'll check later",
})

const webmaster = "Wow, you knew how to do that. If you didn't google that, and you have an extensive knowledge of Web Development, you should remake this website! (but only if it is really old and seems really 2020-ish)"

console.log("_.-^^---....,,---_\n_--                  --_\n<          BOOM!         >)\n\._                   _./\n   ```--. . , ; .--'''\n         | |   |\n      .-=||  | |=-.\n      `-=#$%&%$#=-'\n         | ;  :|\n_____.,-#%&$@%#&#~,._____\nHey! What are you doing here? If you know what to do, then print the variable  webmaster")

function confirm() {
  swal({
    title: "Are you sure?",
    text: `If you delete this file, it will be gone forever (A very long time!)`,
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete)  {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "http://127.0.0.1:5000/events", true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify({
      }));
    } else {
      swal("The file is safe", {
        icon: "success",
      });
    }
  });


}

