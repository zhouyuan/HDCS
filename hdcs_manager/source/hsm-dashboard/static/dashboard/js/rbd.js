
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
        rbd_id = document.getElementById('divCacheRatioRect').title;
        cCacheAction = ec.init(document.getElementById('divCacheActionRect'));
    	//load
        loadCacheRatio(rbd_id);
        loadCacheAction(rbd_id);
        loadCacheIOWorkload(rbd_id);
        loadRBDBasicInfo(rbd_id);
        setInterval(function(){
            loadCacheRatio(rbd_id);
            loadCacheAction(rbd_id);
            loadCacheIOWorkload(rbd_id);
            loadRBDBasicInfo(rbd_id);
        },refreshInterval);
    }
);

function loadCacheRatio(rbd_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/rbd/"+rbd_id+"/cache_ratio",
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

function loadCacheAction(rbd_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/rbd/"+rbd_id+"/cache_action",
        data: null,
        dataType:"json",
        success: function(data){
                cCacheAction.setOption(
                    GetCacheAction(data)
                )
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
     });
}

function loadCacheIOWorkload(rbd_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/rbd/"+rbd_id+"/cache_io_workload",
        data: null,
        dataType:"json",
        success: function(data){
            $("#ldBW")[0].innerHTML =data.cache_bw;
            $("#ldCacheReadIOPS")[0].innerHTML =data.cache_read;
            $("#ldCacheReadMissIOPS")[0].innerHTML =data.cache_read_miss;
            $("#ldCacheWriteIOPS")[0].innerHTML =data.cache_write;
            $("#ldCacheWriteMissIOPS")[0].innerHTML =data.cache_write_miss;
            $("#ldCacheTotalIOPS")[0].innerHTML =Number(data.cache_read)+Number(data.cache_write);
            $("#ldCacheTotalMissIOPS")[0].innerHTML =Number(data.cache_read_miss)+Number(data.cache_write_miss);
            $("#ldLatency")[0].innerHTML =data.cache_latency;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
     });
}

function loadRBDBasicInfo(rbd_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/rbd/"+rbd_id+"/get_rbd_basic_info",
        data: null,
        dataType:"json",
        success: function(data){
            $("#ldRBDName")[0].innerHTML =data.name;
            $("#ldRBDObjects")[0].innerHTML =data.objects;
            $("#ldRBDSize")[0].innerHTML =data.size;
            $("#ldRBDOrder")[0].innerHTML =data.order;
            $("#ldRBDObjectSize")[0].innerHTML =data.object_size;
            $("#ldRBDFormat")[0].innerHTML =data.format;
            $("#ldRBDPrefix")[0].innerHTML =data.block_name_prefix;
            $("#ldRBDFeature")[0].innerHTML =data.features;
            $("#ldRBDFlags")[0].innerHTML =data.flags;
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

function GetCacheAction(data){
    option = {
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['Promote(IOPs)','Flush(IOPs)','Evict(IOPs)']
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : data.date
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'Promote(IOPs)',
                type:'line',
                tiled: 'total',
                data:data.cache_promote
            },
            {
                name:'Flush(IOPs)',
                type:'line',
                tiled: 'total',
                data:data.cache_flush
            },
            {
                name:'Evict(IOPs)',
                type:'line',
                tiled: 'total',
                data:data.cache_evict
            }
        ]
    };
    return option;
}
