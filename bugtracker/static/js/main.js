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

function excel(){
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        var a, today;
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            a = document.createElement('a');
            a.href = window.URL.createObjectURL(xhttp.response);
            today = new Date();
            a.download = "incidencias_" + today.toDateString().split(" ").join("_") + ".xls";
            a.style.display = 'none';
            document.body.appendChild(a);
            return a.click();
        }else if(xhttp.readyState === 4 && xhttp.status === 500){
            alert("Se ha presentado un error al interno al intenter generar el excel, por favor intentelo de nuevo.");
        }
    };
    xhttp.open("get", "/bugtracker/xlsx/?"+$("#filter").serialize(), true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    var data = new FormData();
    data.append('data', $("#filter").serialize());
    xhttp.send(data);
}

function saveIssueEvaluation(){
    var issue_id = $("#id_issue").val();
    var q1 = $("#id_resolve").val();
    var q2 = $("#id_time_evaluation").val();
    var q3 = $("#id_notify").val();
    var q4 = $("#id_satisfied").val();
    var obs = $("#id_observations").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    if(q1 && q2 && q3 && q4){
        $("#error_evaluate").attr('style', 'display: none;');
        $.ajax({
          url: "/bugtracker/issue_evaluation/",
            method: "post",
            data: {
                'issue_id': issue_id,
                'resolve': q1,
                'time_evaluation': q2,
                'notify': q3,
                'satisfied': q4,
                'observations': obs,
                'csrfmiddlewaretoken': token
            }
        }).done(function(response) {
            if(response.code == 200){
                alert(JSON.stringify(response.msg));
                window.location.href = "/";
            }else{
                alert(JSON.stringify(response.msg));
            }
        });
    }else{
        $("#error_evaluate").removeAttr('style');
        $("#error_evaluate").html('<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Debe responder todas las preguntas.');
    }
}