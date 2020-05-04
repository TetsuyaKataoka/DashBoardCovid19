$("#id_max_countries").change(function () {
    // setInterval(function() {
        var form = $(this).closest("form");
        $.ajax({
            url: form.attr("data-view-countries-max-url"),
            data: form.serialize(),
        })
        .done(function (data) {

            // reload_areaの再描画のためjavascriptをbodyに埋め込む
            var el = document.createElement("script");
            // SCRIPTタグのSRC属性に読み込みたいファイルを指定
            el.src = "/static/js/Dashboard.js";
            // BODY要素の最後に追加
            document.head.appendChild(el);

            // idがreload_areaの要素を取得
            $reload_area = $('#reload_area');
            // reload_areaを初期化
            $reload_area.empty();
            $reload_area.append(data);
        })
    // },10000)
});