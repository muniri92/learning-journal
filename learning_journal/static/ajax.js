


function do_some_ajax(){
    jQuery.ajax({
        url     : 'add',
        type    : 'POST',
        dataType: 'json',
        success : function(data){
            alert("Success. Got the message:\n "+ data.message)
        }
    });
}