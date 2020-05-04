//折れ線グラフの色
var colors = ["#FF1493", "#00BFFF", "#483D8B", "\t#FF8C00", "rgb(154, 162, 235)"];

// ツールチップの情報
var tooltips = {
    mode: 'nearest',
    intersect: false,
};

// y軸の情報
const yAxes = {
    id: "y-axis-1",
    type: "linear",
    position: "left",
};

// 全辞書データを取得
var dict_report_detail = JSON.parse(document.getElementById('dict_report_detail').textContent.replace(/\bNaN\b/g, "null"));
init(dict_report_detail);

function init(dict_report_detail) {

    // dataset
    var chart_label = [];
    let tmp_country_region_name = '';
    var data_total_cases = [];
    var data_total_deaths = [];
    var data_active_cases = [];
    var data_total_recovered = [];

    // datasets
    var datasets_total_cases = [];
    var datasets_total_deaths = [];
    var datasets_active_cases = [];
    var datasets_total_recovered = [];
    let i = 0;

    // 横軸の情報を取得
    dict_report_detail.forEach( function (_report ) {
        // 横軸の日付情報をラベルに格納
        if(!chart_label.includes(_report.report_date)){
            chart_label.push(_report.report_date);
        }
    });
    chart_label.sort();

    dict_report_detail.forEach( function (_report ) {

        // ループ初回対応
        if( tmp_country_region_name === '') {
            tmp_country_region_name = _report.country_region_name;
        }

        if (_report.country_region_name !== tmp_country_region_name) {
            while(data_total_cases.length < chart_label.length) {
                data_total_cases.unshift(null);
                data_total_deaths.unshift(null);
                data_active_cases.unshift(null);
                data_total_recovered.unshift(null);
            }
            //データセットにデータを追加
            pushToDataset(data_total_cases, tmp_country_region_name, datasets_total_cases, i);
            pushToDataset(data_total_deaths, tmp_country_region_name, datasets_total_deaths, i);
            pushToDataset(data_active_cases, tmp_country_region_name, datasets_active_cases, i);
            pushToDataset(data_total_recovered, tmp_country_region_name, datasets_total_recovered, i);

            // 国名を初期化
            tmp_country_region_name = _report.country_region_name;
            i++;
            // データのリストを初期化
            data_total_cases = [];
            data_total_deaths = [];
            data_active_cases = [];
            data_total_recovered = [];
        }
        data_total_cases.push(_report.total_cases);
        data_total_deaths.push(_report.total_deaths);
        data_active_cases.push(_report.active_cases);
        data_total_recovered.push(_report.total_recovered);
    });

    // 最終行の地域のデータを追加
    while(data_total_cases.length < chart_label.length) {
        data_total_cases.unshift(null);
        data_total_deaths.unshift(null);
        data_active_cases.unshift(null);
        data_total_recovered.unshift(null);
    }

    //データセットにデータを追加
    pushToDataset(data_total_cases, tmp_country_region_name, datasets_total_cases, i);
    pushToDataset(data_total_deaths, tmp_country_region_name, datasets_total_deaths, i);
    pushToDataset(data_active_cases, tmp_country_region_name, datasets_active_cases, i);
    pushToDataset(data_total_recovered, tmp_country_region_name, datasets_total_recovered, i);

    // グラフの描画
    window.chart_total_cases = drawChart('report_total_cases', 'bar', chart_label, datasets_total_cases, tooltips, yAxes);
    window.chart_total_deaths = drawChart('report_total_deaths', 'bar', chart_label, datasets_total_deaths, tooltips, yAxes);
    window.chart_active_cases = drawChart('report_active_cases', 'bar', chart_label, datasets_active_cases, tooltips, yAxes);
    window.chart_total_recovered = drawChart('report_total_recovered', 'bar', chart_label, datasets_total_recovered, tooltips, yAxes);
}

function pushToDataset(data, label, dataset, i) {
    dataset.push({
            label: label,
            type: "line",
            fill: false,
            data: data,
            borderColor: colors[i],
        }
    );
}

// チャートを描く
function drawChart(canvas_id, type, labels, datasets, tooltips, yAxes) {
    // 描画エリアの要素を取得
    var chartArea = document.getElementById(canvas_id).getContext('2d');
    // 累計感染者数のチャートの描画
    return new Chart(chartArea, {
        type: type,
        data: {
            labels: labels,
            datasets: datasets,
            spanGaps: true,
        },
        options: {
            tooltips: tooltips,
            point: {
                radius: 1,
            },
            responsive: true,
            scales: {
                yAxes: yAxes
            }
        }
    });
}

//ajax
$("#sort_type").change(function () {
    $.ajax({
        url: $(this).attr("data-url"),
        type: 'GET',
        dataType: 'json',
        data: $(this).serialize(),
        // 通信状態に問題がないかどうか
        success: function(data) {
            // json形式で取得したデータをparse
            var dict_report_detail = JSON.parse(data);
            // chartを初期化
            chart_total_cases.destroy();
            chart_total_deaths.destroy();
            chart_active_cases.destroy();
            chart_total_recovered.destroy();
            init(dict_report_detail);

        },
        // 通信エラーになった場合の処理
        error: function(err) {
            console.log("失敗");
        }
    });
});