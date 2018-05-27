$('form.ajax-form').on('submit', function() {
  var form = $(this);
  $.ajax({
    type: 'POST',
    url: form.attr('action'),
    dataType:"json",
    data:form.serialize(),
    contentType: 'application/x-www-form-urlencoded;charset=utf-8',
    success: function(response) {
        if (response.status=="success") {
            console.log(response.message);
            form[0].reset();
            $('#appoint').modal('hide');
            alert(response.message);

        }else{
            alert(response.message);
            console.log(response.errors.number);
        }
      
    },
    error: function(xhr,errmsg,err) {
      //     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
  });
  console.log(form.attr('action'));
  console.log(form.serialize());
  return false;
});

$(document).ready(function() {
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 
});
$(document).ready( function() {
//TEXT FIELD VALIDATION
    $('#title').on('change',function() {
    var input = $(this).val();
    var regex = /^[a-zA-Z\s]+$/;
        if (regex.test(input)) {
          document.getElementById('errors').innerHTML="";
          $(":submit").removeAttr("disabled");
            return true;
        }
        else
        {
        document.getElementById('errors').innerHTML="*Invalid Data*";
        $(":submit").attr("disabled", true);
        return false;
        }
    });});