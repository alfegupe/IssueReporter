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

function excel(opc){
  var url = "";
  var name = "";
  alertify.error(opc);
  if(opc == '1'){
    url = "/bugtracker/xlsx/?"+$("#filter").serialize();
    name = "incidencias_";
  }else if (opc == '2'){
    url = "/bugtracker/xlsx_results/";
    name = "resultados_evaluaciones_";
  }
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
      var a, today;
      if (xhttp.readyState === 4 && xhttp.status === 200) {
          a = document.createElement('a');
          a.href = window.URL.createObjectURL(xhttp.response);
          today = new Date();
          a.download = name + today.toDateString().split(" ").join("_") + ".xls";
          a.style.display = 'none';
          document.body.appendChild(a);
          return a.click();
      }else if(xhttp.readyState === 4 && xhttp.status === 500){
          alert("Se ha presentado un error interno al intentar generar el excel, por favor intentelo de nuevo.");
      }
  };
  xhttp.open("get", url, true);
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
    var q3 = $("#id_difficulty").val();
    var q4 = $("#id_contact").val();
    var q5 = $("#id_satisfied").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    if(q1 && q2 && q3 && q4 && q5){
        $("#error_evaluate").attr('style', 'display: none;');
        $.ajax({
          url: "/bugtracker/issue_evaluation/",
            method: "post",
            data: {
                'issue_id': issue_id,
                'resolve': q1,
                'time_evaluation': q2,
                'difficulty': q3,
                'contact': q4,
                'satisfied': q5,
                'csrfmiddlewaretoken': token
            }
        }).done(function(response) {
            if(response.code == 200){
                //alert(JSON.stringify(response.msg));
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

function validateFormNewUpdateIssue(){
  var validate = 0;
  var msj_error = "<ul>";

  //Validate Title
  if($("#id_issue").val() == ""){
    validate++;
    msj_error += "<li> El <b>Título</b> de la incidencia. </li>";
  }

  //Validate Desciption
  if($("#id_description").val() == ""){
    validate++;
    msj_error += "<li> La <b>Descripción</b> es requerida. </li>";
  }

  //Validate steps_to_reproduce
  if($("#id_steps_to_reproduce").val() == ""){
    validate++;
    msj_error += "<li> Los <b>Pasos para reproducirlo</b> son requeridos. </li>";
  }

  //Validate Software
  if($("#id_software").val() == ""){
    validate++;
    msj_error += "<li> El <b>Software</b> es requerido. </li>";
  }

  //Validate Sede
  if($("#id_headquarter").val() == ""){
    validate++;
    msj_error += "<li> La <b>Sede</b> es requerida. </li>";
  }

  //Validate Navegador
  if($("#id_browser").val() == ""){
    validate++;
    msj_error += "<li> El <b>Navegador</b> es requerido. </li>";
  }

  //Validate OS
  if($("#id_os").val() == ""){
    validate++;
    msj_error += "<li> El <b>Sistema operativo</b> es requerido. </li>";
  }

  //Validate priority
  if($("#id_priority").val() == ""){
    validate++;
    msj_error += "<li> La <b>Prioridad</b> es requerida. </li>";
  }

  //Validate type_issue
  if($("#id_type_issue").val() == ""){
    validate++;
    msj_error += "<li> El <b>Tipo de Incidencia</b> es requerido. </li>";
  }

  //Validate Category_issue
  if($("#id_category_issue").val() == ""){
    validate++;
    msj_error += "<li> La <b>Categoría</b> es requerida. </li>";
  }

  //Validate Reproducibility_issue
  if($("#id_reproducibility_issue").val() == ""){
    validate++;
    msj_error += "<li> La <b>Reproducibilidad</b> es requerida. </li>";
  }

  var is_admin = $("#is_admin").val();
  if(is_admin == "true"){
    if($("#id_dev").val() == ""){
      validate++;
      msj_error += "<li> Debe asignar un <b>Responsable</b> a la incidencia. </li></ul>";
    }
    saveIssueNewUpdate(validate, msj_error);
  }else{
    msj_error += "</ul>";
    saveIssueNewUpdate(validate, msj_error);
  }
}

function saveIssueNewUpdate(validate, msj_error){
  if(validate == 0){
    $("#btn-to-back").hide();
    $("#btn-to-save").attr('disabled', 'true');
    alertify.success("<i class='fa fa-spin fa-spinner'></i> Enviando un email de notificación.");
    $("#issue-udapte-form").submit();
  }else{
    alertify.error("Debe llenar los campos requeridos: <br/><br/>" + msj_error);
  }

}
