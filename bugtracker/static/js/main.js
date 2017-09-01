$(document).ready(function() {

});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

function saveCommentEvaluator(){

    $("#error_comment").attr("style", "display: none;");
    var comment = $("#id_comment").val();
    var issue_id = $("#issue_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    if(comment && issue_id){
        $("#save-comment").attr('disabled', 'true');
        $("#save-comment").html(
            "<i clas='fa fa-spinner'></i> Guardando."
        );
        $.ajax({
          url: "/bugtracker/add_evaluation_comment/",
            method: "post",
            data: {
                'id': issue_id,
                'comment': comment,
                'csrfmiddlewaretoken': token
            }
        }).done(function(response) {
          var msj = "";
          if(response.comment){
            var comment = $("#id_comment").val('');
            var date = new Date(response.created_at);
            msj += '<div id="list-comments">';
            msj += '<div class="panel panel-info">';
            msj += '<div class="panel-heading">';
            msj += response.user + '</br>';
            msj += '<small>'+getFormatTime(date.getDate())+'/'+getFormatTime(parseInt(date.getMonth()+1))
                +'/'+date.getFullYear()+' '+getFormatTime(date.getHours())+':'
                +getFormatTime(date.getMinutes())+'</small>';
            msj += '</div>';
            msj += '<div class="panel-body">';
            msj += response.comment;
            msj += '</div>';
            msj += '</div>';
            msj += '</div>';
            if(response.count === 1){
                $("#content-comments").html('');
            }
            $("#save-comment").removeAttr('disabled');
            $("#save-comment").html(
                    "<i clas='fa fa-save'></i> Guardar."
                );
            $("#list-comments").before(msj)
            $("#close-modal-detail-comment").click();
          }else{
            $("#list-comments").html("<p>No se han agregado comentarios a la incidencia</>")
            $("#save-comment").removeAttr('disabled');
            $("#save-comment").html(
                    "<i clas='fa fa-save'></i> Guardar."
                );
          }
        });

    }else{
        $("#error_comment").removeAttr("style");
        $("#error_comment").html("Debe digitar un comentario para guadarlo.");
    }
}

function getFormatTime(time){
    if(time < 10)
        return '0'+time;
    return time;
}