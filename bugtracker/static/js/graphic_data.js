$(document).ready(function() {

    showGraphicsData();

});


function showGraphicsData(){


  var ctResolve = document.getElementById("chart-resolve").getContext('2d');
  var dataResolve = $("#resolve").val().split(',');
  totalResolve = (dataResolve[0])+ (dataResolve[1]);
  percentageResolve = [(dataResolve[0]/totalResolve*100).toFixed(0), (dataResolve[1]/totalResolve*100).toFixed(0)];
  var chartResolve = new Chart(ctResolve, {
      type: 'pie',
      data: {
          labels: ["No resuelta: "+ percentageResolve[0]+"%", "Fue resuelta completamente: "+ percentageResolve[1]+"%"],
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
  });


  var ctTime = document.getElementById("chart-time").getContext('2d');
  var dataTime = $("#time").val().split(',');
  totalTime = parseInt(dataTime[0])+ parseInt(dataTime[1])+
      parseInt(dataTime[2])+ parseInt(dataTime[3]);
  percentageTime = [(dataTime[0]/totalTime*100).toFixed(0), (dataTime[1]/totalTime*100).toFixed(0),
      (dataTime[2]/totalTime*100).toFixed(0), (dataTime[3]/totalTime*100).toFixed(0)];
  var chartTime = new Chart(ctTime, {
      type: 'pie',
      data: {
          labels: ["Muy lento: "+ percentageTime[0]+"%", "Lento: "+ percentageTime[1]+"%", "Rápido: "+ percentageTime[2]+"%", "Muy rápido: "+ percentageTime[3]+"%"],
          datasets: [{
              labels: '',
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

  });


  var ctDifficulty = document.getElementById("chart-difficulty").getContext('2d');
  var dataDifficulty = $("#difficulty").val().split(',');
  totalDifficulty = parseInt(dataDifficulty[0])+ parseInt(dataDifficulty[1])+
      parseInt(dataDifficulty[2])+ parseInt(dataDifficulty[3]);
  percentageDifficulty = [(dataDifficulty[0]/totalDifficulty*100).toFixed(0),
      (dataDifficulty[1]/totalDifficulty*100).toFixed(0), (dataDifficulty[2]/totalDifficulty*100).toFixed(0),
      (dataDifficulty[3]/totalDifficulty*100).toFixed(0)];
  var chartDifficulty = new Chart(ctDifficulty, {
      type: 'pie',
      data: {
          labels: ["Muy fácil: "+ percentageDifficulty[0]+"%", "Fácil: "+ percentageDifficulty[1]+"%", "Difícil: "+ percentageDifficulty[2]+"%", "Muy difícil: "+ percentageDifficulty[3]+"%"],
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

  });


  var ctContact = document.getElementById("chart-contact").getContext('2d');
  var dataContact = $("#contact").val().split(',');
  totalContact = parseInt(dataContact[0])+ parseInt(dataContact[1])+
      parseInt(dataContact[2])+ parseInt(dataContact[3])+ parseInt(dataContact[4]);
  percentageContact = [(dataContact[0]/totalContact*100).toFixed(0), (dataContact[1]/totalContact*100).toFixed(0),
      (dataContact[2]/totalContact*100).toFixed(0), (dataContact[3]/totalContact*100).toFixed(0),(dataContact[4]/totalContact*100).toFixed(0)];
  var chartContact = new Chart(ctContact, {
      type: 'pie',
      data: {
          labels: ["Extensión telefónica: "+ percentageContact[0]+"%", "Correo electrónico: "+ percentageContact[1]+"%", "Celular: "+ percentageContact[2]+"%",
                    "Chat: "+ percentageContact[3]+"%", "Ninguno: "+ percentageContact[4]+"%"],
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
  });


  var ctSatisfied = document.getElementById("chart-satisfied").getContext('2d');
  var dataSatisfied = $("#satisfied").val().split(',');
  totalSatisfied = parseInt(dataSatisfied[0])+ parseInt(dataSatisfied[1])+
      parseInt(dataSatisfied[2])+ parseInt(dataSatisfied[3]);
  percentageSatisfied = [(dataSatisfied[0]/totalSatisfied*100).toFixed(0), (dataSatisfied[1]/totalSatisfied*100).toFixed(0),
      (dataSatisfied[2]/totalSatisfied*100).toFixed(0), (dataSatisfied[3]/totalSatisfied*100).toFixed(0)];
  var chartSatisfied = new Chart(ctSatisfied, {
      type: 'pie',
      data: {
          labels: ["Muy insatisfecho: "+ percentageSatisfied[0]+"%", "Insatisfecho: "+ percentageSatisfied[1]+"%", "Satisfecho: "+ percentageSatisfied[2]+"%",
                    "Muy satisfecho: "+ percentageSatisfied[3]+"%"],
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

  });

}