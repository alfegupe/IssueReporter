$(document).ready(function() {

});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

function saveCoomentEvaluator(){
    $("#error_comment").attr("style", "display: none;");
    var comment = $("#id_comment").val();
    var issue_id = $("#issue_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    console.log(token);
    if(comment && issue_id){
        $.ajax({
          url: "/bugtracker/add_evaluation_comment/",
            method: "post",
            data: {
                'id': issue_id,
                'comment': comment,
                'csrfmiddlewaretoken': token
            }
        }).done(function(response) {
          console.log("done - " + JSON.stringify(response));
          var msj = "";
          if(response.comments){
          var comment = $("#id_comment").val('');
            response.comments.forEach(function(item, indx){
                var date = new Date(item.created_at);
                msj += '<div class="panel panel-default">';
                msj += '<div class="panel-heading">';
                msj += item.user + '</br>';
                msj += '<small>'+date.toDateString()+'</small>';
                msj += '</div>';
                msj += '<div class="panel-body">';
                msj += item.comment;
                msj += '</div>';
                msj += '</div>';
            })
            $("#list-comments").html(msj)
          }else{
            $("#list-comments").html("<p>No se han agregado comentarios a la incidencia</>")
          }
        });
    }else{
        $("#error_comment").removeAttr("style");
        $("#error_comment").html("Debe digitar un comentario para guadarlo.");
    }
}