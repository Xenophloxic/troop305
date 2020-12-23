swal({
  title: "Welcome!",
  text: "This site is in progress, I am working on it",
  icon: "success",
  button: "Ok, I'll check later",
})

function confirm(value) {
  swal({
    title: "Are you sure?",
    text: `If you delete ${value}, it will be gone forever (A very long time!)`,
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "http://127.0.0.1:5000/webmaster", true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify({
          value: value
      }));
    } else {
      swal("The file is safe", {
        icon: "success",
      });
    }
  });


}