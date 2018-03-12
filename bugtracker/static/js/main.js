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
  var data = new FormData();
  if(opc == '1'){
    url = "/bugtracker/xlsx/?"+$("#filter").serialize();
    name = "incidencias_";
    data.append('data', $("#filter").serialize());
  }else if (opc == '2'){
    url = "/bugtracker/xlsx_results/?"+'init_date='+$("#init_date_results").val()+"&end_date="+$("#end_date_results").val();
    name = "resultados_evaluaciones_";
    data.append('data', {'init_date': $("#init_date").val(), 'end_date': $("#end_date_results").val()});
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
          alertify.error("Se ha presentado un error interno al intentar generar el excel, por favor intentelo de nuevo.");
      }
  };
  xhttp.open("get", url, true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.responseType = 'blob';
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

function getEvaluationDataById(id_issue){
  var url = $("#url_get_issue_details").val();
  $.ajax({
    method: "GET",
    url: url
  }).done(function(response) {
    $("#response_data").text(response.resolve);
    $("#time_data").text(response.time);
    $("#difficulty_data").text(response.difficulty);
    $("#contact_data").text(response.contact);
    $("#satisfied_data").text(response.satisfied);
  });
}

function filterEvaluationsResults(){
    var div_show = $("#clone-data").clone();
    var url = $("#url_get_issue_filters").val();

    var init = $("#init_date_results").val();
    var end = $("#end_date_results").val();

    $("#show-data").html("<div style='text-align: center;'><h1><i class='fa fa-circle-o-notch fa-spin'></i> Cargando datos</h1></div>");
    $.ajax({
        url: url,
        method: "get",
        data: {
            "init_date": init,
            "end_date": end,
        },
    }).done(function(result){

        console.log(JSON.stringify(result));

        $("#show-data").html(div_show);

        $("#resolve1").text(result.resolve['1']);
        $("#resolve5").text(result.resolve['5']);
        $("#resolve").val(result.resolve['1']+","+result.resolve['5']);

        $("#time1").text(result.time['1']);
        $("#time2").text(result.time['2']);
        $("#time3").text(result.time['3']);
        $("#time5").text(result.time['5']);
        $("#time").val(result.time['1']+","+result.time['2']+","+result.time['3']+","+result.time['5']);

        $("#difficulty1").text(result.difficulty['1']);
        $("#difficulty2").text(result.difficulty['2']);
        $("#difficulty3").text(result.difficulty['3']);
        $("#difficulty5").text(result.difficulty['5']);
        $("#difficulty").val(result.difficulty['1']+","+result.difficulty['2']+","+result.difficulty['3']+","+result.difficulty['5']);

        $("#contact1").text(result.contact['1']);
        $("#contact2").text(result.contact['2']);
        $("#contact3").text(result.contact['3']);
        $("#contact4").text(result.contact['4']);
        $("#contact5").text(result.contact['5']);
        $("#contact").val(result.contact['1']+","+result.contact['2']+","+result.contact['3']+","+result.contact['4']+","+result.contact['5']);

        $("#satisfied1").text(result.satisfied['1']);
        $("#satisfied2").text(result.satisfied['2']);
        $("#satisfied3").text(result.satisfied['3']);
        $("#satisfied5").text(result.satisfied['5']);
        $("#satisfied5").val(result.satisfied['1']+","+result.satisfied['2']+","+result.satisfied['3']+","+result.satisfied['5']);

        $("#total-evaluations").text(result.cant);

        showGraphicsData();
    });
}