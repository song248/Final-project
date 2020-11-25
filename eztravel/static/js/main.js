function analysis(){
    $.ajax({
        cache : false,
        url : "analysis/",
        type : 'GET',
        beforeSend:function(){
            $("#loading").show();
            $("#analysis_btn").hide();
            $("#main_header").hide();
        },
        success : function(data) {
            $("#analysis_btn").hide();
            // radar graph
            make_radar_graph(data);
            // hist graph
            make_hist_graph(data);
            // pie graph
            make_doughnut_graph(data);
            // time graph
            make_line_graph(data);
            // wordcloud
            chartReadyHandler(data);
        },
        complete:function(){
        $("#loading").hide();
        $("#result_header").show();
        $("#email_row").show();
        },
        error : function(xhr, status) {
            alert(xhr + " : " + status);
        }
    });
}