$(document).ready(function(){

	function email_test(email){
		var patten = new RegExp(/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+(com|cn)$/);
		return patten.test(email);
	}

	function shack(sth, dis, time){
		if(!sth) return;
		var dis = dis || 5;
		var time = time || 50;
		sth.stop();
		sth.animate({ left: -dis+"px" }, time)
			.animate({ left: dis+"px" }, time)
			.animate({ left: -dis+"px" }, time)
			.animate({ left: dis+"px" }, time)
			.animate({ left: "0px" }, time)
	}

	$("#sentence a").click(function(){
		$("#left").css("display","none");
		$("#sign").css("display","block");
	});

	function check(){
		var flag = true;
		var email = $("#input_email").val();
		if(!email_test(email)){
			shack($("#input_email"));
			flag = false;
		}
		var pwd = $("#input_pwd").val();
		if(!pwd){
			shack($("#input_pwd"));
			flag = false;
		}
		return flag;
	}

	$("#signin").click(function(){
		if(!check()) return;
		console.log("do_sth_signin");
	});

	$("#signup").click(function(){
		if(!check()) return;
		console.log("do_sth_signup");
	});

	window.shack = shack;
});