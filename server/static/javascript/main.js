$(document).ready(function(){

	function email_test(email){
		/*
		var patten = new RegExp(/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+(com|cn)$/);
		return patten.test(email);
		*/
		return true;
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

	$("#major").click(function(){
		if(!check()) return;
		var data = {};
		data[config.user] = $("#input_email").val();
		data[config.nickname] = $("#input_email").val();
		data[config.password] = $("#input_pwd").val();
		if ($(this).text() == "SIGN IN") 
			$.post('/login', data, function(res) {
				var obj = JSON.parse(res);
				if (obj.redirect) {
					location.href = obj.redirect;
				}
				if (obj.error) {
					$("#error").text(obj.error);
				}
			});
		else
			$.post('/register', data, function(res) {
				var obj = JSON.parse(res);
				if (obj.redirect) {
					location.href = obj.redirect
				}
			});
	});

	$("#minor").click(function(){
		var major = $("#major").text();
		var minor = $("#minor").text();
		$("#major").text(minor);
		$("#minor").text(major)
	});

	window.shack = shack;
});
