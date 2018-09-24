$(document).ready(function(){


    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("GET", "/api/v1.0/shops");
    oReq.send();

    function reqListener () {
        var shops = JSON.parse(this.responseText)
        jQuery.each( shops, function( i, val ) {
           console.log(val.name)
           $(".checkbox-group").append(`<input class="checkbox" value="${val.id}" type="checkbox">
                                    <label for="checkbox">${val.name}</label> </br>`)
          });
      }

      $('#send').on("click",function(){
        stores = []
        jQuery.each($(".checkbox:checked"),function(i,val){
            stores.push(val['value'])
        })
        response = {
            "Stores":stores,
            "Password":$('input').val()
        }
        console.log(response)
          var xhr = new XMLHttpRequest();
          xhr.withCredentials = true;
          
          xhr.addEventListener("readystatechange", function () {
            if (this.readyState === 4) {
              alert(this.responseText);
            }
          });
          
          xhr.open("POST", "/sign-up");
          xhr.setRequestHeader("Content-Type", "application/json");
          xhr.setRequestHeader("Cache-Control", "no-cache");
          
          xhr.send(JSON.stringify(response));
      })
      
});