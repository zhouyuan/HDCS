
var spin_opts = {
    lines: 12,
    length: 10,
    width: 3,
    radius: 15,
    corners: 1,
    rotate: 0,
    direction: 1,
    color: 'gray',
    speed: 1,
    trail: 50,
    shadow: false,
    hwaccel: false,
    className: 'spinner',
    zIndex: 2e9,
    top:20,
    left: 50
};

var spinner = new Spinner(spin_opts);

function GenerateSpin(){
	var html = "";
		html += "<div class='modal-dialog'>";
		html += "	<div class='modal-content spin-content'>";
		html += "		<div class='spin-body'>";
		html += "			<div id='divSpin'></div>";
		html += "		</div>"
		html += "	</div>";
		html += "</div>";


		var dialogWrapper = $("#spin_wrapper")[0];
		dialogWrapper.id = "spin_wrapper";
		dialogWrapper.className = "modal fade";
		dialogWrapper.innerHTML = html;

		//Open modal
		$("#spin_wrapper").modal("show");
		//remove the event from the modal
		$("#spin_wrapper").off();
}


function ShowSpin(){
	//Generate Spin
	GenerateSpin();

	//get the spin
	var spin_target = $("#divSpin").get(0);
	spinner.spin(spin_target);
}

function CloseSpin(){
	spinner.spin();
	$("#spin_wrapper").modal("hide");
}

var AJAXCount = 0;
$(document).ajaxStart(function(){
    AJAXCount ++;
	if(AJAXCount!=1){
        //load the spin
	    ShowSpin();
    }
});

$(document).ajaxStop(function(){
	//close the spin
	CloseSpin();
});

$(document).ajaxError(function(){
	//close the spin
	CloseSpin();
});

var token = $("input[name=csrfmiddlewaretoken]").val();

$(document).ready(function(){
    rbd_id = document.getElementById('tRBDCacheConfig').title;
    loadRBDCacheConfig(rbd_id);
});

function loadRBDCacheConfig(rbd_id){
    $.ajax({
	type: "get",
	url: "/hsm_ui/hsm/rbd/"+rbd_id+"/show_cache_config",
	data: null,
	dataType:"json",
	success: function(data){
        $("#ldRBDCacheDir")[0].innerHTML =data.cache_dir;
        $("#ldRBDCleanStart")[0].innerHTML =data.clean_start;
        $("#ldRBDEnableMemoryUsageTracker")[0].innerHTML =data.enable_memory_usage_tracker;
        $("#ldRBDObjectSize")[0].innerHTML =data.object_size;
        $("#ldRBDCacheTotalSize")[0].innerHTML =data.cache_total_size;
        $("#ldRBDCacheDirtyRatioMin")[0].innerHTML =data.cache_dirty_ratio_min;
        $("#ldRBDCacheRatioHealth")[0].innerHTML =data.cache_ratio_health;
        $("#ldRBDCacheRatioMax")[0].innerHTML =data.cache_ratio_max;
        $("#ldRBDCacheFlushInterval")[0].innerHTML =data.cache_flush_interval;
        $("#ldRBDCacheEvictInterval")[0].innerHTML =data.cache_evict_interval;
        $("#ldRBDCacheFlushQueueDepth")[0].innerHTML =data.cache_flush_queue_depth;
        $("#ldRBDAgentThreadsNum")[0].innerHTML =data.agent_threads_num;
        $("#ldRBDCacheServiceThreadsNum")[0].innerHTML =data.cache_service_threads_num;
        $("#ldRBDMessengerPort")[0].innerHTML =data.messenger_port;
        $("#ldRBDLogToFile")[0].innerHTML =data.log_to_file;
    },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
    });
}

$("#btnUpdate").click(function(){
	var id = $("#id_id").val();
    var cache_dir = $("#id_cache_dir").val();
    var clean_start = $("#id_clean_start").val();
    var enable_memory_usage_tracker = $("#id_enable_memory_usage_tracker").val();
    var object_size = $("#id_object_size").val();
	var cache_total_size = $("#id_cache_total_size").val();
    var cache_dirty_ratio_min = $("#id_cache_dirty_ratio_min").val();
    var cache_ratio_health = $("#id_cache_ratio_health").val();
    var cache_ratio_max = $("#id_cache_ratio_max").val();
    var cache_flush_interval = $("#id_cache_flush_interval").val();
    var cache_evict_interval = $("#id_cache_evict_interval").val();
    var cache_flush_queue_depth = $("#id_cache_flush_queue_depth").val();
    var agent_threads_num = $("#id_agent_threads_num").val();
    var cache_service_threads_num = $("#id_cache_service_threads_num").val();
    var messenger_port = $("#id_messenger_port").val();
    var log_to_file = $("#id_log_to_file").val();

	var data = {
        "id": id,
        "cache_dir": cache_dir,
        "clean_start": clean_start,
        "enable_memory_usage_tracker": enable_memory_usage_tracker,
        "object_size": object_size,
        "cache_total_size": cache_total_size,
        "cache_dirty_ratio_min": cache_dirty_ratio_min,
        "cache_ratio_health": cache_ratio_health,
        "cache_ratio_max": cache_ratio_max,
        "cache_flush_interval": cache_flush_interval,
        "cache_evict_interval": cache_evict_interval,
        "cache_flush_queue_depth": cache_flush_queue_depth,
        "agent_threads_num": agent_threads_num,
        "cache_service_threads_num": cache_service_threads_num,
        "messenger_port": messenger_port,
        "log_to_file": log_to_file
    };
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();

	$.ajax({
		type: "post",
		url: "/hsm_ui/hsm/rbd/update_action/",
		data: postData,
		dataType:"json",
		success: function(data){
				console.log(data);
				window.location.href="/hsm_ui/hsm/rbd/";
		   	},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
				if(XMLHttpRequest.status == 500)
                	showTip("error","INTERNAL SERVER ERROR")
			},
		headers: {
			"X-CSRFToken": token
			},
		complete: function(){

		}
    });

});
