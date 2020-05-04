// 全辞書データを取得
var dict_latest_reports = JSON.parse(document.getElementById('dict_latest_reports').textContent);
console.log(dict_latest_reports);
// ドーナツチャートのラベル
var label_array = ['active', 'death', 'recovered', ];

console.log(dict_latest_reports);

// 各辞書データごとにループ
dict_latest_reports.forEach( function (dict_latest_report ) {

    data_array = [dict_latest_report.active_cases, dict_latest_report.total_deaths, dict_latest_report.total_recovered];

    var ctx = document.getElementById('dohnuts_chart_'+dict_latest_report.location__country_region_name).getContext('2d');
    var chart = new Chart(ctx, {
          type: 'doughnut',
          data: {
              labels: label_array,
              datasets: [{
                  backgroundColor: [
                      "#000080",
                      "#CC3300",
                      "#99FF00",

                  ],
                  //背景色(ホバーしたとき)
                  hoverBackgroundColor: [
                      "#000080",
                      "#CC3300",
                      "#99FF00",
                  ],
                  data: data_array,
              }]
          },
          options: {
              cutoutPercentage: 76,  //　円の中心からどのくらい切り取るか
              title: {
                  display: true,
                  text: dict_latest_report.location__country_region_name+"\n("+dict_latest_report.total_cases+" cases)",
                  fontColor: "white",
                  fontSize: 15
              },
              responsive: true,
              maintainAspectRatio: false,
              legend: {
                  labels: {
                        boxWidth:30,
                        padding:20 //凡例の各要素間の距離
                  },
              display: false
              },
              plugins: [data_array],
          }
      });
});



