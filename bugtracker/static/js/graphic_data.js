$(document).ready(function() {

  var ctResolve = document.getElementById("chart-resolve").getContext('2d');
  var ctTime = document.getElementById("chart-time").getContext('2d');
  var ctNotify = document.getElementById("chart-notify").getContext('2d');
  var ctSatisfied = document.getElementById("chart-satisfied").getContext('2d');
  var dataRsolve = $("#resolve").val().split(',');
  var dataTime = $("#time").val().split(',');
  var dataNotify = $("#notify").val().split(',');
  var dataSatisfied = $("#satisfied").val().split(',');

  var chartResolve = new Chart(ctResolve, {
      type: 'horizontalBar',
      data: {
          labels: ["No fue Resuelta", "Parcialmente", "Completamente", "Total"],
          datasets: [{
              label: '',
              data: dataRsolve,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
              ],
              borderColor: [
                  'rgba(255,99,132,1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });
  var chartTime = new Chart(ctTime, {
      type: 'horizontalBar',
      data: {
          labels: ["Muy lento", "Lento", "Normal", "Rápido", "Muy rápido", "Total"],
          datasets: [{
              label: '',
              data: dataTime,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
              ],
              borderColor: [
                  'rgba(255,99,132,1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });
  var chartNotify = new Chart(ctNotify, {
      type: 'horizontalBar',
      data: {
          labels: ["No fue notificado", "Por Correo electrónico", "Por Teléfono", "Total"],
          datasets: [{
              label: '',
              data: dataNotify,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
              ],
              borderColor: [
                  'rgba(255,99,132,1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });
  var chartSatisfied = new Chart(ctSatisfied, {
      type: 'horizontalBar',
      data: {
          labels: ["No", "Si", "Total"],
          datasets: [{
              label: '',
              data: dataSatisfied,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
              ],
              borderColor: [
                  'rgba(255,99,132,1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });

});
