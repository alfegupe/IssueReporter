$(document).ready(function() {

    showGraphicsData();

});


function showGraphicsData(){

  var ctResolve = document.getElementById("chart-resolve").getContext('2d');
  var ctTime = document.getElementById("chart-time").getContext('2d');
  var ctDifficulty = document.getElementById("chart-difficulty").getContext('2d');
  var ctContact = document.getElementById("chart-contact").getContext('2d');
  var ctSatisfied = document.getElementById("chart-satisfied").getContext('2d');

  var dataResolve = $("#resolve").val().split(',');
  var dataTime = $("#time").val().split(',');
  var dataDifficulty = $("#difficulty").val().split(',');
  var dataContact = $("#contact").val().split(',');
  var dataSatisfied = $("#satisfied").val().split(',');

  var chartResolve = new Chart(ctResolve, {
      type: 'horizontalBar',
      data: {
          labels: ["No resuelta", "Fue resuelta completamente", "Total"],
          datasets: [{
              label: '',
              data: dataResolve,
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
          labels: ["Muy lento", "Lento", "Rápido", "Muy rápido", "Total"],
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

  var chartDifficulty = new Chart(ctDifficulty, {
      type: 'horizontalBar',
      data: {
          labels: ["Muy fácil", "Fácil", "Difícil", "Muy difícil", "Total"],
          datasets: [{
              label: '',
              data: dataDifficulty,
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

  var chartContact = new Chart(ctContact, {
      type: 'horizontalBar',
      data: {
          labels: ["Extensión telefónica", "Correo electrónico", "Celular",
                    "Chat", "Ninguno", "Total"],
          datasets: [{
              label: '',
              data: dataContact,
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

  var chartSatisfied = new Chart(ctSatisfied, {
      type: 'horizontalBar',
      data: {
          labels: ["Muy insatisfecho", "Insatisfecho", "Satisfecho",
                    "Muy satisfecho", "Total"],
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

}