$(document).ready(function() {
	hljs.initHighlightingOnLoad();

	$('[data-toggle="tooltip"]').tooltip();

	$.ajaxSetup({
		data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
	});

	$("#ajax-get-test").click(function() {
		$.get("/ajax/get", function(data, status) {
			alert("Data: " + data + "\nStatus: " + status);
		});
	});

	$("#ajax-post-test").click(function() {
		var post_data = prompt("Input your name");
		if (post_data === null || post_data === "") return;
		$.post("/ajax/post", {data: post_data}, function(data, status) {
			if (status === "success") {
				alert(data["text"] + "\nStatus: " + status +
						"\nExtra info: " + data["extra"]);
			} else {
				alert("Fail");
			}
		});
	});

	if ($('#tag-cloud-list').length) {
		$.get('/post/get_tag_cloud_list', function(data, status) { 
			if (status === "success") { 
				var tag_list = data.tag_list; 
				var count = data.count; 
				var font_size = data.size;
				var p = $('#tag-cloud-list'); 
				for (var i = 0; i < tag_list.length; ++i) { 
					var tag_node = '<a href="' + '/tag/' + tag_list[i] + '" style="font-size:' + font_size[i] + 'pt;">' + tag_list[i] + '</a> ';
					p.append(tag_node);
				} 
			} 
		}); 
	}

	if ($('#recent-posts-list').length) {
		$.get('/post/get_recent_posts_list', function(data, status) {
			if (status === "success") {
				var p = $('#recent-posts-list');
				for (var i = 0; i < data.id.length; ++i) {
					p.append('<li><a href="' + '/post/' + data.id[i] + '/">' + 
						data.title[i] + '</a></li>');
				}
			}
		});
	}
});
