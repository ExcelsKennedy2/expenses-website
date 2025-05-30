// // Bar Chart
// const renderChart = (data, labels) => {
//  document.addEventListener("DOMContentLoaded", () => {
//                   new Chart(document.querySelector('#barChart'), {
//                     type: 'bar',
//                     data: {
//                       labels: labels,
//                       datasets: [{
//                         label: 'Last 6 months expenses',
//                         data: data,
//                         backgroundColor: [
//                           'rgba(255, 99, 132, 0.2)',
//                           'rgba(255, 159, 64, 0.2)',
//                           'rgba(255, 205, 86, 0.2)',
//                           'rgba(75, 192, 192, 0.2)',
//                           'rgba(54, 162, 235, 0.2)',
//                           'rgba(153, 102, 255, 0.2)',
//                           'rgba(201, 203, 207, 0.2)'
//                         ],
//                         borderColor: [
//                           'rgb(255, 99, 132)',
//                           'rgb(255, 159, 64)',
//                           'rgb(255, 205, 86)',
//                           'rgb(75, 192, 192)',
//                           'rgb(54, 162, 235)',
//                           'rgb(153, 102, 255)',
//                           'rgb(201, 203, 207)'
//                         ],
//                         borderWidth: 1
//                       }]
//                     },
//                     options: {
//                       // scales: {
//                       //   y: {
//                       //     beginAtZero: true
//                       //   }
//                       // }
//                       title: {
//                         display: true,
//                         text: 'Expenses per category',
//                       }
//                     }
//                   });
//                 });
//
//
// }
// const getChartData = ()=>{
//    console.log('fetching')
//    fetch('/expense_category_summary/').then((res) => res.json()).then((results) => {
//      console.log('results', results);
//      const category_data = results.expense_category_data;
//      const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
//      renderChart(data, labels);
//    })
//  };
// document.onload = getChartData();
//
//
// // Doughnut Chart
// const doughnutChart = (data, labels) => {
//   document.addEventListener("DOMContentLoaded", () => {
//                   new Chart(document.querySelector('#doughnutChart'), {
//                     type: 'doughnut',
//                     data: {
//                       labels: [labels],
//                       datasets: [{
//                         label: 'Last 6 months expenses',
//                         data: data,
//                         backgroundColor: [
//                           'rgb(255, 99, 132)',
//                           'rgb(54, 162, 235)',
//                           'rgb(255, 205, 86)'
//                         ],
//                         hoverOffset: 4
//                       }]
//                     }
//                   });
//                 });
// }
// const renderChartData = ()=>{
//    console.log('fetching')
//    fetch('/expense_category_summary/').then((res) => res.json()).then((results) => {
//      console.log('results', results);
//      const category_data = results.expense_category_data;
//      const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
//      doughnutChart(data, labels);
//    })
//  };
// document.onload = renderChartData();

document.addEventListener("DOMContentLoaded", () => {
  const renderChart = (data, labels) => {
    new Chart(document.querySelector('#barChart'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last 6 months expenses',
          data: data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        title: {
          display: true,
          text: 'Expenses per category',
        }
      }
    });
  }

  const doughnutChart = (data, labels) => {
    new Chart(document.querySelector('#doughnutChart'), {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last 6 months expenses',
          data: data,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
          ],
          hoverOffset: 4
        }]
      }
    });
  }

  const getChartData = () => {
    fetch('/expense_category_summary/')
      .then(res => res.json())
      .then(results => {
        const category_data = results.expense_category_data;
        const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
        renderChart(data, labels);
        doughnutChart(data, labels);
      });
  }

  getChartData();
});
