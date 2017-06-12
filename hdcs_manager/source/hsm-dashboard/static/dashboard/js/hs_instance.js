
require.config({
    paths:{
        echarts:"../../../../../static/lib/echarts"
    }
});

var refreshInterval=20000;
var token = $("input[name=csrfmiddlewaretoken]").val();
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar',
        'echarts/chart/pie',
        'echarts/chart/gauge'
    ],
    function(ec){
        cCacheRatios = ec.init(document.getElementById('divCacheRatioRect'));
        hs_instance_id = document.getElementById('divCacheRatioRect').title;
    	//load
        loadCacheRatio(hs_instance_id);
        loadCacheIOWorkload(hs_instance_id);
        setInterval(function(){
            loadCacheRatio(hs_instance_id);
            loadCacheIOWorkload(hs_instance_id);
        },refreshInterval);
    }
);

function loadCacheRatio(hs_instance_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/hs_instance/"+hs_instance_id+"/cache_ratio",
        data: null,
        dataType:"json",
        success: function(data){
                cCacheRatios.setOption(GetCacheRatio(data.cache_free_size,data.cache_used_size,data.cache_clean_size,data.cache_dirty_size))
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
     });
}

function GetCacheRatio(FREE,USED,CLEAN,DIRTY){
    option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data:['Dirty','Clean','Used','Free']
        },
        series: [
            {
                name:'source',
                type:'pie',
                selectedMode: 'single',
                radius: [0, '30%'],

                label: {
                    normal: {
                        position: 'inner'
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:[
                    {value:FREE, name:'Free'},
                    {value:USED, name:'Used', selected:true}
                ]
            },
            {
                name:'source',
                type:'pie',
                radius: ['40%', '55%'],

                data:[
                    {value:FREE, name:'Free'},
                    {value:CLEAN, name:'Clean'},
                    {value:DIRTY, name:'Dirty'}
                ]
            }
        ]
    };
    return option;
}

function loadCacheIOWorkload(hs_instance_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/hs_instance/"+hs_instance_id+"/cache_io_workload",
        data: null,
        dataType:"json",
        success: function(data){
            $("#ldBW")[0].innerHTML =data.cache_bw;
            $("#ldCacheReadIO")[0].innerHTML =data.cache_read;
            $("#ldCacheReadMissIO")[0].innerHTML =data.cache_read_miss;
            $("#ldCacheWriteIO")[0].innerHTML =data.cache_write;
            $("#ldCacheWriteMissIO")[0].innerHTML =data.cache_write_miss;
            $("#ldCacheTotalIO")[0].innerHTML =Number(data.cache_read)+Number(data.cache_write);
            $("#ldCacheTotalMissIO")[0].innerHTML =Number(data.cache_read_miss)+Number(data.cache_write_miss);
            $("#ldLatency")[0].innerHTML =data.cache_latency;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
     });
}
