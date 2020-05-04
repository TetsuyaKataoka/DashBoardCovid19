//サーバーからデータを受け取る
$("#sort_type").change(function () {
    var form = $(this).closest("form-group");
    $.ajax({
        url: form.attr("data-view-countries-max-url"),
        type: 'GET',

        // 通信状態に問題がないかどうか
        success: function(data) {

            console.log("成功");

        },
        // 通信エラーになった場合の処理
        error: function(err) {

            console.log("失敗");

        }
    });
});