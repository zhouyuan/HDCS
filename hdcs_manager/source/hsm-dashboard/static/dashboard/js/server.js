
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
		html += "		</div>";
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

$(document).ready(function(){
    server_id = document.getElementById('tOSAndKernelInfo').title;
    loadOSAndKernel(server_id);
    loadMemory(server_id);
    loadCPU(server_id);
	loadInterval();
});

var refreshInterval=20000;

function loadInterval(){
    server_id = document.getElementById('tOSAndKernelInfo').title;
    setInterval(function(){
        loadOSAndKernel(server_id);
 	    loadMemory(server_id);
        loadCPU(server_id);
    }, refreshInterval);
}

function loadOSAndKernel(server_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/server/"+server_id+"/get_os_and_kernel",
        data: null,
        dataType:"json",
        success: function(data){
            $("#ldDistributorId")[0].innerHTML =data.distributor_id;
            $("#ldRelease")[0].innerHTML =data.release;
            $("#ldCodeName")[0].innerHTML =data.codename;
            $("#ldKernel")[0].innerHTML =data.kernel;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
     });
}

function loadMemory(server_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/server/"+server_id+"/get_mem",
        data: null,
        dataType:"json",
        success: function(data){
            $("#ldTotal")[0].innerHTML =data.total;
            $("#ldUsed")[0].innerHTML =data.available;
            $("#ldFree")[0].innerHTML =data.used;
            $("#ldBuffers")[0].innerHTML =data.free;
            $("#ldCached")[0].innerHTML =data.buffers;
            $("#ldAvailable")[0].innerHTML =data.cached;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
     });
}

function loadCPU(server_id){
    $.ajax({
        type: "get",
        url: "/hsm_ui/hsm/server/"+server_id+"/get_cpu",
        data: null,
        dataType:"json",
        success: function(data){
            $("#ldUser")[0].innerHTML =data.user;
            $("#ldSystem")[0].innerHTML =data.system;
            $("#ldNice")[0].innerHTML =data.nice;
            $("#ldIdle")[0].innerHTML =data.idle;
            $("#ldIOWait")[0].innerHTML =data.iowait;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/hsm_ui/auth/logout/";
        }
     });
}

$("#servers__action_activate").click(function(){
	var server_id_list = {"server_id_list":[]};
	
	var is_selected = false;

	$("#servers>tbody>tr").each(function(){
        if($(this)[0].children[0].children[0].children[0].checked) {
            var server_id = $(this)[0].children[0].children[0].children[0].value;
            is_selected = true;
            server_id_list["server_id_list"].push(server_id);
        }
	});

    if(is_selected == false){
        showTip("warning","please select the server!");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/hsm_ui/hsm/server/activate/",
		data: JSON.stringify(server_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                if(data.error_code.length == 0){
                    window.location.href="/hsm_ui/hsm/server/";
                    showTip("info",data.info);
                }
                else{
                    showTip("error",data.error_msg);
                }
		   	},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
				if(XMLHttpRequest.status == 500){
					$("#divOSDTip").show();
					$("#divOSDTip")[0].innerHTML = XMLHttpRequest.statusText;
				}
			},
		headers: {
			"X-CSRFToken": token
			},
		complete: function(){

		}
    });
	return false;
});
